# v2.0 迁移指南

!!! danger "破坏性变更"

    **mini-swe-agent v2.0** 带来了重大改进，但需要进行迁移。
    如果要继续使用 v1.x，请锁定依赖版本：`mini-swe-agent~=1.0`。
    请参阅 [v1 文档](https://mini-swe-agent.com/v1/) 或 [GitHub 上的 v1 分支](https://github.com/SWE-agent/mini-swe-agent/tree/v1)。

## 新特性

- **工具调用（Tool calls）**：原生工具调用 API 支持（现已成为默认方式）
- **多模态输入**：支持图片和其他内容类型

## 我需要改什么？

> 我只用默认配置的 mini CLI

无需改动。

> 我使用自定义配置

你可能需要移动一些配置键。请参见[配置变更](#配置变更)。

> 我要解析／分析轨迹

一些元数据字段移到了 `extra` 中。请参见[轨迹格式](#轨迹格式)。

> 我使用 Python 绑定，或者构建了自定义子类

你需要重构。可以让智能体根据下面的说明来重构你的代码。

## 配置变更

如果你只修改过 `system_template` 和 `instance_template`，则无需改动。

**从 `agent` 移到 `model`：**

- `observation_template`（由 `action_observation_template` 改名而来）
- `format_error_template`
- `action_regex`（仅用于基于文本的解析）

**已移除：**

- `timeout_template`

**代码块格式变更：**

默认的动作正则从 `` ```bash `` 改为 `` ```mswea_bash_command ``，以避免与提示词中的 bash 示例冲突。

**完成信号变更：**

从 `echo MINI_SWE_AGENT_FINAL_OUTPUT` 改为 `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`。

**新结构：**

```yaml
agent:
  system_template: "..."
  instance_template: "..."
  step_limit: 0
  cost_limit: 3.
environment:
  cwd: "..."
  timeout: 30
model:
  model_name: "..."
  observation_template: "..."
  format_error_template: "..."
```

**CLI 现在支持多个配置和键值覆盖：**

```bash
mini -c mini.yaml -c model.model_kwargs.temperature=0.5
mini -c swebench.yaml -c agent.step_limit=100
mini -c mini.yaml -c /path/to/model.yaml
```

!!! warning
    如果你使用 `-c`，就不会加载完整的默认配置，因此请务必在指定覆盖／更新项的同时，始终指定你的配置文件。

## 工具调用

v2.0 默认使用原生工具调用（而不是基于正则的文本解析）。

**有什么区别？**

- 工具调用（默认）：模型使用原生工具调用 API 来调用一个“bash”工具
- 基于文本（旧方式）：模型在 markdown 代码块（或类似格式）中输出命令，再用正则提取

**怎么用：**

工具调用是默认方式。CLI 使用为工具调用配置的 `mini.yaml` 和 `swebench.yaml`。

```bash
# 默认（工具调用）
mini
python -m minisweagent.run.benchmarks.swebench
mini-extra swebench

# 基于文本的解析
mini-extra swebench -c swebench_backticks.yaml
mini -c mini_textbased.yaml
```

**对于自定义配置：**

```yaml
model:
  model_class: litellm  # 工具调用（默认）
  model_name: anthropic/claude-sonnet-4-5-20250929

# 或者使用基于文本的方式：
model:
  model_class: litellm_textbased
  action_regex: "```mswea_bash_command\\s*\\n(.*?)\\n```"
```

## 轨迹格式

- 在 v1 中，轨迹的 `messages` 字段中的所有消息都是“手工格式化”的，即都带有 `content: str` 和 `role: str` 字段。
- **在 v2 中，我们以模型的原生输出作为消息的基础，只额外添加 `extra` 字段**。

如果你使用的模型走标准的 `/completion` 端点，那么你仍然总是会有 `content: str` 和 `role: str` 字段。
但如果你使用 [`/response`](https://platform.openai.com/docs/api-reference/responses) 端点，情况可能就不一样了。

换句话说：确切的消息结构取决于你使用的模型。

* 优点：支持任何模型的消息结构
* 缺点：如果你要解析轨迹，可能需要适配所用模型的消息结构。

## 移除与重命名

**移除的功能：**

- **“可视”界面**：替代性的、基于文本的 `mini -v` CLI 的 `-v` 参数不再受支持。这是一个艰难的决定，但最终可视模式没有获得我们期望的采用率，而且维护成本远高于默认界面。
- **轮换 API key**：不再支持用 `::` 分隔的 `ANTHROPIC_API_KEYS`。请使用单个 `ANTHROPIC_API_KEY`。
- **`github_issue` 运行脚本**：专用的 `github_issue.py` 运行脚本已被移除。请改用 `mini` CLI。
- **`MSWEA_MODEL_API_KEY` 环境变量**：不再用于覆盖 API key。

**移除的模型类：**

- **`anthropic` 模型类**：已移除。Anthropic 模型请使用 `litellm` 模型类（确保启用缓存控制）。

**重命名的模型类：**

| v1 名称 | v2 名称 |
|---------|---------|
| `litellm_response_api` | `litellm_response` |
| `portkey_response_api` | `portkey_response` |

**新增的模型类：**

| 名称 | 说明 |
|------|-------------|
| `litellm_textbased` | 基于文本的解析（正则），替代工具调用 |
| `openrouter_textbased` | OpenRouter 的基于文本的解析 |
| `openrouter_response` | 带 response API 的 OpenRouter |

**新增的环境：**

- **`swerex_modal`**：在 Modal 上运行环境（需要 `pip install mini-swe-agent[modal]`）

## 架构变更

1. **职责转移**：模型现在负责解析动作和格式化观察结果。这样就能通过更换模型类在工具调用与文本解析之间切换。Agent 类现在是一个更简单的协调者。

2. **无状态模型**：成本追踪移到了 Agent。Model 协议中的 `cost` 和 `n_calls` 属性已被移除。

3. **Pydantic 配置**：`AgentConfig`（以及其他配置）从 `dataclass` 改为 Pydantic 的 `BaseModel`。这要求 `pydantic >= 2.0`。

4. **新增协议方法**：所有类都实现 `get_template_vars()` 和 `serialize()`，而不再要求具备特定属性。

### 协议变更

如果你想编写一个与 `mini-swe-agent` 兼容的自定义 Model、Environment 或 Agent，你不需要继承任何东西。
相反，mini-swe-agent 完全使用[协议（protocols）](https://typing.python.org/en/latest/spec/protocol.html)的鸭子类型
（简而言之：只要实现了所需的方法，你就可以把任何类当作 Model、Environment 或 Agent 使用）。
像 `--config-class` 这样的配置选项也接受完整的导入类，因此你可以把自己的类放在任何地方。

**Model 协议：**

```python
# 移除的属性
cost: float      # 移到了 Agent
n_calls: int     # 移到了 Agent

# 新增的方法
def format_message(self, **kwargs) -> dict: ...
def format_observation_messages(self, message: dict, outputs: list[dict], template_vars: dict | None = None) -> list[dict]: ...
def serialize(self) -> dict: ...
```

**Environment 协议：**

```python
# 签名变更
def execute(self, action: dict, cwd: str = "") -> dict[str, Any]: ...  # 原为：(command: str) -> dict[str, str]

# 新增方法
def serialize(self) -> dict: ...
```

**Agent 协议：**

```python
# 移除的属性（你不再需要实现这些，但仍然可以实现）
model: Model
env: Environment
messages: list[dict]

# 返回类型变更
def run(self, task: str, **kwargs) -> dict: ...  # 原为：tuple[str, str]

# 新增方法
def save(self, path: Path | None, *extra_dicts) -> dict: ...
```

### 异常变更

所有流程控制异常现在都继承自 `InterruptAgentFlow`，并移到了 `minisweagent.exceptions`：

```python
InterruptAgentFlow (基类)
├── Submitted (任务完成)
├── LimitsExceeded (成本/步数上限)
├── FormatError (模型输出无效)
└── UserInterruption (用户取消)  # 新增
```

**移除的异常类：**

- `NonTerminatingException` - 请使用 `InterruptAgentFlow` 基类
- `TerminatingException` - 请使用 `InterruptAgentFlow` 基类
- `ExecutionTimeoutError` - 已移除（不再使用）

```python
# 旧写法
from minisweagent.agents.default import Submitted, FormatError

# 新写法
from minisweagent.exceptions import Submitted, FormatError
```

### Agent.run() 的返回值

```python
# 旧写法（v1）
submission, exit_status = agent.run(task)  # tuple[str, str]

# 新写法（v2）
result = agent.run(task)  # dict
submission = result["submission"]
exit_status = result["exit_status"]
```

`run()` 方法返回最终退出消息中的 `extra` 字典。要获取完整的轨迹数据，请使用 `agent.save(path)` 或 `agent.serialize()`。

# Cookbook

!!! abstract "混搭与扩展 mini"

    * 本指南介绍如何混合 `mini` 智能体的各个组件，创建你自己的定制版本。
    * 你可能想先看看[默认智能体的控制流](control_flow.md)


!!! note "开发环境搭建"

    请务必按照 [quickstart.md](../quickstart.md) 中的开发环境搭建说明操作。

我们提供了几种不同的智能体入口点，
例如 [hello world](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/hello_world.py)，
或者[调用 `mini` 时的默认入口](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/mini.py)。

想让配置已经不足以满足你的定制需求？
只需按下面的配方操作：

1. 你需要什么样的控制流？选一个[智能体类](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents)（例如[最简示例](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py)、[带人在回路](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/interactive.py)）
2. 动作应该怎么执行？选一个[环境类](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments)（例如[本地](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py)或[docker](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments/docker.py)）
3. 如何查询语言模型？选一个[模型类](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models)（例如 [litellm](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)）
4. 如何调用智能体？把它们一起绑定到一个[运行脚本](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run)中，也可以从[配置](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/config)中读取（例如 [hello world](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/hello_world.py) 或 [`mini` 入口点](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/mini.py)）

我们的目标是让所有这些组件都非常简单，但它们之间有大量可选组合——足以覆盖你可能想做的各种事情。

你可以把 `MSWEA_DEFAULT_RUN` 环境变量设为你运行脚本的导入路径，从而覆盖默认入口点。

## Hello world

最基本的示例请参见 [Python 绑定](../usage/python_bindings.md)。

## 混搭组合

### 模型

=== "Hello world（使用自动模型选择）"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.models import get_model
    from minisweagent.environments.local import LocalEnvironment

    model_name = "anthropic/claude-sonnet-4-5-20250929"

    agent = DefaultAgent(
        get_model(input_model_name=model_name),
        LocalEnvironment(),
    )
    agent.run(task)
    ```

=== "Hello world（Litellm）"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.models.litellm_model import LitellmModel
    from minisweagent.environments.local import LocalEnvironment

    model_name = "gpt-4o"

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        LocalEnvironment(),
    )
    agent.run(task)
    ```

### 环境

=== "使用本地执行的 Hello world"

    ```python
    from minisweagent.environments.local import LocalEnvironment

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        LocalEnvironment(),
    )
    ```

=== "使用 docker 执行的 Hello world"

    ```python
    from minisweagent.environments.docker import DockerEnvironment

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        DockerEnvironment(),
    )
    ```

### 智能体

=== "默认智能体"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.models import get_model
    from minisweagent.environments.local import LocalEnvironment

    agent = DefaultAgent(
        get_model(input_model_name=model_name),
        LocalEnvironment(),
    )
    ```

=== "人在回路"

    ```python
    from minisweagent.agents.interactive import InteractiveAgent
    from minisweagent.models import get_model
    from minisweagent.environments.local import LocalEnvironment

    agent = InteractiveAgent(
        get_model(input_model_name=model_name),
        LocalEnvironment(),
    )
    ```

## 进阶

### 自定义执行方式

一个对某些动作使用 python 函数的智能体：


=== "子类化智能体"

    ```python
    from minisweagent.agents.default import DefaultAgent
    import shlex

    def python_function(*args) -> dict:
        ...
        return {"output": "..."}

    class AgentWithPythonFunctions(DefaultAgent):
        def execute_actions(self, message: dict) -> list[dict]:
            for action in message.get("extra", {}).get("actions", []):
                command = action.get("command", "")
                if command.startswith("python_function"):
                    args = shlex.split(command.removeprefix("python_function").strip())
                    return self.add_messages(self.model.format_observation_messages(
                        message, [python_function(*args)], self.get_template_vars()
                    ))
            # 其余情况一切照旧
            return super().execute_actions(message)
    ```


=== "子类化环境"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment
    import shlex

    def python_function(*args) -> dict:
        ...
        return {"output": "..."}

    class EnvironmentWithPythonFunctions(LocalEnvironment):
        def execute(self, action: dict, cwd: str = "") -> dict:
            command = action.get("command", "")
            if command.startswith("python_function"):
                args = shlex.split(command.removeprefix("python_function").strip())
                return python_function(*args)
            # 其他所有命令都照常执行
            return super().execute(action, cwd)

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        EnvironmentWithPythonFunctions(),
    )
    ```

一个在发出 `submit` 命令时退出的智能体：

=== "子类化智能体"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.exceptions import Submitted

    class AgentQuitsOnSubmit(DefaultAgent):
        def execute_actions(self, message: dict) -> list[dict]:
            for action in message.get("extra", {}).get("actions", []):
                if action.get("command", "") == "submit":
                    # `Submitted` 异常会被智能体捕获，
                    # 并打印最终输出。
                    raise Submitted({
                        "role": "exit",
                        "content": "The agent has finished its task.",
                        "extra": {"exit_status": "Submitted", "submission": ""},
                    })
            return super().execute_actions(message)
    ```

=== "子类化环境"

    ```python
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment
    from minisweagent.exceptions import Submitted

    class EnvironmentQuitsOnSubmit(LocalEnvironment):
        def execute(self, action: dict, cwd: str = "") -> dict:
            if action.get("command", "") == "submit":
                raise Submitted({
                    "role": "exit",
                    "content": "The agent has finished its task.",
                    "extra": {"exit_status": "Submitted", "submission": ""},
                })
            return super().execute(action, cwd)

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        EnvironmentQuitsOnSubmit(),
    )
    ```


一个在执行前校验动作的智能体（同时也是如何使用扩展配置类的示例）：

=== "子类化智能体"

    ```python
    import re
    from minisweagent.agents.default import DefaultAgent, AgentConfig
    from minisweagent.exceptions import FormatError
    from pydantic import BaseModel

    class ValidatingAgentConfig(AgentConfig):
        forbidden_patterns: list[str] = [
            r"rm -rf /",
            r"sudo.*passwd",
            r"mkfs\.",
        ]

    class ValidatingAgent(DefaultAgent):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs, config_class=ValidatingAgentConfig)

        def execute_actions(self, message: dict) -> list[dict]:
            for action in message.get("extra", {}).get("actions", []):
                command = action.get("command", "")
                for pattern in self.config.forbidden_patterns:
                    if re.search(pattern, command, re.IGNORECASE):
                        raise FormatError(self.model.format_message(
                            role="user", content="Action blocked: forbidden pattern detected"
                        ))
            return super().execute_actions(message)
    ```

=== "子类化环境"

    ```python
    import re
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment, LocalEnvironmentConfig
    from minisweagent.models.litellm_model import LitellmModel

    class EnvironmentWithForbiddenPatternsConfig(LocalEnvironmentConfig):
        forbidden_patterns: list[str] = [
            r"rm -rf /",
            r"sudo.*passwd",
            r"mkfs\.",
        ]

    class EnvironmentWithForbiddenPatterns(LocalEnvironment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs, config_class=EnvironmentWithForbiddenPatternsConfig)

        def execute(self, action: dict, cwd: str = "") -> dict:
            command = action.get("command", "")
            for pattern in self.config.forbidden_patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return {"output": "Action blocked: forbidden pattern detected", "returncode": 1}
            return super().execute(action, cwd)

    agent = DefaultAgent(
        LitellmModel(model_name=model_name),
        EnvironmentWithForbiddenPatterns(),
    )
    ```

### 在 Ray 上运行 mini-swe-agent

[这篇博客文章](https://www.anyscale.com/blog/massively-parallel-agentic-simulations-with-ray)
介绍了如何用 Ray 并行运行 mini-swe-agent。

{% include-markdown "_footer.md" %}

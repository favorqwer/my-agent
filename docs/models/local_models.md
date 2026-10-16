!!! abstract "本地模型"

    * 本指南介绍如何设置本地模型。
    * 你应该已经熟悉[快速入门指南](../quickstart.md)了。
    * 你还应该快速浏览一下[全局配置指南](../advanced/global_configuration.md)，以理解
      全局配置，以及 [Yaml 配置文件指南](../advanced/yaml_configuration.md)。


!!! tip "示例"

    * [议题 #303](https://github.com/SWE-agent/mini-swe-agent/issues/303) 中有若干使用本地模型的示例。
    * 我们也欢迎通过 pull request 向本指南补充具体的使用示例。

## 使用 litellm

目前，模型默认通过 [`litellm`](https://www.litellm.ai/) 支持。

使用本地模型通常分两步：

1. 编辑智能体配置文件，加入 `custom_llm_provider`、`api_base` 之类的设置。
2. 要么忽略成本追踪产生的错误，要么更新模型注册表以包含你的本地模型。

### 设置 API base／提供商

如果你使用本地模型，很可能需要给 `litellm` 调用添加一些额外的关键字参数。
这通过 `model_kwargs` 字典完成，它会直接传给 `litellm.completion`。

换句话说，我们是这样调用 litellm 的：

```python
litellm.completion(
    model=model_name,
    messages=messages,
    **model_kwargs
)
```

你可以像下面这样在智能体配置文件中设置 `model_kwargs`：

??? note "默认配置文件"

    ```yaml
    --8<-- "src/minisweagent/config/mini.yaml"
    ```

在最后一节中，你可以添加：

```yaml
model:
  model_name: "my-local-model"
  model_kwargs:
    custom_llm_provider: "openai"
    api_base: "https://..."
    ...
  ...
```

!!! tip "更新默认的 `mini` 配置文件"

    你可以设置 `MSWEA_MINI_CONFIG_PATH` 来指定默认 `mini` 配置文件的路径。
    这样你就能用自己的配置覆盖默认配置文件。
    更多细节请参见[全局配置指南](../advanced/global_configuration.md)。

如果这还不够，我们的模型类应该很容易修改：

??? note "完整的模型类"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)
    - [API 参考](../reference/models/litellm.md)

    ```python
    --8<-- "src/minisweagent/models/litellm_model.py"
    ```

另一件你很可能需要搞清楚的事情是成本。
用 `litellm` 有两种处理方式：

1. 搭建一个 litellm 代理服务器（它能让你对所有语言模型调用拥有很强的控制力）
2. 更新模型注册表（见下一节）

### 成本追踪

如果按上面的方式运行，你很可能会遇到缺少成本信息的错误。

如果你不需要成本追踪，可以忽略这些错误，最好是在智能体配置文件中加入：

```yaml
model:
  cost_tracking: "ignore_errors"
  ...
...
```

或者，你可以设置全局配置：

```bash
export MSWEA_COST_TRACKING="ignore_errors"
```

不过要注意，这是一个全局设置，会影响所有模型！

然而，处理成本问题的最佳方式是给 litellm 添加一个模型注册表，把你的本地模型包含进去。

LiteLLM 的模型成本与元数据来自[这个文件](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)。如果该文件过时或缺少你想要的模型，你可以通过提供一个自定义注册表文件来覆盖或补充其中的数据。

模型注册表 JSON 文件应遵循 LiteLLM 的格式：

```json
{
  "my-custom-model": {
    "max_tokens": 4096,
    "input_cost_per_token": 0.0001,
    "output_cost_per_token": 0.0002,
    "litellm_provider": "openai",
    "mode": "chat"
  },
  "my-local-model": {
    "max_tokens": 8192,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
    "litellm_provider": "ollama",
    "mode": "chat"
  }
}
```

!!! warning "模型名称"

    模型名称区分大小写。请确保完全匹配。

!!! warning "模型提供商"

    如果你使用了 `custom_llm_provider`，或者在模型名前面加了提供商前缀（例如 `openai/...`），
    那么它必须与配置中的 `litellm_provider` 一致！

设置模型注册表路径有两种方式：

1. 设置 `LITELLM_MODEL_REGISTRY_PATH`（例如 `mini-extra config set LITELLM_MODEL_REGISTRY_PATH /path/to/model_registry.json`）
2. 在智能体配置文件中设置 `litellm_model_registry`

```yaml
model:
  litellm_model_registry: "/path/to/model_registry.json"
  ...
...
```

## 具体示例

### 用 vLLM 生成 SWE-bench 轨迹

本示例展示如何使用 [vLLM](https://docs.vllm.ai/en/latest/) 作为本地推理引擎来生成 SWE-bench 轨迹。

首先，用你选定的模型启动一个 vLLM 服务器。例如：

```bash
vllm serve ricdomolm/mini-coder-1.7b &
```

默认情况下，服务器会在 `http://localhost:8000` 上可用。

其次，编辑位于 `src/minisweagent/config/benchmarks/swebench.yaml` 的 mini-swe-agent SWE-bench 配置文件，加入你的本地 vLLM 模型：

```yaml
model:
  model_name: "hosted_vllm/ricdomolm/mini-coder-1.7b"  # 或 hosted_vllm/path/to/local/model
  model_kwargs:
    api_base: "http://localhost:8000/v1"  # 如果使用非默认端口/地址，请相应调整
```

如果你需要上面的自定义注册表，请创建一个 `registry.json` 文件：

```bash
cat > registry.json <<'EOF'
{
  "ricdomolm/mini-coder-1.7b": {
    "max_tokens": 40960,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
    "litellm_provider": "hosted_vllm",
    "mode": "chat"
  }
}
EOF
```

现在你就可以生成轨迹了！让我们来解 SWE-bench Verified 中的 `django__django-11099` 实例：

```bash
LITELLM_MODEL_REGISTRY_PATH=registry.json mini-extra swebench \
    --output test/ --subset verified --split test --filter '^(django__django-11099)$'
```

现在你应该能在 `test/` 目录中看到生成的轨迹了。

--8<-- "docs/_footer.md"

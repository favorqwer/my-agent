# Litellm Response Model

!!! note "LiteLLM Response API 模型类"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_response_model.py)

    ??? note "完整源代码"

        ```python
        --8<-- "src/minisweagent/models/litellm_response_model.py"
        ```

!!! tip "何时使用这个模型"

    * 当你想使用 OpenAI 的 [Responses API](https://platform.openai.com/docs/api-reference/responses) 并配合原生工具调用时，请使用这个模型类。
    * 这对于 GPT-5 之类受益于 Responses API 提供的扩展思考／推理能力的模型特别有用。
    * 该模型通过 `previous_response_id` 跨轮次维护对话状态。

## 用法

要使用 Response API 模型，请在智能体配置中指定 `model_class: "litellm_response"`：

```yaml
model:
  model_class: "litellm_response"
  model_name: "openai/gpt-5.2"
  model_kwargs:
    drop_params: true
    reasoning:
      effort: "high"
```

或者通过命令行：

```bash
mini -m "openai/gpt-5.2" --model-class litellm_response
```

::: minisweagent.models.litellm_response_model

{% include-markdown "../../_footer.md" %}

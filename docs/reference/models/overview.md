# Models 概览

本页介绍 mini-SWE-agent 中所有可用的模型类。

## 模型类

| 类 | 快捷名 | 端点 | 工具调用 | 说明 |
|-------|----------|----------|-----------|-------------|
| [`LitellmModel`](litellm.md) | `litellm` | `/completion` | ✅ | 默认模型，使用 [LiteLLM](https://docs.litellm.ai/docs/providers) 提供广泛的提供商支持（OpenAI 官方及其兼容中转站、Anthropic、Gemini、DeepSeek、100+ 提供商） |
| [`LitellmTextbasedModel`](litellm.md) | `litellm_textbased` | `/completion` | ❌ | 使用基于文本动作的 LiteLLM（无原生工具调用） |
| [`LitellmResponseModel`](litellm_response_toolcall.md) | `litellm_response` | `/response` | ✅ | 使用 [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses) 和原生工具调用的 LiteLLM |
| [`DeterministicModel`](test_models.md) | `deterministic` | N/A | ❌ | 返回预定义输出（用于测试） |

{% include-markdown "../../_footer.md" %}

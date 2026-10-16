# Models 概览

本页介绍 mini-SWE-agent 中所有可用的模型类。

## 模型类

| 类 | 快捷名 | 端点 | 工具调用 | 说明 |
|-------|----------|----------|-----------|-------------|
| [`LitellmModel`](litellm.md) | `litellm` | `/completion` | ✅ | 默认模型，使用 [LiteLLM](https://docs.litellm.ai/docs/providers) 提供广泛的提供商支持（OpenAI、Anthropic、100+ 提供商） |
| [`LitellmTextbasedModel`](litellm.md) | `litellm_textbased` | `/completion` | ❌ | 使用基于文本动作的 LiteLLM（无原生工具调用） |
| [`LitellmResponseModel`](litellm_response_toolcall.md) | `litellm_response` | `/response` | ✅ | 使用 [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses) 和原生工具调用的 LiteLLM |
| [`OpenRouterModel`](openrouter.md) | `openrouter` | `/completion` | ✅ | [OpenRouter](https://openrouter.ai/) API 集成 |
| [`OpenRouterTextbasedModel`](openrouter.md) | `openrouter_textbased` | `/completion` | ❌ | 使用基于文本动作的 OpenRouter |
| [`OpenRouterResponseModel`](openrouter.md) | `openrouter_response` | `/response` | ✅ | 使用原生工具调用的 OpenRouter Responses API |
| [`PortkeyModel`](portkey.md) | `portkey` | `/completion` | ✅ | [Portkey](https://portkey.ai/) AI 网关集成 |
| [`PortkeyResponseAPIModel`](portkey_response.md) | `portkey_response` | `/response` | ✅ | 支持 Responses API 的 Portkey |
| [`RequestyModel`](requesty.md) | `requesty` | `/completion` | ✅ | [Requesty](https://requesty.ai/) API 集成 |
| [`DeterministicModel`](test_models.md) | `deterministic` | N/A | ❌ | 返回预定义输出（用于测试） |
| [`RouletteModel`](extra.md) | — | 元 | ❌ | 从多个模型中随机选择 |
| [`InterleavingModel`](extra.md) | — | 元 | ❌ | 按顺序在多个模型之间交替 |

{% include-markdown "../../_footer.md" %}

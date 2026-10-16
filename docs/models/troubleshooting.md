# 模型故障排查

本节收录了常见错误信息以及对应的解决方法。

## Litellm

`litellm` 是默认的模型类，用于支持大多数模型。

### API key 无效

```json
AuthenticationError: litellm.AuthenticationError: geminiException - {
  "error": {
    "code": 400,
    "message": "API key not valid. Please pass a valid API key.",
    "status": "INVALID_ARGUMENT",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "API_KEY_INVALID",
        "domain": "googleapis.com",
        "metadata": {
          "service": "generativelanguage.googleapis.com"
        }
      },
      {
        "@type": "type.googleapis.com/google.rpc.LocalizedMessage",
        "locale": "en-US",
        "message": "API key not valid. Please pass a valid API key."
      }
    ]
  }
}
 You can permanently set your API key with `mini-extra config set KEY VALUE`.
```

请仔细检查你的 API key，确保它是正确的。
你可以用 `mini-extra config edit` 查看所有 API key。

### “奇怪的”认证错误

如果你认证失败，但看到的不是上面那条错误信息，
那可能是你忘了在模型名称中包含提供商。

例如，下面这个：

```
  File "/Users/.../.virtualenvs/openai/lib/python3.12/site-packages/google/auth/_default.py", line 685, in default
    raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS)
google.auth.exceptions.DefaultCredentialsError: Your default credentials were not found. To set up Application Default Credentials, see
https://cloud.google.com/docs/authentication/external/set-up-adc for more information.
```

就是因为你忘了给 gemini 模型加上 `gemini/` 前缀。

### 计算成本时出错

```
Exception: This model isn't mapped yet. model=together_ai/qwen/qwen3-coder-480b-a35b-instruct-fp8, custom_llm_provider=together_ai.
Add it here - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json.
```

`litellm` 不知道你这个模型的成本。
请参考[本地模型](local_models.md)指南中的模型注册表一节来添加它。

另一个常见错误是模型名称中完全没有提供商，或提供商写错了（例如写成 `gemini-2.0-flash` 而不是 `gemini/gemini-2.0-flash`）。

## 不支持 temperature

有些模型（例如 `o1`、`o3`、`GPT-5` 等）不支持 temperature。默认配置已不再指定 temperature 值，所以现在开箱即用应该没问题。

## Portkey

### 计算成本时出错

我们使用 `litellm` 来计算 Portkey 模型的成本，因为 Portkey 似乎无法通过方便的 API 提供每次请求的成本信息。

这可能导致如下错误：

```
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/minisweagent/models/portkey_model.py", line 85, in query
    cost = litellm.cost_calculator.completion_cost(response)
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/cost_calculator.py", line 973, in completion_cost
    raise e
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/cost_calculator.py", line 966, in completion_cost
    raise e
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/cost_calculator.py", line 928, in completion_cost
    ) = cost_per_token(
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/cost_calculator.py", line 218, in cost_per_token
    _, custom_llm_provider, _, _ = litellm.get_llm_provider(model=model)
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/litellm_core_utils/get_llm_provider_logic.py", line 395, in get_llm_provider
    raise e
  File "/opt/miniconda3/envs/clash/lib/python3.10/site-packages/litellm/litellm_core_utils/get_llm_provider_logic.py", line 372, in get_llm_provider
    raise litellm.exceptions.BadRequestError(  # type: ignore
litellm.exceptions.BadRequestError: litellm.BadRequestError: LLM Provider NOT provided. Pass in the LLM provider you are trying to call. You passed model=grok-code-fast-1
 Pass model as E.g. For 'Huggingface' inference endpoints pass in `completion(model='huggingface/starcoder',..)` Learn more: https://docs.litellm.ai/docs/providers
```

在这种情况下，问题仅仅在于 portkey 的模型名称与 litellm 的模型名称不匹配（具体到这里，
就是没有包含提供商）。

要解决这个问题，你可以用 `litellm_model_name_override` 键手动把 litellm 模型名称设为 portkey 的模型名称。
例如：

```yaml
model:
  model_name: "grok-code-fast-1"  # portkey 的模型名称
  model_class: "portkey"  # 确保使用 portkey 模型类
  litellm_model_name_override: "xai/grok-code-fast-1"  # 用于成本信息的 litellm 模型名称
  ...
```

--8<-- "docs/_footer.md"

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

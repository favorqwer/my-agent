# 模型设置快速入门

!!! tip "设置"

    * 大多数情况下，你只需运行 `mini-extra config setup` 即可设置默认模型和 API key。
      首次运行 `mini` 时应该也会自动运行它。
    * 默认情况下，我们通过 [`litellm`](https://github.com/BerriAI/litellm) 支持所有模型。
    * 我们也支持通过 [Openrouter](https://openrouter.ai/) 和 [Portkey](https://portkey.ai/) 使用模型。

## 设置 API key

有几种设置 API key 的方式：

* **推荐**：运行我们的设置脚本：`mini-extra config setup`。首次运行 `mini` 时它应该也会自动运行。
* 使用 `mini-extra config set ANTHROPIC_API_KEY <your-api-key>` 把 key 写入 `mini` 的[配置文件](../advanced/global_configuration.md)。
* 把 key 导出为环境变量：`export ANTHROPIC_API_KEY=<your-api-key>`（重启 shell 后不会保留，除非你把它加到 shell 配置文件中，比如 `~/.bashrc` 或 `~/.zshrc`）。
* 如果你要并行运行多个智能体，请参见我们关于轮换 anthropic key 的说明（见[这里](../advanced/global_configuration.md)）。

??? note "所有 API key 名称"

    我们使用 [`litellm`](https://github.com/BerriAI/litellm) 来支持大多数模型。
    以下是 `litellm` 中可用的所有 API key 名称列表：

    ```
    ALEPH_ALPHA_API_KEY
    ALEPHALPHA_API_KEY
    ANTHROPIC_API_KEY
    ANYSCALE_API_KEY
    AZURE_AI_API_KEY
    AZURE_API_KEY
    AZURE_OPENAI_API_KEY
    BASETEN_API_KEY
    CEREBRAS_API_KEY
    CLARIFAI_API_KEY
    CLOUDFLARE_API_KEY
    CO_API_KEY
    CODESTRAL_API_KEY
    COHERE_API_KEY
    DATABRICKS_API_KEY
    DEEPINFRA_API_KEY
    DEEPSEEK_API_KEY
    FEATHERLESS_AI_API_KEY
    FIREWORKS_AI_API_KEY
    FIREWORKS_API_KEY
    FIREWORKSAI_API_KEY
    GEMINI_API_KEY
    GROQ_API_KEY
    HUGGINGFACE_API_KEY
    INFINITY_API_KEY
    MARITALK_API_KEY
    MISTRAL_API_KEY
    NEBIUS_API_KEY
    NLP_CLOUD_API_KEY
    NOVITA_API_KEY
    NVIDIA_NIM_API_KEY
    OLLAMA_API_KEY
    OPENAI_API_KEY
    OPENAI_LIKE_API_KEY
    OPENROUTER_API_KEY
    OR_API_KEY
    PALM_API_KEY
    PERPLEXITYAI_API_KEY
    PREDIBASE_API_KEY
    PROVIDER_API_KEY
    REPLICATE_API_KEY
    TOGETHERAI_API_KEY
    VOLCENGINE_API_KEY
    VOYAGE_API_KEY
    WATSONX_API_KEY
    WX_API_KEY
    XAI_API_KEY
    XINFERENCE_API_KEY
    ```

    此外，Portkey 模型使用 `PORTKEY_API_KEY` 环境变量。

## 选择模型

!!! note "模型名称与提供商。"

    我们使用 [`litellm`](https://github.com/BerriAI/litellm) 支持大多数模型。
    你可以[在这里](https://docs.litellm.ai/docs/providers)找到其支持的模型列表。
    请务必在模型名称中包含提供商，例如 `anthropic/claude-...`。

* **推荐**：`mini-extra config setup`（首次运行 `mini` 时应会自动运行）可以为你设置默认模型
* 所有命令行界面都允许你通过 `-m` 或 `--model` 设置模型名称。
* 此外，你还可以通过 `mini-extra config set MSWEA_MODEL_NAME <model-name>`、编辑全局[配置文件](../advanced/global_configuration.md)（快捷方式：`mini-extra config edit`），或设置 `MSWEA_MODEL_NAME` 环境变量来设置默认模型。
* 你也可以在配置文件中设置模型（`model` 下的 `model_name` 键）。
* 如果你想使用本地模型，请查看这份[指南](local_models.md)。

!!! note "常用模型"

    以下是一些常用模型的示例：

    ```
    anthropic/claude-opus-4-6-20260205
    openai/gpt-5.4
    openai/gpt-5.4-mini
    gemini/gemini-2.5-pro
    deepseek/deepseek-chat
    ```

    ??? note "所有受支持模型的列表"

        以下是截至 2025 年 8 月 29 日 `litellm` 支持的所有模型名称列表。
        如需更新的模型，请查看 [litellm 的 `model_prices_and_context_window.json` 文件](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)。

        ```
        --8<-- "docs/data/all_models.txt"
        ```

要找到对应的 API key，请查看上一节。

## 额外的模型设置

要配置推理强度（reasoning effort）或类似设置，你需要编辑[智能体配置文件](../advanced/yaml_configuration.md)。
在较新的版本中，运行 `mini` 时会打印配置文件的位置（输出中的 "agent config"）。

以下是一些通用示例：

=== "Temperature"

    `litellm` 允许通过 `model_kwargs` 键设置模型专属设置：

    ```yaml
    model:
      model_name: "anthropic/claude-sonnet-4-5-20250929"
        model_kwargs:
          temperature: 0.0
    ```

    注意，并非所有模型都支持 temperature。

=== "GPT-5 推理强度（Chat Completions API）"

    `litellm` 允许通过 `model_kwargs` 键设置模型专属设置：

    ```yaml
    model:
      model_name: "openai/gpt-5-mini"
      model_kwargs:
        drop_params: true
        reasoning_effort: "high"
        verbosity: "medium"
    ```

    这里用 `drop_params` 来丢弃模型不支持的参数。

=== "使用 Responses API 的 GPT-5"

    对于支持 Responses API 的 OpenAI 模型，你可以使用 `litellm_response_toolcall` 模型类：

    ```yaml
    model:
      model_class: "litellm_response_toolcall"
      model_name: "openai/gpt-5-mini"
      model_kwargs:
        drop_params: true
        reasoning:
          effort: "high"
    ```

=== "OpenRouter"

    本示例显式把模型类设为 `openrouter`（更多细节见下一节）。
    它还显式指定了提供商，以禁用它们之间的切换（如果你需要非常一致的成本行为，
    例如做基准评测，这会很有用；但如果你只是想要低延迟和好价格，则不推荐这样做）。

    ```yaml
    model:
        model_name: "moonshotai/kimi-k2-0905"
        model_class: "openrouter"
        model_kwargs:
            temperature: 0.0
            provider:
              allow_fallbacks: false
              only: ["Moonshot AI"]
    ```

=== "本地模型"

    将 `litellm` 与本地模型配合使用：

    ```yaml
    model:
      model_name: "my-local-model"
      model_kwargs:
        custom_llm_provider: "openai"
        api_base: "https://..."
        ...
    ```

    本地模型的更多细节请参见[这份指南](local_models.md)。
    特别地，你需要为本地模型配置 token 成本。

以下是配置特定模型的更多示例：

=== "Gemini 3（Openrouter）"

    ```yaml
    model:
        model_name: "google/gemini-3-pro-preview"
        model_class: openrouter
        model_kwargs:
            temperature: 0.0
    ```

=== "GPT 5.1 medium（Portkey）"

    ```yaml
    model:
        model_name: "@openai/gpt-5.1"
        model_class: portkey
        model_kwargs:
            reasoning_effort: "medium"
            verbosity: "medium"
    ```

=== "Claude Haiku 4.5"

    ```yaml
    model:
        model_name: "anthropic/claude-haiku-4-5-20251001"
        model_kwargs:
            temperature: 0.0
    ```

=== "GPT 5 mini（Portkey）"

    ```yaml
    model:
        model_name: "@openai/gpt-5-mini"
        model_class: portkey
    ```

=== "Deepseek"

    ```yaml
    model:
        model_name: "deepseek/deepseek-reasoner"
        model_kwargs:
            temperature: 0.0
    ```

=== "Minimax（Openrouter）"

    ```yaml
    model:
        model_name: "minimax/minimax-m2"
        model_class: openrouter
        model_kwargs:
            temperature: 0.0
    ```

## 模型类

我们通过不同的后端支持各种模型。
默认情况下（如果你只指定模型名称），我们会为你挑选最合适的后端。
这几乎总是默认为 `litellm`（Anthropic 模型是个特例，因为它们需要显式的缓存断点处理）。

不过，还有一些其他后端可供使用，你可以通过 `--model-class` 参数或智能体配置文件中的
`model.model_class` 键来指定（见上一节）。

例如：

=== "Openrouter 模型"

    ```bash
    mini -m "moonshotai/kimi-k2-0905" --model-class openrouter
    ```

    **或者：**在智能体配置文件中：

    ```yaml
    model:
        model_name: "moonshotai/kimi-k2-0905"
        model_class: openrouter
    ```

=== "Portkey 模型"

    ```bash
    mini -m "claude-sonnet-4-5-20250929" --model-class portkey
    ```

    **或者：**在智能体配置文件中：
    ```yaml
    model:
        model_name: "claude-sonnet-4-5-20250929"
        model_class: portkey
    ```


* **`litellm`**（[`LitellmModel`](../reference/models/litellm.md)）—— **默认且推荐**。通过 [litellm](https://github.com/BerriAI/litellm) 支持大多数模型。可用于 OpenAI、Anthropic、Google 等众多提供商。当模型名称包含 "anthropic"、"claude"、"sonnet" 或 "opus" 时，Anthropic 模型会自动获得缓存控制设置。

* **`litellm_response`**（[`LitellmResponseModel`](../reference/models/litellm_response_toolcall.md)）—— `LitellmModel` 的专用版本，使用 OpenAI 的 Responses API 和原生工具调用。适用于 GPT-5 之类的模型，并且是 GPT-5-codex 之类模型的必需项。它会跨轮次维护对话状态。

* **`openrouter`**（[`OpenRouterModel`](../reference/models/openrouter.md)）—— 直接集成 [OpenRouter](https://openrouter.ai/) API，通过单一端点访问各种模型。

* **`portkey`**（[`PortkeyModel`](../reference/models/portkey.md)）—— 集成 [Portkey](https://portkey.ai/)，以提供增强的可观测性、缓存和路由能力。注意它仍然使用 `litellm` 来计算成本。

此外，还有一些更“另类”的模型类可供使用：

* **`deterministic`**（[`DeterministicModel`](../reference/models/test_models.md)）—— 返回预定义的响应，用于测试和开发。
* **`minisweagent.models.extra.roulette.RouletteModel` 和 `minisweagent.models.extra.roulette.InterleavingModel`**（[`RouletteModel`](../reference/models/extra.md) 和 [`InterleavingModel`](../reference/models/extra.md)）—— 每次查询时随机选择或交替使用多个已配置的模型。更多细节请参见[这篇博客文章](https://www.swebench.com/SWE-bench/blog/2025/08/19/mini-roulette/)。

与后两者类似，你也可以指定指向自己自定义模型类的任意导入路径（即使它还不属于 mini-SWE-agent 包）。

--8<-- "docs/_footer.md"


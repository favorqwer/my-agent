# ❤️ 参与贡献

我们非常欢迎贡献！

## 可以帮忙的方向

- 文档、示例、教程等。具体来说，我们在寻找：
    - 这个库在真实场景中被使用的示例
    - 为 [cookbook](advanced/cookbook.md) 补充更多示例
- 支持更多模型（任何 `litellm` 开箱即用无法覆盖的模型）
- 支持更多环境与部署方式（例如将其作为 GitHub Action 运行等）
- 看看[议题列表](https://github.com/SWE-agent/mini-swe-agent/issues)，寻找标记为 `good-first-issue` 或 `help-wanted` 的议题（请先阅读下面的指南）

## 设计与架构

- `mini-swe-agent` 的目标是保持极简、可改造（hackable）以及高质量的代码。
- 要扩展功能，我们更倾向于为四个组件之一（参见 [cookbook](advanced/cookbook.md)）新增一个版本，而不是把现有组件变得更复杂。
- 组件应相对自包含，但如果存在可能被共享的工具函数，就添加一个 `utils` 文件夹（比如[这个](https://github.com/SWE-agent/mini-swe-agent/tree/main/src/minisweagent/models/utils)）。但要保持简单！
- 如果你的组件稍微特殊一些，就把它放进 `extra` 文件夹（比如[这个](https://github.com/SWE-agent/mini-swe-agent/tree/main/src/minisweagent/run/extra)）。
- 我们的目标用户是那些不介意修改一点代码（尤其是运行脚本）来实现自己需求的人。
- 因此，并非所有东西都需要通过配置文件来配置，但应该很容易编写一个运行脚本来使用它。
- 许多语言模型会写出非常冗长的代码——请把它清理干净！测试也是如此。它们仍应保持简洁、易读。
- 提交前请确保 `ruff check` 与 `pytest` 通过。

## 开发环境搭建

请务必按照 [quickstart.md](quickstart.md) 中的开发环境搭建说明操作。

之后你可以用 `pytest -n auto` 运行 `pytest`（这会在所有核心上并行运行测试以加速）。

{% include-markdown "_footer.md" %}

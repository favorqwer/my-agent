# 快速入门

!!! tip "安装方式"

    === "pip"

        使用 pip 在当前环境中安装 `mini`：

        ```bash
        pip install mini-swe-agent
        ```

        然后试试我们的命令行界面：

        ```bash
        mini  # CLI
        mini-extra  # 额外实用工具
        ```

    === "uv（隔离环境）"

        使用 `uv`/`uvx`（[安装说明](https://docs.astral.sh/uv/getting-started/installation/)）直接运行 `mini` CLI。
        如果你只对 CLI 感兴趣、不需要 Python 绑定，就用这种方式（`mini` 会被安装到一个匿名虚拟环境中）。

        快速安装并运行：

        ```bash
        uvx mini-swe-agent  # CLI
        uvx --from mini-swe-agent mini-extra  # 额外实用工具
        ```

        永久安装：

        ```bash
        uv tool install mini-swe-agent
        # 然后
        mini  # CLI
        mini-extra  # 额外实用工具
        ```

    === "pipx（隔离环境）"

        使用 pipx（[安装说明](https://pipx.pypa.io/stable/installation/)）直接运行 `mini` CLI。
        如果你只对 CLI 感兴趣、不需要 Python 绑定，就用这种方式（`mini` 会被安装到一个匿名虚拟环境中）。

        快速安装并运行：

        ```bash
        # CLI
        pipx run mini-swe-agent
        # 额外实用工具
        pipx run --spec mini-swe-agent mini-extra
        ```

        或者进行持久安装（推荐）：

        ```bash
        pipx install mini-swe-agent
        # 然后
        mini  # CLI
        mini-extra  # 额外实用工具
        ```

        如果命令无法立即生效，你可能需要运行 `pipx ensurepath`。

    === "从源码安装 / 开发模式"

        用于开发，或你想自定义智能体时：

        ```bash
        git clone https://github.com/SWE-agent/mini-swe-agent.git
        cd mini-swe-agent
        pip install -e .
        ```

        然后运行：

        ```bash
        mini  # CLI
        mini-extra  # 额外实用工具
        ```

        或者挑一个[运行脚本](https://github.com/SWE-agent/mini-swe-agent/tree/main/src/minisweagent/run)：

        ```bash
        python src/minisweagent/run/hello_world.py
        ```

        如果你打算参与贡献，还请安装开发依赖：

        ```bash
        pip install -e '.[dev]'
        ```

        要检查安装是否正常，可以在根目录下运行 `pytest -n auto`。
        这会并行运行所有测试（大约需要 3 分钟）。

!!! note "更新日志"

    最近的变更请查看 [GitHub 发行说明](https://github.com/SWE-agent/mini-swe-agent/releases)。

!!! info "要升级到 v2 吗？"

    请查看我们的 [v2 迁移指南](advanced/v2_migration.md)，了解所有变更以及如何更新你的代码。

!!! example "示例提示词"

    用这些示例提示词试试 mini-SWE-agent：

    - 在 `sudoku` 文件夹中用 python 实现一个数独求解器。确保代码库模块化，并用 pytest 做好充分测试。
    - 请对当前项目运行 pytest，找出失败的单元测试并帮我修复。务必确保最终方案经过测试。
    - 帮我通过添加简短的 docstring 和类型注解，为代码库补充文档和类型信息。

## 模型

!!! note "首次运行 `mini` 时应完成模型设置"

    * 如果你错过了设置向导，只需运行 `mini-extra config setup`
    * 更多信息请查看[模型设置快速入门](models/quickstart.md)。
    * 如果你想使用本地模型，请查看这份[指南](models/local_models.md)。

    提示：请务必在模型名称中包含提供商，例如 `anthropic/claude-...`。

!!! success "该用哪个模型？"

    对于大多数任务，我们推荐使用 `anthropic/claude-opus-4-6-20260205`。
    对于 openai 的模型，我们推荐使用 `openai/gpt-5.4` 或 `openai/gpt-5.4-mini`。
    你可以在我们的 [SWE-bench (bash-only)](https://swebench.com) 排行榜上查看不同模型的得分。

# 常见问题（FAQ）

## 通用

!!! question "mini-SWE-agent 能在我的系统上运行吗？"

    mini-SWE-agent 应该能在任何拥有 bash shell 的系统上运行，或者使用容器运行时（例如 docker、singularity、apptainer 等）来模拟 bash shell 的系统上运行。

??? question "我应该用 mini-SWE-agent 还是 swe-agent？"

    以下情况你应该使用 `mini-swe-agent`：

    - 你想要一个能在本地使用的快速命令行工具
    - 你想要一个控制流非常简单的智能体
    - 你想要更快、更简单、更稳定的沙箱与基准评测
    - 你在做微调（FT）或强化学习（RL），不想过拟合到某个特定的智能体脚手架

    以下情况你应该使用 `swe-agent`：

    - 你需要特定工具，或者想试验不同的工具
    - 你想试验不同的历史记录处理器（history processor）
    - 你想在不改动代码的情况下使用非常强大的 yaml 配置

    两者都能带给你：

    - 在 SWE-Bench 上的出色性能
    - 一个轨迹浏览器

??? question "`mini` 相比 `swe-agent` 简单在哪里？"

    `mini` 比 `swe-agent` 更简单，因为它：

    - 除 bash 之外没有任何工具 —— 它甚至不使用语言模型的工具调用接口。
      这意味着无论运行在什么环境里，你都不必安装任何东西。你需要的只是 `bash`。
    - 拥有完全线性的历史记录 —— 智能体的每一步只是向消息列表追加内容，仅此而已。
    - 使用 `subprocess.run` 执行动作 —— 每个动作完全独立（而不是保持一个有状态的 shell 会话运行）。
      相信我，这[避免了很多问题](#why-no-shell-session)。

??? question "mini-SWE-agent 有哪些局限？"

    mini-SWE-agent 可以以各种方式轻松扩展，以下所述均基于默认配置。
    从很高的 SWE-bench 得分也能看出，以下局限在实践中都不成问题。

    - 除 bash 之外没有其他工具
    - 动作是从三反引号代码块中解析出来的（而不是假定使用函数调用／工具调用格式）
    - 默认情况下，动作通过 `subprocess.run` 执行，也就是说每个动作都与之前的动作相互独立。
      （这意味着智能体无法切换目录或导出环境变量；不过环境变量可以按动作单独设置。）相信我，这[避免了很多问题](#why-no-shell-session)。

    如果你希望在这些方面拥有更多灵活性，可以改用 [SWE-agent](https://swe-agent.com/)。

??? question "全局配置存储在哪里？"

    全局配置存储在配置目录下的 `.env` 文件中。
    运行 `mini --help` 时会打印该位置。

    `.env` 文件是一个简单的键值文件，由 `dotenv` 库读取。


## 模型

!!! question "你们支持哪些模型？"

    目前，mini-SWE-agent 支持所有 [litellm](https://github.com/BerriAI/litellm) 或 [OpenRouter](https://openrouter.ai/) 支持的模型；
    如果 `litellm` 不支持某些模型，我们也愿意扩展 `models/` 目录以加入更多模型。

!!! question "如何为某个模型设置 API key？"

    API key 既可以存为环境变量（注意，除非你在 `~/.bashrc` 或类似文件中设置它们，否则环境变量不会持久化），
    也可以作为长期有效的键写入配置文件。

    要临时把 API key 设置为环境变量，可以使用以下命令：

    ```bash
    export OPENAI_API_KEY=sk-test123
    ```

    要把 API key 永久写入配置文件，可以使用以下命令：

    ```bash
    mini-extra config set OPENAI_API_KEY sk-test123
    ```

    或者，你也可以直接编辑配置目录下的 `.env` 文件
    （运行 `mini --help` 时会打印该位置）。

!!! question "如何设置默认模型？"

    默认模型以 `MSWEA_MODEL_NAME` 的形式存储在配置／环境中。
    要永久修改它：

    ```bash
    mini-extra config set MSWEA_MODEL_NAME anthropic/claude-sonnet-4-5-20250929
    ```

    或者，你也可以直接编辑配置目录下的 `.env` 文件
    （运行 `mini --help` 时会打印该位置）。

## 细节问题

??? question "为什么不需要保持 shell 会话运行是件大事？"
    <a name="why-no-shell-session"></a>

    到目前为止，大多数智能体都会保持一个持续运行的 shell 会话。智能体的每个动作都在这个会话中执行。
    然而，这远非易事：

    1. 命令何时结束并不明显。本质上你只是把输入粘贴进 shell 会话然后按回车——但什么时候才算读完输出呢？
       我们尝试过各种启发式方法（监视 PID、等待 shell 回到提示符等），但它们都不可靠。
       `mini` 智能体完全不需要这些！
    2. 语言模型给出的特别糟糕的命令可能会杀死 shell 会话。那之后怎么办呢？
    3. 中断 shell 会话中正在运行的命令也可能弄乱 shell 本身，尤其是会干扰你之后想提取的所有输出。

    `mini` 则不同：它没有持续运行的 shell 会话。每个动作都作为子进程执行，这意味着
    每个动作都与之前的动作相互独立（它实际上就是一次 `subprocess.run`／`os.system`／`docker exec` 调用）。

    这意味着智能体甚至无法切换目录或导出环境变量。
    但你并不需要这些！你总可以在每个动作前加上 `cd /path/to/project` 或 `export FOO=bar`
    （事实上，有些语言模型，比如 Claude，即使你不要求它们也会这么做）。

{% include-markdown "_footer.md" %}

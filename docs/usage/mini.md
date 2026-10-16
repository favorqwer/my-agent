# `mini`

!!! abstract "概览"

    * `mini` 是一个 REPL 风格的交互式命令行界面，用于在本地环境中使用 mini-SWE-agent（相对于需要沙箱或大规模批处理的工作流而言）。

<figure markdown="span">
  <div class="gif-container gif-container-styled" data-glightbox-disabled>
    <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/mini.png?raw=true"
         data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/mini.gif?raw=true"
         alt="mini" data-glightbox="false" width="600" />
  </div>
</figure>


## 命令行选项

常用开关：

- `-h`/`--help`：显示帮助
- `-t`/`--task`：指定要运行的任务（否则会提示你输入）
- `-c`/`--config`：指定要使用的配置文件，否则我们会使用 [`mini.yaml`](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/mini.yaml) 或 `MSWEA_MINI_CONFIG_PATH` 环境变量指定的配置（参见[全局配置](../advanced/global_configuration.md)）。
  只写出配置文件名即可，例如 `-c mini.yaml`（配置文件如何解析请参见[全局配置](../advanced/global_configuration.md)）。
- `-m`/`--model`：指定要使用的模型，否则我们会使用 `MSWEA_MODEL_NAME` 环境变量指定的模型（参见[全局配置](../advanced/global_configuration.md)）
- `-y`/`--yolo`：以 `yolo` 模式启动（见下文）

## 运行模式

`mini` 提供三种不同的运行模式：

- `confirm`（`/c`）：语言模型提出一个动作，用户被提示确认（按回车）或拒绝（输入拒绝理由）
- `yolo`（`/y`）：语言模型给出的动作立即执行，无需确认
- `human`（`/u`）：由用户接管，自行输入并执行命令

你可以在智能体等待输入的任何时候输入 `/c`、`/y`、`/u` 命令来切换模式。
你也可以随时按 `Ctrl+C` 中断智能体，从而切换模式。

`mini` 默认以 `confirm` 模式启动。要以 `yolo` 模式启动，可以在命令行中加上 `-y`/`--yolo`。

## 其他提示

- `mini` 会把上次运行的完整历史记录保存到你的全局配置目录中。
  该目录的路径会在你启动 `mini` 时打印出来。

## 实现

??? note "默认配置"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/mini.yaml)

    ```yaml
    --8<-- "src/minisweagent/config/mini.yaml"
    ```

??? note "运行脚本"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/mini.py)
    - [API 参考](../reference/run/mini.md)

    ```python
    --8<-- "src/minisweagent/run/mini.py"
    ```

??? note "智能体类"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/agents/interactive.py)
    - [API 参考](../reference/agents/interactive.md)

    ```python
    --8<-- "src/minisweagent/agents/interactive.py"
    ```

{% include-markdown "../_footer.md" %}

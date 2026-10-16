# `mini-extra config`

!!! abstract "概览"

    * `mini-extra config` 是用于管理全局配置文件的实用工具。
    * 可以用 `mini-extra config` 或 `mini-e config` 快速启动它。

## 命令

### `setup`

交互式设置向导，帮助你配置默认模型和 API key。

```bash
mini-extra config setup
```

它会提示你输入：

1. 你的默认模型（例如 `anthropic/claude-sonnet-4-5-20250929`）
2. 你的 API key 名称和值（例如 `ANTHROPIC_API_KEY`）

### `set`

在全局配置文件中设置指定的键。

```bash
# 示例：设置默认模型
mini-extra config set MSWEA_MODEL_NAME anthropic/claude-sonnet-4-5-20250929
# 或交互式设置
mini-extra config set
```

### `unset`

从全局配置文件中删除某个键。

```bash
mini-extra config unset MSWEA_MODEL_NAME
```

### `edit`

用默认编辑器打开全局配置文件（使用 `$EDITOR` 或 `nano`）。

```bash
mini-extra config edit
```

## 配置键

更多配置选项请参见[全局配置](../advanced/global_configuration.md)。

## 实现

??? note "运行脚本"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/utilities/config.py)
    - [API 参考](../reference/run/config.md)

    ```python
    --8<-- "src/minisweagent/run/utilities/config.py"
    ```

{% include-markdown "../_footer.md" %}

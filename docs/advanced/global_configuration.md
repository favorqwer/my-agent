# 全局配置

!!! abstract "配置 mini"

    * 本指南介绍如何配置 `mini` 智能体的全局设置（API key、默认模型等）。
      基本上就是任何以环境变量或类似方式设置的内容。
    * 你应该已经熟悉[快速入门指南](../quickstart.md)了。
    * 更多与智能体相关的设置请参见[Yaml 配置文件指南](yaml_configuration.md)。

!!! tip "设置模型"

    模型的设置也在[快速入门指南](../quickstart.md)中有所介绍。

## 设置全局配置

所有全局配置既可以设为环境变量，也可以写在 `.env` 文件中（确切位置会在你运行 `mini` 时打印出来）。
环境变量的优先级高于 `.env` 文件中设置的变量。

我们提供了几个辅助函数来更新全局配置。

例如，要设置默认模型和 API key，你可以运行：

```bash
mini-extra config setup
```

或者更新特定设置：

```
mini-extra config set KEY VALUE
# 例如：
mini-extra config set MSWEA_MODEL_NAME "anthropic/claude-sonnet-4-5-20250929"
mini-extra config set ANTHROPIC_API_KEY "sk-..."
```

或者删除某个键：

```bash
mini-extra config unset KEY
# 例如：
mini-extra config unset ANTHROPIC_API_KEY
```

你也可以直接编辑 `.env` 文件，我们为此也提供了辅助函数：

```bash
mini-extra config edit
```

设置环境变量（推荐用于临时实验或存放 API key）：

```bash
export KEY="value"
# windows:
setx KEY "value"
```

## 模型、密钥、成本

!!! tip "另请参阅"

    请先阅读[快速入门指南](../quickstart.md)——它已经涵盖了这里的大部分内容。

```bash
# 默认模型名称
# （默认值：未设置）
MSWEA_MODEL_NAME="anthropic/claude-sonnet-4-5-20250929"
```

要忽略成本追踪检查产生的错误（例如使用免费模型时），请设置：

```bash
# 注意：这可能导致支出失控！
MSWEA_COST_TRACKING="ignore_errors"
```

要向 litellm 注册额外模型（详见[本地模型](../models/local_models.md)），你可以在智能体文件中指定路径，或者设置

```bash
LITELLM_MODEL_REGISTRY_PATH="/path/to/your/model/registry.json"
```

全局成本上限：

```bash
# 模型调用次数的全局上限（0 = 不限制）
# （默认值：0）
MSWEA_GLOBAL_CALL_LIMIT="100"

# 以美元计的全局成本上限（0 = 不限制）
# （默认值：0）
MSWEA_GLOBAL_COST_LIMIT="10.00"

# 模型 API 调用的重试次数
# （默认值：10）
MSWEA_MODEL_RETRY_STOP_AFTER_ATTEMPT="10"
```

## 默认配置文件

```bash
# 在内置配置之外，为智能体配置文件设置自定义目录
# 这样就能通过名称来指定它们
MSWEA_CONFIG_DIR="/path/to/your/own/config/dir"

# mini 运行脚本的配置路径
# （默认值：package_dir / "config" / "mini.yaml"）
MSWEA_MINI_CONFIG_PATH="/path/to/your/own/config"

# 轨迹 inspector 的自定义样式路径
# （默认值：package_dir / "config" / "inspector.tcss"）
MSWEA_INSPECTOR_STYLE_PATH="/path/to/your/inspector/style.tcss"
```

### 环境相关设置

```bash
# docker 可执行文件的路径／名称
# （默认值："docker"）
MSWEA_DOCKER_EXECUTABLE="docker"
```

### 其他设置

```bash
# 自定义全局配置目录（存放 .env 与运行历史）
# （默认值：由 platformdirs 决定，Windows 上是 %LOCALAPPDATA%\mini-swe-agent\mini-swe-agent）
MSWEA_GLOBAL_CONFIG_DIR="/path/to/your/config/dir"

# 设置后不再打印启动时的版本号与迁移提示（适合脚本、CI）
MSWEA_SILENT_STARTUP="1"

# 标记已完成首次运行向导，由 mini-extra config setup 自动写入，一般不需要手动设置
MSWEA_CONFIGURED="true"
```

## 默认运行文件

```bash
# 主 CLI 的默认运行脚本入口点
# （默认值："minisweagent.run.mini"）
MSWEA_DEFAULT_RUN="minisweagent.run.mini"
```

{% include-markdown "_footer.md" %}

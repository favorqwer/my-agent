# 配置

* `mini.yaml` - `mini`／`agents/interactive.py` 智能体的默认配置（使用工具调用）。
* `mini_textbased.yaml` - 同上，但改为从 markdown 代码块中解析命令（不使用工具调用）。
* `default.yaml` - `default.py` 智能体的默认配置。
* `inspector.tcss` - 轨迹 inspector 的样式表。

## 基准评测

* `benchmarks/swebench.yaml` - `run/benchmarks/swebench.py` 入口点的配置（使用工具调用）。
* `benchmarks/swebench_backticks.yaml` - 同上，但使用 markdown 代码块解析命令。
* `benchmarks/swebench_xml.yaml` - 同上，但使用 XML 标签解析命令。
* `benchmarks/programbench.yaml` - `run/benchmarks/programbench.py` 入口点的配置。

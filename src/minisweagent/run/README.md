# 入口点／运行脚本

## 在本地运行（即不使用沙箱）

* `hello_world.py` - 如何使用 `default.py` 智能体的极简示例。
* `mini.py` - 使用 `interactive.py` 智能体，也就是 `mini` 命令。

## 基准评测

* `benchmarks/swebench.py` - 在 SWE-bench 上批量评测。
* `benchmarks/swebench_single.py` - 运行单个 SWE-bench 实例（便于调试）。
* `benchmarks/programbench.py` - 在 ProgramBench 上批量运行。
* `benchmarks/utils/` - 批处理共用工具（进度显示、实例筛选等）。

## 工具命令（`mini-extra` 的子命令）

* `utilities/mini_extra.py` - `mini-extra` 的中央入口。
* `utilities/config.py` - 管理全局配置文件（`mini-extra config`）。
* `utilities/inspector.py` - 浏览轨迹文件（`mini-extra inspector`）。

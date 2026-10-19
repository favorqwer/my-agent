# ProgramBench

!!! abstract "概览"

    * `mini-extra programbench` 以批处理模式在所有 [ProgramBench](https://github.com/facebookresearch/programbench) 任务实例上运行智能体。
    * 输出可直接与 `programbench eval` 兼容。
    * ProgramBench 是一个逆向工程基准：智能体被放入一个包含已编译二进制的容器中，
      必须产出一份全新的源代码库，复现该二进制的行为。
      通过针对重新构建出的可执行文件运行测试来为解法打分。

## 用法

!!! warning "Docker 容器的可用性"

    ProgramBench 的 docker 容器（发布为 `programbench/<instance>:task_cleanroom`）
    假定为 x86 Linux 架构；在其他架构上你可能无法运行它们。


!!! warning "请先安装 ``programbench``"

    该运行器会导入 ``programbench`` 来发现任务实例。运行前请先安装它：
    ``pip install programbench``（或 ``uvx programbench``）。


!!! tip "快速入门"

    ```bash
    mini-extra programbench --help
    # 或者
    python src/minisweagent/run/benchmarks/programbench.py --help
    # 示例：
    mini-extra programbench \
        --model anthropic/claude-sonnet-4-5-20250929 \
        --workers 4
    ```

    基本参数：

    - `-o`、`--output` - 输出目录（默认：带时间戳的 `programbench_results_<ts>/`）
    - `-m`、`--model` - 要使用的模型
    - `-c`、`--config` - 配置文件路径（默认：`config` 目录下的 `programbench.yaml`）
    - `-w`、`--workers` - 并行处理的工作线程数（默认：`1`）

    数据选择参数：

    - `--slice` - 切片规格（例如 `0:5` 表示前 5 个实例）
    - `--filter` - 用正则表达式过滤实例 ID
    - `--shuffle` - 打乱实例顺序（默认：`False`）
    - `--redo-existing` - 重做已存在的实例（默认：`False`）

    高级参数：

    - `--environment-class` - 要使用的环境类型（推荐：`docker`）
    - `--model-class` - 要使用的模型类

    docker 镜像 tag 硬编码为 ``:task_cleanroom``（一个不含构建产物的镜像）。

!!! tip "输出结构"

    每个实例会在 ``<output>/<instance_id>/`` 下写入两个文件：

    - ``submission.tar.gz`` - 智能体的工作区（容器内 ``/workspace`` 的 gzip 压缩 tar 包）
    - ``<instance_id>.traj.json`` - 完整的智能体轨迹

    该目录可以直接传给 ``programbench eval``：

    ```bash
    programbench eval <output>/
    ```

!!! tip "网络隔离"

    默认配置会以 ``--network none`` 启动每个容器。因此智能体
    无法从互联网安装依赖、克隆 GitHub 仓库或下载源码
    tarball —— 整个逆向工程过程都必须离线进行，只能依赖
    所提供的二进制及其附带的文档。如果你需要允许特定的主机，请在配置中覆盖
    ``environment.run_args``。

## 常见问题

参见 [SWE-bench 常见问题](swebench.md#常见问题) —— 其中大部分条目（成本上限、KeyboardInterrupt 行为、
docker 故障排查）同样适用于 ProgramBench。

## 实现

??? note "默认配置"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/benchmarks/programbench.yaml)

    ```yaml
    --8<-- "src/minisweagent/config/benchmarks/programbench.yaml"
    ```

??? note "`programbench.py` 运行脚本"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/benchmarks/programbench.py)
    - [API 参考](../reference/run/programbench.md)

    ```python
    --8<-- "src/minisweagent/run/benchmarks/programbench.py"
    ```

{% include-markdown "../_footer.md" %}

# SWE-bench

!!! abstract "概览"

    * 我们提供了两个脚本来运行 [SWE-bench](https://www.swebench.com/) 基准。
    * `mini-extra swebench` 以批处理模式运行所有任务实例。
    * `mini-extra swebench-single` 以交互方式运行单个任务实例（便于调试）。
    * 你也可以查看这些运行脚本，了解如何构建自己的批处理流水线。

<figure markdown="span">
  <div class="gif-container gif-container-styled" data-glightbox-disabled>
    <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/swebench.png?raw=true"
         data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/swebench.gif?raw=true"
         alt="swebench" data-glightbox="false" width="600" />
  </div>
</figure>

## 用法

!!! warning "Docker 容器的可用性"

    用于 Linux 的 docker 容器假定为 x86 Linux 架构；
    在其他架构上你可能无法运行它们。


!!! tip "快速入门"

    我们提供两个不同的脚本：`swebench` 和 `swebench-single`：

    === "批处理模式"

        批处理模式会并行运行所有任务实例。

        ```bash
        mini-extra swebench --help
        # 或者
        python src/minisweagent/run/benchmarks/swebench.py --help
        # 示例：
        mini-extra swebench \
            --model anthropic/claude-sonnet-4-5-20250929 \
            --subset verified \
            --split test \
            --workers 4
        ```

        基本参数：

        - `-o`、`--output` - 输出目录
        - `-m`、`--model` - 要使用的模型
        - `-c`、`--config` - 配置文件路径（默认：`config` 目录下的 `swebench.yaml`）
        - `-w`、`--workers` - 并行处理的工作线程数（默认：`1`）

        数据选择参数：

        - `--subset` - 要使用的 SWEBench 子集或数据集路径（默认：`lite`）
        - `--split` - 数据集划分（默认：`dev`）
        - `--slice` - 切片规格（例如 '0:5' 表示前 5 个实例）
        - `--filter` - 用正则表达式过滤实例 ID
        - `--shuffle` - 打乱实例顺序（默认：`False`）
        - `--redo-existing` - 重做已存在的实例（默认：`False`）

        高级参数：

        - `--environment-class` - 要使用的环境类型（推荐：`docker` 或 `singularity`）

    === "单个实例（用于调试）"

        单实例模式以交互方式运行单个任务实例。它用于调试，因此与上面的批处理模式命令不同，它不会生成 preds.json 文件。

        ```bash
        mini-extra swebench-single --help
        # 或者
        python src/minisweagent/run/benchmarks/swebench_single.py --help
        # 示例：
        mini-extra swebench-single \
            --subset verified \
            --split test \
            --model anthropic/claude-sonnet-4-5-20250929 \
            -i sympy__sympy-15599
        # 或者
        mini-extra swebench-single \
            --subset verified \
            --split test \
            -m anthropic/claude-sonnet-4-5-20250929 \
            -i 0  # 实例索引
        ```

        注意：如果你希望在退出时不弹出确认提示，直接运行脚本，
        请加上 `--exit-immediately` 参数。

        基本参数：

        - `-m`、`--model` - 要使用的模型
        - `-c`、`--config` - 配置文件路径（默认：`config` 目录下的 `swebench.yaml`）
        - `-o`、`--output` - 输出轨迹文件（默认：保存到全局配置目录）

        数据选择参数：

        - `--subset` - 要使用的 SWEBench 子集或数据集路径（默认：`lite`）
        - `--split` - 数据集划分（默认：`dev`）
        - `-i`、`--instance` - SWE-Bench 实例 ID（默认：`0`）

        高级参数：

        - `--environment-class` - 要使用的环境类型（推荐：`docker` 或 `singularity`）
        - `--exit-immediately` - 当智能体想要结束时立即退出，而不是弹出提示（默认：`False`）

!!! tip "在 SWE-bench 上评测"

    你有两种方式在 SWE-bench 上评测：我们的免费云端评测，或者 SWE-bench CLI。

    === "云端评测"

        你可以使用 [sb-cli](https://www.swebench.com/sb-cli/) 进行极其快速的云端评测
        （而且是免费的！）。安装它并获取 token 之后，只需运行：

        ```bash
        sb-cli submit swe-bench_verified test --predictions_path preds.json --run_id some-id-for-your-run
        ```

        通常你会在 20 分钟内拿到结果（这不取决于你运行了多少实例，
        而取决于 SWE-bench 中评测最慢的那个实例）。

    === "本地评测"

        你也可以使用本地安装的 [SWE-bench](https://github.com/SWE-bench/SWE-bench)
        进行评测：

        ```bash
        python -m swebench.harness.run_evaluation \
            --dataset_name princeton-nlp/SWE-bench_Verified \
            --predictions_path preds.jsonl \
            --max_workers <num_workers> \
            --run_id <run_id>
        ```

## 常见问题

> 我可以设置全局成本上限吗？

可以，你可以通过 `MSWEA_GLOBAL_CALL_LIMIT` 和 `MSWEA_GLOBAL_COST_LIMIT` 环境变量／全局配置来设置全局成本上限。
更多细节请参见[全局配置](../advanced/global_configuration.md)。

> 当我用 KeyboardInterrupt 中止时，未完成的任务会怎样？

轨迹只会在完成时保存，所以大多数情况下，你下次重新运行脚本即可完成任务。
不过，你仍应检查 `preds.json` 中是否有 `KeyboardInterrupt`，以防某些任务被中止但已保存。

> 即使我删除了轨迹，某些任务还是卡住了。

已完成的实例是从 `preds.json` 推断出来的。请从该文件中删除对应的条目。

> 如何在不同数据集上运行？

只要它遵循 SWE-bench 格式，你就可以用 `--subset /path/to/your/dataset` 在自定义数据集上运行。
该数据集需要能通过 `datasets.load_dataset(path, split=split)` 加载。

> 有些进度运行器长时间卡在“initializing task”／超时

它们可能正在拉取 docker 容器——下次运行应该会立刻开始。
如果你看到因为 `docker pull` 操作导致的超时，可能想把 `environment.pull_timeout`
从默认的 `120`（秒）调大一些。

> 我遇到了一些 docker 问题

试着手动运行那条 docker 命令，看看发生了什么（它应该会打印到控制台上）。
用 `docker ps` 确认它正在运行，并确认你可以用 `docker exec -it <container-id> ls` 得到一些输出。

> 我的 HPC 集群上没有 Docker。

你可以在[智能体配置文件](../advanced/yaml_configuration.md)中把 `environment.environment_class` 设为 `singularity`，
从而使用 singularity/apptainer 后端；
或者在命令行中指定 `--environment-class singularity`

> 我可以在环境中运行启动命令吗？

可以，你可以使用 `run.env_startup_command` 配置项，在智能体启动前于环境中运行一条命令。
例如：

```yaml
run:
  env_startup_command: "apt-get update && apt-get install -y python3-pip"
```

该命令会使用 `jinja2`，把实例的变量作为模板变量进行渲染。
例如，你可以这样写：

```yaml
run:
  env_startup_command: "git clone {{ repo_url }} . --force"
```

在使用 [`bubblewrap`](../reference/environments/bubblewrap.md) 之类的环境运行时，这可能特别有用。

> SWE-bench 可以使用什么环境？

更多细节请参见[这份指南](../advanced/environments.md)。

## 实现

??? note "默认配置"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/benchmarks/swebench.yaml)

    ```yaml
    --8<-- "src/minisweagent/config/benchmarks/swebench.yaml"
    ```

??? note "`swebench.py` 运行脚本"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/benchmarks/swebench.py)
    - [API 参考](../reference/run/swebench.md)

    ```python
    --8<-- "src/minisweagent/run/benchmarks/swebench.py"
    ```

??? note "`swebench_single.py` 运行脚本"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/benchmarks/swebench_single.py)
    - [API 参考](../reference/run/swebench_single.md)

    ```python
    --8<-- "src/minisweagent/run/benchmarks/swebench_single.py"
    ```

{% include-markdown "../_footer.md" %}

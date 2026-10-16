# 环境类

!!! abstract "环境类"

    * 环境负责执行语言模型／智能体生成的代码。
    * 我们提供了多种类，既可以直接在宿主机上执行代码，也可以在容器中执行（例如 Docker、Singularity 等）。

我们支持多种通过不同后端执行代码的环境。

如果你运行 [`mini`](../usage/mini.md) CLI，默认会在 `local` 环境中运行。

不过，特别是在 SWE-bench 上评测时，你会希望运行在隔离环境中，因此我们提供了多种可用的“后端”。

你可以通过 `--environment-class` 参数或[智能体配置文件](yaml_configuration.md)中的
`environment.environment_class` 键来指定环境类。

* **`local`**（[`LocalEnvironment`](../reference/environments/local.md)）。使用 `subprocess.run` 直接在宿主机上执行命令。没有隔离。可以直接在你当前的 Python 环境中工作。

* **`docker`**（[`DockerEnvironment`](../reference/environments/docker.md)）。使用 `docker exec` 执行命令。

* **`singularity`**（[`SingularityEnvironment`](../reference/environments/singularity.md)）—— 在 Singularity/Apptainer 容器中执行命令。在无法使用 Docker 的 HPC 环境中，是不错的 Docker 替代方案。

此外，还有一些更专用的环境类可供使用：

* **`swerex_docker`**（[`SwerexDockerEnvironment`](../reference/environments/swerex_docker.md)）—— 通过 [SWE-ReX](https://github.com/swe-agent/swe-rex) 进行 Docker 执行

* **`swerex_modal`**（[`SwerexModalEnvironment`](../reference/environments/swerex_modal.md)）—— 通过 [SWE-ReX](https://github.com/swe-agent/swe-rex) 在 [Modal](https://modal.com) 云上执行。适合通过远程执行大规模训练编码智能体。

* **`bubblewrap`**（[`BubblewrapEnvironment`](../reference/environments/bubblewrap.md)）—— **仅限 Linux**。使用 [bubblewrap](https://github.com/containers/bubblewrap) 实现轻量、非特权沙箱。实验性功能。

* **`contree`**（[`ContreeEnvironment`](../reference/environments/contree.md)）—— 使用 [ConTree](https://contree.dev/) 实现安全的代码执行沙箱。这是一个为智能体打造、支持类 Git 执行的平台。

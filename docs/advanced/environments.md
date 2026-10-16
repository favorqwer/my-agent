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

## Windows 上的行为

系统提示词假定了一个 POSIX shell（bash），因此在 Windows 上，`local` 环境默认使用 **Git Bash** 执行命令。
探测顺序如下：

1. 配置文件中显式设置的 `environment.interpreter`（例如 `["cmd", "/c"]` 可以强制使用 `cmd.exe`）；
2. `C:\Program Files\Git\bin\bash.exe`、`C:\Program Files (x86)\Git\bin\bash.exe`、`%LOCALAPPDATA%\Programs\Git\bin\bash.exe`；
3. `PATH` 中的 `bash.exe`；
4. 以上都找不到时，回退到 `cmd.exe`。

WSL 自带的 `bash.exe`（位于 `System32` 或 `WindowsApps` 下的垫片）会被刻意跳过，因为它会在 WSL 的文件系统视图（`/mnt/c/...`）中执行命令，而不是 Windows 文件系统。
使用 WSL 的 bash 时，请显式指定路径，例如 `interpreter: ["C:\\Windows\\System32\\bash.exe", "-c"]`。需要留意以下差异：

- **路径形式**：bash 报告的是 POSIX 风格路径，例如 `C:\Users\me\project` 会显示为 `/c/Users/me/project`，临时目录甚至会被映射成 `/tmp/...`。在 bash 内部这些路径都可以正常使用。
- **输出编码**：Windows 程序默认按本地代码页输出（中文系统是 cp936），我们会强制子进程使用 UTF-8（`PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`），并在解码时优先尝试 UTF-8、失败后回退到平台编码，以避免中文乱码。你也可以用 `environment.encoding` 显式指定编码。
- **超时**：Windows 没有进程组，超时时会使用 `taskkill /F /T` 杀掉整棵进程树，避免留下孤儿进程。
- **交互界面**：`mini` 的交互界面基于 prompt_toolkit，需要真正的 Windows 控制台。建议在 PowerShell 或 Windows Terminal 中运行；在 Git Bash（mintty）等终端里会自动退化为普通的 `input()` 提示（多行输入用空行提交）。
- **基准评测**：SWE-bench / ProgramBench 需要 docker（Windows 上建议 Docker Desktop + WSL2）；`bubblewrap` 与 `singularity` 仅支持 Linux。

如果你希望完全使用 Windows 原生的 `cmd.exe`，可以这样配置：

```yaml
environment:
  interpreter: ["cmd", "/c"]
```

对应的 `local` 环境配置项分别为 `interpreter`（执行命令的解释器）与 `encoding`（输出编码）。

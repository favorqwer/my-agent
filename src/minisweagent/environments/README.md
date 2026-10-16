# 环境

* `local.py` - 用 `subprocess.run` 执行代码（Windows 上默认改用 Git Bash，详见[文档](https://mini-swe-agent.com/latest/advanced/environments/)）
* `docker.py` - 在 docker 或 podman 容器中执行代码
* `singularity.py` - 在 singularity 或 apptainer 容器中执行代码

## 额外组件

* `extra/swerex_docker.py` - 通过 [swerex](https://github.com/swe-agent/swe-rex) 用 docker 执行环境
* `extra/swerex_modal.py` - 通过 [swerex](https://github.com/swe-agent/swe-rex) 在 [Modal](https://modal.com) 上执行环境
* `extra/bubblewrap.py` - 用 [bubblewrap](https://github.com/containers/bubblewrap) 执行环境（仅 Linux）
* `extra/contree.py` - 在 [ConTree](https://contree.dev) 沙箱中执行环境

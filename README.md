<div align="center">
<a href="https://mini-swe-agent.com/latest/"><img src="https://github.com/SWE-agent/mini-swe-agent/raw/main/docs/assets/mini-swe-agent-banner.svg" alt="mini-swe-agent banner" style="height: 7em"/></a>
</div>

# 极简的 AI 软件工程智能体

📣 [mini-swe-agent 现已驱动 Ramp SWE-Bench](https://labs.ramp.com/swebench)<br/>
📣 [mini-swe-agent 在 DeepSWE 上击败了 Claude Code 和 Codex](https://deepswe.datacurve.ai/blog#evaluation-harness)<br/>
📣 [在我们的全新且极具挑战性的基准 ProgramBench 上运行 mini-swe-agent](https://mini-swe-agent.com/latest/usage/programbench/)<br/>
📣 [关于构建极简 AI 智能体的新教程](https://minimal-agent.com/)

[![Docs](https://img.shields.io/badge/Docs-green?style=for-the-badge&logo=materialformkdocs&logoColor=white)](https://mini-swe-agent.com/latest/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/swe-bench/shared_invite/zt-36pj9bu5s-o3_yXPZbaH2wVnxnss1EkQ)
[![PyPI - Version](https://img.shields.io/pypi/v/mini-swe-agent?style=for-the-badge&logo=python&logoColor=white&labelColor=black&color=deeppink)](https://pypi.org/project/mini-swe-agent/)

> [!WARNING]
> 这是 **mini-swe-agent v2**。请阅读[迁移指南](https://mini-swe-agent.com/latest/advanced/v2_migration/)。如需上一版本，请查看 [v1 分支](https://github.com/SWE-agent/mini-swe-agent/tree/v1)。

2024 年，我们构建了 [SWE-bench](https://github.com/swe-bench/SWE-bench) 和 [SWE-agent](https://github.com/swe-agent/swe-agent)，并助力掀起了编码智能体的革命。

现在我们要问：**如果我们的智能体简单 100 倍，但效果几乎一样好，会怎样？**

`mini` 具有如下特点：

- **被广泛采用**：Meta、NVIDIA、Essential AI、IBM、Nebius、Anyscale、普林斯顿大学、斯坦福大学等众多机构都在使用。
- **极简**：[智能体类](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py)只有约 100 行 Python（[环境](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py)、
[模型](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)和[运行脚本](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/hello_world.py)稍多一点）——没有任何花哨的依赖！
- **性能出众**：在 [SWE-bench verified 基准](https://www.swebench.com/)上得分超过 74%；启动速度远快于 Claude Code
- **易于部署**：支持**本地环境**、**docker/podman**、**singularity/apptainer**、**bubblewrap**、**contree** 等
- **兼容性强**：通过 **litellm**、**openrouter**、**portkey** 等支持所有模型。支持 `/completion` 和 `/response` 端点、交错思考（interleaved thinking）等
- 由打造 [SWE-bench](https://swebench.com)、[SWE-agent](https://swe-agent.com) 等项目的普林斯顿与斯坦福团队构建
- **经过测试**：[![Codecov](https://img.shields.io/codecov/c/github/swe-agent/mini-swe-agent?style=flat-square)](https://codecov.io/gh/SWE-agent/mini-swe-agent)

<details>

<summary>更多动机（研究视角）</summary>

[SWE-agent](https://swe-agent.com/latest/) 在 2024 年开启了 AI 智能体的发展之路。当时，我们非常强调为智能体提供工具和特殊接口。
然而一年之后，随着语言模型能力的提升，构建一个有用的智能体已经完全不需要这些了！
事实上，`mini` 智能体

- **除 bash 之外没有任何工具** —— 它甚至不需要使用语言模型的工具调用（tool-calling）接口。
  这意味着你可以用任何模型运行它。在沙箱环境中运行时，你也不需要操心安装任何包——它只需要 bash。
- **拥有完全线性的历史记录** —— 智能体的每一步只是向消息列表追加内容，仅此而已。
  因此，轨迹（trajectory）与传给语言模型的消息之间没有任何差别。
  非常适合调试和微调。
- **使用 `subprocess.run` 执行动作** —— 每个动作完全独立（而不是保持一个有状态的 shell 会话运行）。
  这使得在沙箱中执行动作变得非常简单（实际上只需把 `subprocess.run` 换成 `docker exec`），并且可以轻松扩展。
  说真的，这[非常重要](https://mini-swe-agent.com/latest/faq/#why-no-shell-session)，相信我。

这使它非常适合作为基线系统，也适合作为一个把语言模型（而非智能体脚手架）置于关注中心的系统。
你可以在 [SWE-bench (bash only)](https://www.swebench.com/) 排行榜上看到结果，该榜单评估了不同语言模型在 `mini` 上的表现。

</details>

<details>
<summary>更多动机（工具视角）</summary>

有些智能体是过拟合的研究产物，另一些则是重度依赖 UI 的前端巨兽。

`mini` 智能体想成为一个可供随意改造的工具，而不是一个黑盒。

- **足够简单**，一眼就能看懂
- **足够方便**，可以在日常工作流中使用
- **足够灵活**，便于扩展

与其他智能体（包括我们自己的 [swe-agent](https://swe-agent.com/latest/)）不同，它要激进地简单得多，因为它：

- **除 bash 之外没有任何工具** —— 它甚至不需要使用语言模型的工具调用接口。
  我们不为智能体可能想做的每一件具体事情实现自定义工具，而是完全专注于让语言模型充分发挥 shell 的全部潜力。
  想让它做某件具体的事，比如开一个 PR？
  直接告诉语言模型自己去搞定，而不是花时间在智能体里实现它。
- **使用 `subprocess.run` 执行动作** —— 每个动作完全独立（而不是保持一个有状态的 shell 会话运行）。
  这对智能体的稳定性[非常重要](https://mini-swe-agent.com/latest/faq/#why-no-shell-session)，相信我。
- **拥有完全线性的历史记录** —— 智能体的每一步只是向下一步传给语言模型的消息中追加内容，仅此而已。
  这对于调试和理解语言模型收到的提示非常有帮助。

</details>

<details>
<summary>我应该用 SWE-agent 还是 mini-SWE-agent？</summary>

你应该把 `mini-swe-agent` 当作默认选择。
尤其是当你符合以下情况时，应该使用 `mini-swe-agent`：

- 你想要一个能在本地使用的快速命令行工具
- 你想要一个控制流非常简单的智能体
- 你想要更快、更简单、更稳定的沙箱与基准评测
- 你在做微调（FT）或强化学习（RL），不想过拟合到某个特定的智能体脚手架

而以下情况你应该使用 `swe-agent`：

- 你想试验不同的工具集合，且每种工具都有自己的接口
- 你想试验不同的历史记录处理器（history processor）

两者都能带给你：

- 在 SWE-Bench 上的出色性能
- 一个轨迹浏览器

</details>

<table>
<tr>
<td width="50%">
<a href="https://mini-swe-agent.com/latest/usage/mini/"><strong>CLI</strong></a> (<code>mini</code>)
</td>
<td>
<a href="https://mini-swe-agent.com/latest/usage/swebench/"><strong>批量推理</strong></a>
</td>
</tr>
<tr>
<td width="50%">

![mini](https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/mini.gif?raw=true)

</td>
<td>

![swebench](https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/swebench.gif?raw=true)

</td>
</tr>
<tr>
<td>
<a href="https://mini-swe-agent.com/latest/usage/inspector/"><strong>轨迹浏览器</strong></a>
</td>
<td>
<a href="https://mini-swe-agent.com/latest/advanced/cookbook/"><strong>Python 绑定</strong></a>
</td>
</tr>
<tr>
<td>

![inspector](https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/inspector.gif?raw=true)

</td>
<td>

```python
agent = DefaultAgent(
    LitellmModel(model_name=...),
    LocalEnvironment(),
)
agent.run("Write a sudoku game")
```

</td>
</tr>
</table>

## 让我们开始吧！

**方式 1：** 如果你只想试用 CLI（包会安装在匿名虚拟环境中）

```bash
pip install uv && uvx mini-swe-agent
# or
pip install pipx && pipx ensurepath && pipx run mini-swe-agent
```

**方式 2：** 在当前环境中安装 CLI 与 Python 绑定

```bash
pip install mini-swe-agent
mini  # 运行 CLI
```

**方式 3：** 从源码安装（开发者配置）

```bash
git clone https://github.com/SWE-agent/mini-swe-agent.git
cd mini-swe-agent && pip install -e .
mini  # 运行 CLI
```

在我们的[文档](https://mini-swe-agent.com/latest/)中了解更多：

* [快速入门指南](https://mini-swe-agent.com/latest/quickstart/)
* [使用 `mini` CLI](https://mini-swe-agent.com/latest/usage/mini/)
* [全局配置](https://mini-swe-agent.com/latest/advanced/global_configuration/)
* [Yaml 配置文件](https://mini-swe-agent.com/latest/advanced/yaml_configuration/)
* [用 cookbook 增强能力](https://mini-swe-agent.com/latest/advanced/cookbook/)
* [常见问题（FAQ）](https://mini-swe-agent.com/latest/faq/)
* [参与贡献！](https://mini-swe-agent.com/latest/contributing/)

## 引用

如果你觉得这项工作有帮助，请在你的工作中考虑引用 [SWE-agent 论文](https://arxiv.org/abs/2405.15793)：

```bibtex
@inproceedings{yang2024sweagent,
  title={{SWE}-agent: Agent-Computer Interfaces Enable Automated Software Engineering},
  author={John Yang and Carlos E Jimenez and Alexander Wettig and Kilian Lieret and Shunyu Yao and Karthik R Narasimhan and Ofir Press},
  booktitle={The Thirty-eighth Annual Conference on Neural Information Processing Systems},
  year={2024},
  url={https://arxiv.org/abs/2405.15793}
}
```

我们的其他项目：

<div align="center">
  <a href="https://github.com/SWE-agent/SWE-agent"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/sweagent_logo_text_below.svg" alt="SWE-agent" height="120px"></a>
   &nbsp;&nbsp;
  <a href="https://github.com/SWE-agent/SWE-ReX"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/swerex_logo_text_below.svg" alt="SWE-ReX" height="120px"></a>
   &nbsp;&nbsp;
  <a href="https://github.com/SWE-bench/SWE-bench"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/swebench_logo_text_below.svg" alt="SWE-bench" height="120px"></a>
   &nbsp;&nbsp;
  <a href="https://github.com/SWE-bench/SWE-smith"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/swesmith_logo_text_below.svg" alt="SWE-smith" height="120px"></a>
   &nbsp;&nbsp;
  <a href="https://github.com/codeclash-ai/codeclash"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/codeclash_logo_text_below.svg" alt="CodeClash" height="120px"></a>
   &nbsp;&nbsp;
  <a href="https://github.com/SWE-bench/sb-cli"><img src="https://raw.githubusercontent.com/SWE-agent/swe-agent-media/refs/heads/main/media/logos_banners/sbcli_logo_text_below.svg" alt="sb-cli" height="120px"></a>
</div>

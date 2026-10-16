<div align="center">
<img src="assets/mini-swe-agent-banner.svg" alt="mini-swe-agent banner" style="height: 7em"/>

<h1 style="margin-bottom: 1ex;">只有 100 行代码、却真正实用的 AI 智能体</h1>

</div>

<div align="center">

<a href="https://join.slack.com/t/swe-bench/shared_invite/zt-36pj9bu5s-o3_yXPZbaH2wVnxnss1EkQ">
    <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" alt="Slack">
</a>
<a href="https://github.com/SWE-agent/mini-swe-agent">
    <img alt="GitHub Release" src="https://img.shields.io/github/v/release/swe-agent/mini-swe-agent?style=for-the-badge&logo=github&label=GitHub&labelColor=black&color=green" alt="GitHub Release">
</a>
<a href="https://pypi.org/project/mini-swe-agent/">
    <img src="https://img.shields.io/pypi/v/mini-swe-agent?style=for-the-badge&logo=python&logoColor=white&labelColor=black&color=deeppink" alt="PyPI - Version">
</a>

</div>

!!! warning "这是 mini-swe-agent v2"

    请阅读[迁移指南](https://mini-swe-agent.com/latest/advanced/v2_migration/)。如需上一版本，请查看 [v1 文档](https://mini-swe-agent.com/v1/)或 [v1 分支](https://github.com/SWE-agent/mini-swe-agent/tree/v1)。

2024 年，[SWE-bench](https://swebench.com) 和 [SWE-agent](https://swe-agent.com) 助力掀起了编码智能体的革命。

现在我们要问：**如果我们的智能体简单 100 倍，但效果几乎一样好，会怎样？**

`mini` 具有如下特点：

- **被广泛采用**：Meta、NVIDIA、Essential AI、IBM、Nebius、Anyscale、普林斯顿大学、斯坦福大学等众多机构都在使用。
- **极简**：[只有 100 行 Python](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py)（[环境](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py)、
[模型](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)、[脚本](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/run/hello_world.py)合计再加 100 行）——没有任何花哨的依赖！
- **性能出众**：在 [SWE-bench verified 基准](https://www.swebench.com/)上得分超过 74%；启动速度远快于 Claude Code
- **易于部署**：支持**本地环境**、**docker/podman**、**singularity/apptainer**、**bubblewrap**、**contree** 等
- **兼容性强**：通过 **litellm**、**openrouter**、**portkey** 等支持所有模型。支持 `/completion` 和 `/response` 端点、交错思考（interleaved thinking）等
- 由打造 [SWE-bench](https://swebench.com)、[SWE-agent](https://swe-agent.com) 等项目的普林斯顿与斯坦福团队构建
- **经过测试**：[![Codecov](https://img.shields.io/codecov/c/github/swe-agent/mini-swe-agent?style=flat-square)](https://codecov.io/gh/SWE-agent/mini-swe-agent)

??? note "为什么用 mini-SWE-agent 做研究？"

    [SWE-agent](https://swe-agent.com/latest/) 在 2024 年开启了 AI 智能体的发展之路。当时，我们非常强调为智能体提供工具和特殊接口。然而一年之后，构建一个有用的智能体已经完全不需要这些了！

    事实上，`mini` 智能体：

    - **除 bash 之外没有任何工具** —— 它甚至不使用语言模型的工具调用接口。
      这意味着你可以用任何模型运行它。
      在沙箱环境中运行时，你也不需要操心安装任何包——它只需要 bash。
    - **拥有完全线性的历史记录** —— 智能体的每一步只是向消息列表追加内容，仅此而已。
      因此，轨迹（trajectory）与传给语言模型的消息之间没有任何差别。
      非常适合调试和微调。
    - **使用 `subprocess.run` 执行动作** —— 每个动作完全独立（而不是保持一个有状态的 shell 会话运行）。这使得在沙箱中执行动作变得非常简单（实际上只需把 `subprocess.run` 换成 `docker exec`），并且可以轻松扩展。
      说真的，这[非常重要](faq.md#why-no-shell-session)，相信我。

    这使它非常适合作为基线系统，也适合作为一个把语言模型（而非智能体脚手架）置于关注中心的系统。
    你可以在 [SWE-bench (bash only)](https://www.swebench.com/) 排行榜上看到结果，该榜单评估了不同语言模型在 `mini` 上的表现。

??? note "为什么把 mini-SWE-agent 当作工具使用？"

    有些智能体是过拟合的研究产物，另一些则是重度依赖 UI 的前端巨兽。

    `mini` 智能体想成为一个可供随意改造的工具，而不是一个黑盒。

    - **足够简单**，一眼就能看懂
    - **足够方便**，可以在日常工作流中使用
    - **足够灵活**，便于扩展

    与其他智能体（包括我们自己的 [swe-agent](https://swe-agent.com/latest/)）不同，它要激进地简单得多，因为它：

    - **除 bash 之外没有任何工具** —— 它甚至不使用语言模型的工具调用接口。
      我们不为智能体可能想做的每一件具体事情实现自定义工具，而是完全专注于让语言模型充分发挥 shell 的全部潜力。
      想让它做某件具体的事，比如开一个 PR？
      直接告诉语言模型自己去搞定，而不是花时间在智能体里实现它。
    - **使用 `subprocess.run` 执行动作** —— 每个动作完全独立（而不是保持一个有状态的 shell 会话运行）。
      这对智能体的稳定性[非常重要](https://mini-swe-agent.com/latest/faq/#why-no-shell-session)，相信我。
    - **拥有完全线性的历史记录** —— 智能体的每一步只是向下一步传给语言模型的消息中追加内容，仅此而已。
      这对于调试和理解语言模型收到的提示非常有帮助。

??? note "我应该用 mini-SWE-agent 还是 swe-agent？"

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

<table>
<tr>
<td width="50%">
<a href="usage/mini"><strong>CLI</strong></a> (<code>mini</code>)
</td>
<td>
<a href="usage/swebench/"><strong>批量推理</strong></a>
</td>
</tr>
<tr>
<td width="50%">
  <div class="gif-container" data-glightbox-disabled>
    <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/mini.png?raw=true"
         data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/mini.gif?raw=true"
         alt="mini" data-glightbox="false" />
  </div>
</td>
<td>
<div class="gif-container" data-glightbox-disabled>
  <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/swebench.png?raw=true"
       data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/swebench.gif?raw=true"
       alt="swebench" data-glightbox="false" />
</div>
</td>
</tr>
<tr>
<td>
<a href="usage/inspector/"><strong>轨迹浏览器</strong></a>
</td>
<td>
<a href="advanced/cookbook/"><strong>Python 绑定</strong></a>
</td>
</tr>
<tr>
<td>
<div class="gif-container" data-glightbox-disabled>
  <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/inspector.png?raw=true"
       data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/inspector.gif?raw=true"
       alt="inspector" data-glightbox="false" />
</div>
</td>
<td>
<pre><code class="language-python">agent = DefaultAgent(
    LitellmModel(model_name=...),
    LocalEnvironment(),
)
agent.run("Write a sudoku game")</code></pre>
</td>
</tr>
</table>


!!! info "要升级到 v2 吗？"

    请查看我们的 [v2 迁移指南](advanced/v2_migration.md)，了解所有变更以及如何更新你的代码。

## 继续阅读：

<div class="grid cards">
  <a href="quickstart/" class="nav-card-link">
    <div class="nav-card">
      <div class="nav-card-header">
        <span class="material-icons nav-card-icon">launch</span>
        <span class="nav-card-title">安装与快速入门</span>
      </div>
      <p class="nav-card-description">开始使用 mini-SWE-agent</p>
    </div>
  </a>

  <a href="usage/mini/" class="nav-card-link">
    <div class="nav-card">
      <div class="nav-card-header">
        <span class="material-icons nav-card-icon">flash_on</span>
        <span class="nav-card-title">用法：简洁界面</span>
      </div>
      <p class="nav-card-description">学习使用 <code>mini</code> 命令</p>
    </div>
  </a>

  <a href="faq/" class="nav-card-link">
    <div class="nav-card">
      <div class="nav-card-header">
        <span class="material-icons nav-card-icon">help</span>
        <span class="nav-card-title">常见问题</span>
      </div>
      <p class="nav-card-description">常见疑问与解答</p>
    </div>
  </a>

  <a href="advanced/yaml_configuration/" class="nav-card-link">
    <div class="nav-card">
      <div class="nav-card-header">
        <span class="material-icons nav-card-icon">settings</span>
        <span class="nav-card-title">配置</span>
      </div>
      <p class="nav-card-description">搭建并定制你的智能体</p>
    </div>
  </a>

  <a href="advanced/cookbook/" class="nav-card-link">
    <div class="nav-card">
      <div class="nav-card-header">
        <span class="material-icons nav-card-icon">fitness_center</span>
        <span class="nav-card-title">进阶增强</span>
      </div>
      <p class="nav-card-description">开始改造这个智能体吧！</p>
    </div>
  </a>
</div>

## 📣 新闻

* [mini-swe-agent 现已驱动 Ramp SWE-Bench](https://labs.ramp.com/swebench)
* [mini-swe-agent 在 DeepSWE 上击败了 Claude Code 和 Codex](https://deepswe.datacurve.ai/blog#evaluation-harness)
* [在我们的全新且极具挑战性的基准 ProgramBench 上运行 mini-swe-agent](usage/programbench.md)
* [关于构建极简 AI 智能体的新教程](https://minimal-agent.com/)
* 11 月 19 日：[Gemini 3 Pro 借助 mini-swe-agent 在 SWE-bench verified 上达到 74%！](https://x.com/KLieret/status/1991164693839270372)
* 8 月 19 日：[新博客文章：在 GPT-5 和 Sonnet 4 之间随机切换可以提升性能](https://www.swebench.com/post-250820-mini-roulette.html)

## 📣 新特性

最新更新请查看 [GitHub 发行说明](https://github.com/SWE-agent/mini-swe-agent/releases)。

## 📣 文档更新

* 7 月 27 日：关于[本地模型](models/local_models.md)的更多说明

{% include-markdown "_footer.md" %}

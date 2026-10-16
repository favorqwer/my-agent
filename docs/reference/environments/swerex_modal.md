# SWE-ReX Modal

!!! note "SWE-ReX Modal 环境类"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/environments/extra/swerex_modal.py)
    - 需要 [Modal](https://modal.com) 账号并完成认证

该环境通过 [SWE-ReX](https://github.com/swe-agent/swe-rex) 在 [Modal](https://modal.com) 沙箱中执行命令。

## 设置

1. 安装完整依赖：
   ```bash
   pip install "mini-swe-agent[full]"
   ```

2. 设置 Modal 认证：
   ```bash
   modal setup
   ```

## 用法

使用 Modal 在 SWE-bench 上评测 GPT-5 mini：
```
mini-extra swebench \
    --config src/minisweagent/config/extra/swebench_modal.yaml \
    --subset verified \
    --split test \
    --workers 100 \
    -o ./results/gpt5-mini-modal
```

{% include-markdown "../../_footer.md" %}

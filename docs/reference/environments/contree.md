# ConTree

!!! note "ConTree 环境类"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/environments/extra/contree.py)
    - 需要 [ConTree](https://contree.dev) token

    ??? note "完整源代码"

        ```python
        --8<-- "src/minisweagent/environments/extra/contree.py"
        ```

::: minisweagent.environments.extra.contree

该环境通过 [ConTree SDK](https://github.com/nebius/contree-sdk) 在 [ConTree](https://contree.dev) 沙箱中执行命令

## 设置

1. 安装依赖：
   ```bash
   pip install "mini-swe-agent[contree]"
   ```

2. 设置 ConTree 的 token 和 base_url：
   ```bash
   export CONTREE_TOKEN="your-contree-token"
   export CONTREE_BASE_URL="your-given-base-url-for-contree"
   ```

## 用法

像使用任何其他环境一样运行 mini-swe-agent：
```
mini-extra swebench \
    --subset verified \
    --split test \
    --workers 100
    --environment-class contree
```

它既可以通过 CLI 参数指定，也可以在 swebench.yaml 配置中把 `environment_class` 设为 `contree`

{% include-markdown "../../_footer.md" %}


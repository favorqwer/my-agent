# Python 绑定

!!! abstract "概览"

    本页展示了把 mini-SWE-agent 作为 Python 库使用的最基本示例。
    关于更高级的用法、子类化以及组件的混搭组合，请参见[子类化与更多内容](../advanced/cookbook.md)。

## Hello world

```python
import logging

from minisweagent.agents.default import DefaultAgent
from minisweagent.models import get_model
from minisweagent.environments.local import LocalEnvironment

logging.basicConfig(level=logging.DEBUG)
task = "Write a hello world program"
model_name = "anthropic/claude-sonnet-4-5-20250929"

agent = DefaultAgent(
    get_model(input_model_name=model_name),
    LocalEnvironment(),
)

# 运行智能体
agent.run(task)
```

{% include-markdown "../_footer.md" %}

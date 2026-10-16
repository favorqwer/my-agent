# Yaml 配置文件

!!! abstract "智能体配置文件"

    * 你可以使用 YAML 配置文件来配置智能体的行为。本指南介绍具体做法。
    * 你应该已经熟悉[快速入门指南](../quickstart.md)了。
    * 关于全局环境设置（API key、默认模型等，基本上任何能以环境变量形式设置的内容），请参见[全局配置](global_configuration.md)。
    * 还想要更多？请参见 [Python 绑定](cookbook.md)，了解如何子类化并开发你自己的智能体。

## 整体结构

配置文件长这样：

??? note "配置文件"

    ```yaml
    --8<-- "src/minisweagent/config/mini.yaml"
    ```

我们使用以下顶层键：

- `agent`：智能体配置（提示词模板、成本上限等）
- `environment`：环境配置（例如你想在 docker 容器中运行）
- `model`：模型配置（模型名称、推理强度等）
- `run`：运行配置（输出文件等）

## 智能体配置

不同的智能体类可能有略微不同的配置选项。
完整的选项列表可以在 [API 参考](../reference/agents/default.md)中找到。

要使用不同的智能体类，你可以把 `agent_class` 键设为你想用的智能体类名，
甚至设为一个导入路径（这样即使你自己的自定义智能体类还不属于 mini-SWE-agent 包，也能使用它）。

### 提示词模板

我们使用 [Jinja2](https://jinja.palletsprojects.com/) 来渲染模板（例如实例模板）。

简而言之：你用双（！）花括号包含变量，例如 `{{task}}` 用来包含交给智能体的任务。

不过，你也可以直接在模板中实现相当复杂的逻辑，比如：

??? note "示例：处理过长的观察结果"

    下面的代码片段会缩短过长的观察结果，并在输出太长时显示一条警告。

    ```jinja
    <returncode>{{output.returncode}}</returncode>
    {% if output.output | length < 10000 -%}
        <output>
            {{ output.output -}}
        </output>
    {%- else -%}
        <warning>
            The output of your last command was too long.
            Please try a different command that produces less output.
            If you're looking at a file you can try use head, tail or sed to view a smaller number of lines selectively.
            If you're using grep or find and it produced too much output, you can use a more selective search pattern.
            If you really need to see something from the full command's output, you can redirect output to a file and then search in that file.
        </warning>

        {%- set elided_chars = output.output | length - 10000 -%}

        <output_head>
            {{ output.output[:5000] }}
        </output_head>

        <elided_chars>
            {{ elided_chars }} characters elided
        </elided_chars>

        <output_tail>
            {{ output.output[-5000:] }}
        </output_tail>
    {%- endif -%}
    ```

在所有内置智能体中，你都可以使用以下变量：

- 环境变量（仅 `LocalEnvironment` 支持，相关讨论见[这里](https://github.com/SWE-agent/mini-swe-agent/pull/425)）
- 智能体配置变量（即配置文件中 `agent` 部分设置的所有内容，例如 `step_limit`、`cost_limit` 等）
- 环境配置变量（即配置文件中 `environment` 部分设置的所有内容，例如 `cwd`、`timeout` 等）
- 传给智能体 `run` 方法的变量（默认只有 `task`，但如果需要，你也可以传其他变量）
- 上一次动作执行的输出（即 `execute_action` 方法返回的 `output`）

### 使用工具调用

请确保使用合适的模型类以及与之匹配的配置。

### 从文本中自定义解析动作

mini-SWE-agent 可以从 markdown 代码块（` ```mswea_bash_command ... ``` `）或工具调用中解析动作。
你可以通过设置 `action_regex` 字段来自定义这一行为，以支持 XML 等不同格式。

!!! warning "重要"

    如果你设置了自定义的 action_regex（例如 `<action>(.*?)</action>`），你必须在所有提示词模板（system_template、instance_template、format_error_template 等）中使用相同的输出格式，确保 LLM 相应地包裹命令。完整配置示例见下文。


??? example "用 XML 格式替代 markdown"

    本示例使用与默认 mini.yaml 配置相同的结构，只是用 `<action>` 标签代替了 markdown 代码块：

    ```yaml
    --8<-- "src/minisweagent/config/benchmarks/swebench_xml.yaml"
    ```

    你也可以通过指定 `--config swebench_xml` 直接加载这个配置。


??? example "默认的 markdown 格式"

    这是默认配置（本来就是默认值，你无需显式指定）：


    ```yaml
    model:
      action_regex: ```mswea_bash_command\s*\n(.*?)\n```
    agent:
      system_template: |
        Your response must contain exactly ONE bash code block.

        ```mswea_bash_command
        your_command_here
        ```
    ```

!!! warning "换行与转义"

    在从 `yaml` 配置文件指定 `action_regex` 时，请务必理解 yaml 文件中的转义规则。
    例如，当你使用 `|` 语法时，你的正则表达式末尾可能会有一个换行符，这很可能不是你想要的。
    最好的做法是把正则写在一行内，并且不要在它两边加任何引号。你不必对正则中的任何字符进行转义。例如：`action_regex: <bash_code>(.*?)</bash_code>`

## 模型配置

模型配置的更多细节请参见[这份指南](../models/quickstart.md)。

## 环境配置

环境配置的更多细节请参见[这份指南](../advanced/environments.md)。

## 运行配置

参见“用法”部分中的信息。

{% include-markdown "_footer.md" %}

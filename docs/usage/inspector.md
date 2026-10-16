# Inspector：浏览智能体轨迹

!!! abstract "概览"

    * `inspector` 是一个工具，可以让你浏览展示 mini-SWE-agent 运行历史的 `.traj.json` 文件。
    * 可以用 `mini-e i` 或 `mini-extra inspector` 快速启动它。
    * 轨迹文件格式请参见[输出文件](output_files.md)。
    * 替代方案：[jless](https://jless.io/) 是一个很棒的用于浏览轨迹的命令行 JSON 查看器。

<figure markdown="span">
  <div class="gif-container gif-container-styled" data-glightbox-disabled>
    <img src="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/png/inspector.png?raw=true"
         data-gif="https://github.com/SWE-agent/swe-agent-media/blob/main/media/mini/gif/inspector.gif?raw=true"
         alt="inspector" data-glightbox="false" width="600" />
  </div>
</figure>

## 用法

```bash
# 从当前目录递归查找所有 .traj.json 文件
mini-extra inspector
# 或更短的写法
mini-e i
# 打开指定文件的 inspector
mini-e i <path_to_traj.json>
# 在指定目录中搜索轨迹文件
mini-e i <path_to_directory>
```

## 按键绑定

- `q`：退出 inspector
- `h`/`LEFT`：上一步
- `l`/`RIGHT`：下一步
- `j`/`DOWN`：向下滚动
- `k`/`UP`：向上滚动
- `H`：上一条轨迹
- `L`：下一条轨迹
- `e`：在 [jless](https://jless.io/) 中打开当前步骤

### 常见问题

> 如何在屏幕上选择／复制文本？

按住 `Alt`/`Option` 键，然后用鼠标选择文本。

## 实现

inspector 使用 [textual](https://textual.textualize.io/) 实现。

??? note "实现"

    - [在 GitHub 上阅读](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/run/utilities/inspector.py)

    ```python linenums="1"
    --8<-- "src/minisweagent/run/utilities/inspector.py"
    ```

{% include-markdown "../_footer.md" %}

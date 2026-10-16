# 输出文件

!!! abstract "概览"

    mini-SWE-agent 以 JSON 格式保存运行结果。本页记录这些输出文件的结构。

## 轨迹文件（`.traj.json`）

!!! warning "v2.0 格式变更"

    输出格式在 v2.0 中发生了变化（`trajectory_format: mini-swe-agent-1.1`）。更多信息请参见 [v2 迁移指南](../advanced/v2_migration.md)。

!!! tip "查看轨迹文件"

    使用 [inspector](inspector.md) 以交互方式浏览轨迹文件。

轨迹文件包含一次智能体运行的完整历史，包括所有消息、配置和元数据。

### 结构

```json
{
  "info": {
    "model_stats": {
      "instance_cost": 0.05,  // 本次运行 API 调用的总成本
      "api_calls": 12  // 发起的 API 调用次数
    },
    "config": {
      "agent": { ... },  // 智能体配置
      "agent_type": "minisweagent.agents.default.DefaultAgent",
      "model": { ... },  // 模型配置
      "model_type": "minisweagent.models.litellm_model.LitellmModel",
      "environment": { ... },  // 环境配置
      "environment_type": "minisweagent.environments.local.LocalEnvironment"
    },
    "mini_version": "2.0.0",  // 所使用的 mini-SWE-agent 版本
    "exit_status": "Submitted",  // 最终状态（Submitted、LimitsExceeded 等）
    "submission": "..."  // 智能体提交的最终输出／补丁（如果有）
  },
  "messages": [  // 完整对话历史
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    ...
  ],
  "trajectory_format": "mini-swe-agent-1.1"  // 格式版本标识符
}
```


消息遵循 [OpenAI 聊天格式](https://platform.openai.com/docs/api-reference/chat)，并额外带有一个 `extra` 字段用于存放 mini-SWE-agent 的元数据。模型可能会给消息添加其他字段（例如 `tool_calls`、`reasoning_content`）。

!!! note "工具调用类模型"
    使用基于工具调用的模型（例如 `LitellmToolcallModel`）时，角色略有不同：assistant 消息包含 `tool_calls` 而不是 content，观察（observation）消息使用 `role: "tool"` 并带有一个 `tool_call_id` 字段。

```json
// 系统消息（智能体指令）
{"role": "system", "content": "You are a helpful assistant..."}

// 用户消息（任务描述）
{"role": "user", "content": "Please solve this issue: ..."}

// assistant 消息（模型响应，包含解析出的动作）
{
  "role": "assistant",
  "content": "Let me check the files...\n\n```mswea_bash_command\nls -la\n```",
  "extra": {
    "actions": [{"command": "ls -la"}],  // 解析出待执行的动作
    "cost": 0.003,  // 本次 API 调用的成本
    "timestamp": 1706000000.0,  // 该消息创建时的 unix 时间戳
    "response": { ... }  // API 的原始响应
  }
}

// 观察消息（执行结果）
{
  "role": "user",
  "content": "<returncode>0</returncode>\n<output>\nfile1.py\nfile2.py\n</output>",
  "extra": {
    "returncode": 0,
    "timestamp": 1706000001.0
  }
}

// 最终消息（智能体提交时）
{
  "role": "user",
  "content": "",
  "extra": {
    "exit_status": "Submitted",
    "submission": "diff --git a/file.py..."
  }
}
```


## `preds.json` 格式

预测文件汇总了所有实例的结果，其格式与 SWE-bench 评测兼容：

```json
{
  "owner__repo__123": {  // 以 instance_id 为键
    "model_name_or_path": "anthropic/claude-sonnet-4-5-20250929",  // 所使用的模型
    "instance_id": "owner__repo__123",  // SWE-bench 实例标识符
    "model_patch": "diff --git a/file.py b/file.py\n..."  // 生成的补丁（unified diff）
  },
  ...
}
```

{% include-markdown "../_footer.md" %}

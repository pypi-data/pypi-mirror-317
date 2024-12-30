# Agent

一个简单的Agent查询库。

## 安装

```bash
pip install agent
```

## 使用方法

```python
from agent import Agent

# 初始化agent
agent = Agent(api_key="your-api-key", agent_id="optional-agent-id", agent_name="optional-agent-name")

# 发送查询
response = agent.query("你的查询内容")
```

## 参数说明

- `api_key`: 必需，用于认证的API密钥
- `agent_id`: 可选，agent的唯一标识符
- `agent_name`: 可选，agent的名称

## 许可证

MIT 
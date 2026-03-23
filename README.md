# 0xGame AI CTF挑战平台

> 一个完整的AI提示词越狱挑战平台模板，包含选手端AI服务和可选的后台日志监控系统。

## 项目概述
本项目专注于AI安全和Prompt Injection防护挑战。为了适应不同的出题需求，项目采用模块化设计：

1. **AI服务 (核心)** (`ai/`) - 选手端AI聊天服务，扮演神秘图书馆管理员角色。**支持完全独立部署**。
2. **日志服务 (可选)** (`logger/`) - 后台日志监控系统，用于实时监控选手的交互记录。

## 项目结构

```
ai_timu/
├── ai/                          # 选手端AI服务 (核心)
│   ├── src/                     # 源代码目录
│   └── ...
├── logger/                     # 后台日志服务 (可选)
│   ├── log_receiver.py          # 主程序
│   └── ...
├── docker-compose.yml          # 全局一键编排配置
└── README.md                   # 主项目文档 (本文件)
```

## 功能特性

### AI服务特性
- 🤖 基于Flask的AI聊天服务，集成SiliconFlow API
- 🛠️ 支持选手自定义 API Key 和 Model ID，避免硬编码失效
- 🛡️ 多层Prompt Injection防护机制
- 📝 实时日志发送 (支持远程服务器，即使服务器不可用也不影响挑战)
- 🎨 精美的Web前端界面
- 🐳 完整的Docker容器化部署

### 日志服务特性 (可选)
- 🔐 带身份验证的Web管理界面
- 📊 实时日志接收和分类显示
- 🗂️ 按会话ID自动分类管理

## 快速开始

### 方案 A：一键全栈部署 (推荐)

如果您希望同时拥有 AI 挑战和后台日志监控功能：

```bash
# 在项目根目录下
docker compose up -d --build
```

### 方案 B：仅部署 AI 挑战服务 (最简模式)

如果您只需要 AI 挑战功能，不需要后台监控：

```bash
cd ai
docker compose up -d --build
```

## 访问服务

- **AI挑战服务**: http://localhost:11434
- **日志监控后台**: http://localhost:8080 (仅在方案 A 下可用)

## 详细配置

### 1. Flag 配置
修改 `ai/flag` 文件内容为您的实际 Flag。

### 2. AI 提示词定制
修改 `ai/src/server.py` 中的 `prompt` 变量内容。

### 3. 日志上报配置
在 `docker-compose.yml` (方案 A) 或 `ai/Dockerfile` (方案 B) 中修改 `EXFIL_HOST`：
- 方案 A 下默认为 `logger`。
- 方案 B 下若不使用日志，可保持默认。

## 常见问题

**Q: 为什么 API Key 验证失败？**
A: 请确保您的 SiliconFlow 账号已完成实名认证，并检查 API Key 是否正确。

**Q: 选手可以更换模型吗？**
A: 可以。前端提供了 Model ID 输入框，选手可以填入硅基流动支持的任何有效模型 ID。

### 日志服务配置

修改管理员凭证：
```yaml
environment:
  - ADMIN_USERNAME=your-admin-username
  - ADMIN_PASSWORD=your-secure-password
  - SECRET_KEY=your-secret-key
```

## 安全特性

### AI服务安全
- 严格的Prompt Injection检测
- 敏感信息过滤
- 交互频率限制
- 会话隔离

### 日志服务安全
- Flask-Login身份验证
- 密码哈希存储
- 会话管理
- 数据转义处理

## 开发说明

### 本地开发

```bash
# AI服务
cd ai/src
pip install -r ../requirements.txt
python server.py

# 日志服务
cd logger
pip install -r requirements.txt
python log_receiver.py
```

### 自定义挑战

1. 修改AI提示词背景故事
2. 更新前端界面样式
3. 调整安全检测规则
4. 配置自定义Flag

## 故障排除

### 常见问题

1. **端口冲突**: 检查11434、5656、8080端口是否被占用
2. **连接失败**: 确认Docker服务正常运行
3. **日志不显示**: 检查网络连接和防火墙设置

### 日志查看

```bash
# 查看AI服务日志
cd ai
docker-compose logs -f

# 查看日志服务日志
cd logger
docker-compose logs -f
```

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目基于开源协议发布，具体参见各子项目文档。

## 致谢

- 感谢多多师傅在RDCTF上的原创挑战
- 感谢所有贡献者和测试人员

---

**注意**: 在生产环境中使用时，请务必修改所有默认密码和密钥！

# 0xGame AI CTF挑战平台

> 一个完整的AI提示词越狱挑战平台模板，包含选手端AI服务和后台日志监控系统，本项目二创于多多师傅的RDCTF挑战中的一个题目，致谢多多

## 项目概述
本项目是一个CTF（Capture The Flag）安全挑战平台，专注于AI安全和Prompt Injection防护。项目包含两个核心组件：

1. **AI服务** (`ai/`) - 选手端AI聊天服务，扮演神秘图书馆管理员角色
2. **日志服务** (`logger/`) - 后台日志监控系统，实时记录和查看AI交互

## 项目结构
> 温馨提示：logger服务可以不用配置，细节请看ai/README.md

```
ai_timu/
├── ai/                          # 选手端AI服务
│   ├── src/                     # 源代码目录
│   │   ├── server.py           # Flask主服务
│   │   ├── log_manager.py      # 日志管理器
│   │   ├── wsgi.py             # WSGI配置
│   │   └── templates/          # 前端模板
│   │       └── index.html      # 主界面
│   ├── docker-compose.yml      # Docker编排配置
│   ├── Dockerfile              # 容器构建配置
│   ├── requirements.txt        # Python依赖
│   ├── start.sh               # 启动脚本
│   ├── flag                   # Flag文件
│   └── README.md              # AI服务文档
├── logger/                     # 后台日志服务
│   ├── templates/              # Web界面模板
│   │   ├── logger_index.html  # 日志查看界面
│   │   └── login.html         # 登录页面
│   ├── docker-compose.yml     # Docker编排配置
│   ├── Dockerfile             # 容器构建配置
│   ├── log_receiver.py        # 日志接收服务
│   ├── requirements.txt       # Python依赖
│   └── README.md              # 日志服务文档
└── README.md                  # 主项目文档（本文件）
```

## 功能特性

### AI服务特性
- 🤖 基于Flask的AI聊天服务，集成SiliconFlow API
- 🛡️ 多层Prompt Injection防护机制
- 📝 实时日志记录和发送
- 🎨 精美的Web前端界面
- 🐳 完整的Docker容器化部署

### 日志服务特性
- 🔐 带身份验证的Web管理界面
- 📊 实时日志接收和分类显示
- 🗂️ 按会话ID自动分类管理
- 🗑️ 会话删除功能
- 🌐 多用户并发支持

## 快速开始

### 1. 环境要求
- Docker & Docker Compose
- Python 3.8+

### 2. 一键部署

```bash
# 部署AI服务
cd ai
docker compose up -d

# 部署日志服务
cd ../logger
docker compose up -d
```

### 3. 访问服务

- **AI服务**: http://localhost:11434
- **日志服务**: http://localhost:8080

## 详细配置

### AI服务配置

修改 `ai/src/server.py` 中的系统提示词：
```python
system_prompt = """你是一个神秘图书馆的管理员...
flag: {flag_for_prompt}
"""
```

配置日志服务器地址：
```dockerfile
ENV EXFIL_HOST=your-logger-server-ip
ENV EXFIL_PORT=5656
```

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
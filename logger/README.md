# AI CTF挑战 - 日志监控服务

> 带身份验证的实时日志监控系统，用于AI安全挑战的交互记录和分析

## 项目简介

这是一个独立的、带身份验证的日志服务，专门用于接收和实时显示来自AI CTF挑战题目的交互日志。服务提供Web管理界面，支持多会话管理和实时监控。

## 功能特性

- 🔐 **安全认证**: Web界面受密码保护，防止未授权访问
- 📊 **会话管理**: 自动根据session_id对日志进行分类
- ⚡ **实时监控**: 点击会话即可实时查看交互日志
- 🗑️ **数据清理**: 支持彻底删除会话及其所有日志
- 📡 **TCP接收**: 在5656端口监听TCP连接接收日志数据
- 🐳 **容器化部署**: 完整的Docker支持，一键部署

## 快速部署

### Docker部署（推荐）

```bash
# 构建并启动服务
docker compose up -d

# 查看服务状态
docker compose logs -f

# 停止服务
docker compose down
```

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python log_receiver.py
```

## 服务访问

- **Web管理界面**: http://localhost:8080
- **日志接收端口**: TCP 5656

## 配置说明

### 必需配置项

1. **管理员凭证配置**
   
   修改 `docker-compose.yml` 中的环境变量：
   
   ```yaml
   services:
     logger:
       environment:
         # 修改为您的管理员用户名和密码
         - ADMIN_USERNAME=your-admin-username
         - ADMIN_PASSWORD=your-secure-password
         - SECRET_KEY=your-secret-key-change-this
   ```
   
   **安全提示**: 务必修改默认密码和密钥！

2. **网络配置**
   
   确保防火墙开放以下端口：
   - `5656/tcp`: 日志接收端口
   - `8080/tcp`: Web管理界面

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ADMIN_USERNAME` | 管理员用户名 | admin0xgame2025 |
| `ADMIN_PASSWORD` | 管理员密码 | you_can_not_guess_me(>_<) |
| `SECRET_KEY` | Flask会话密钥 | random-secret-key |
| `LOG_PORT` | 日志接收端口 | 5656 |
| `WEB_PORT` | Web服务端口 | 8080 |

## 使用指南

### 登录管理界面

1. 访问 `http://your-server-ip:8080`
2. 使用配置的管理员凭证登录
3. 登录后进入日志监控主界面

### 查看日志

1. **会话列表**: 左侧显示所有连接的会话ID
2. **实时查看**: 点击任意会话，右侧显示该会话的详细日志
3. **自动刷新**: 日志界面支持自动刷新显示最新内容

### 会话管理

- **删除会话**: 在查看会话日志时，点击右上角"删除此会话"按钮
- **数据清理**: 删除操作会永久移除该会话的所有日志记录

## 项目结构

```
logger/
├── templates/              # Web界面模板
│   ├── logger_index.html  # 日志查看主界面
│   └── login.html         # 登录页面
├── docker-compose.yml     # Docker编排配置
├── Dockerfile             # 容器构建配置
├── log_receiver.py        # 日志接收服务主程序
├── requirements.txt       # Python依赖
└── README.md             # 项目文档
```

## 技术架构

### 核心组件

1. **TCP日志接收器**
   - 监听5656端口接收AI服务发送的日志
   - 支持多客户端并发连接
   - 数据格式：JSON序列化

2. **Flask Web服务**
   - 提供Web管理界面
   - 集成Flask-Login身份验证
   - 实时数据推送

3. **会话管理系统**
   - 基于session_id的自动分类
   - 内存中会话数据存储
   - 会话生命周期管理

### 安全特性

- **身份验证**: Flask-Login集成
- **密码安全**: Werkzeug密码哈希
- **会话安全**: Flask会话管理
- **数据安全**: HTML转义处理


## 故障排除

### 常见问题

1. **服务无法启动**
   - 检查端口5656和8080是否被占用
   - 确认Docker服务正常运行

2. **无法接收日志**
   - 验证AI服务配置的日志服务器地址
   - 检查防火墙设置

3. **Web界面无法访问**
   - 确认8080端口已开放
   - 检查浏览器网络设置

### 日志调试

```bash
# 查看服务日志
docker compose logs -f

# 查看特定容器日志
docker compose logs logger

# 实时监控日志接收
tail -f /var/log/your-log-file
```

## 性能优化

### 内存管理
- 定期清理过期会话
- 设置会话最大数量限制
- 实现日志数据归档

### 网络优化
- 配置连接超时时间
- 实现连接池管理
- 添加流量控制机制

## 许可证

本项目基于开源协议发布，可用于教学和比赛监控用途。

---

**安全警告**: 生产环境中务必修改所有默认密码和密钥，并定期更新安全配置！
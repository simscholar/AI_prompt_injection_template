# AI CTF挑战 - 选手端服务 (核心组件)

> 基于Flask的AI安全挑战平台，专注于Prompt Injection防护。**支持完全独立部署**。

## 项目简介

本项目是一个AI安全CTF挑战的选手端服务，选手需要通过与AI对话来尝试获取隐藏的flag。AI扮演神秘图书馆管理员的角色，具有严格的防护机制防止flag泄露。

**致谢**: 本项目二创于多多师傅在RDCTF上的原创挑战题目，感谢多多师傅允许开源，方便其他出题师傅直接fork用于教学和比赛。

## 功能特性

- 🤖 **智能AI对话**: 基于SiliconFlow API的智能对话系统，支持动态 Model ID
- 🛠️ **自定义配置**: 选手可自行输入 API Key 和 Model ID，适配模型变动
- 🛡️ **多层防护**: 严格的Prompt Injection检测和防护机制
- 📝 **实时日志 (可选)**: 完整的交互日志记录，支持发送至远程日志服务器
- 🎨 **精美界面**: 现代化的Web前端界面
- 🐳 **容器化部署**: 完整的Docker支持，支持一键独立运行
- 🔄 **会话管理**: 多用户并发会话支持

## 快速部署

### 1. 独立部署 (推荐)

如果您只需要 AI 挑战功能，可以直接启动：

```bash
# 进入ai目录
cd ai

# 构建并启动服务
docker compose up -d --build
```

### 2. 配合日志服务部署

如果您需要监控选手的交互记录，请参考项目根目录下的 `docker-compose.yml` 进行一键编排。

### 3. 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
cd src
python server.py
```

## 服务访问

- **Web界面**: http://localhost:11434 (默认端口)
- **API端点**: http://localhost:5555

## 配置说明

### 必需配置项

1. **Flag设置**
   - 修改 `flag` 文件内容为您的实际flag

2. **日志服务器配置 (可选)**
   - 修改 `Dockerfile` 中的日志服务器地址：
   ```dockerfile
   ENV EXFIL_HOST=logger # 如果不使用日志服务，可保持默认或设为空
   ENV EXFIL_PORT=5656
   ```
   *注：即使日志服务器不可用，AI 挑战功能仍可正常使用。*

3. **AI提示词定制**
   - 修改 `src/server.py` 中的系统提示词内容
   - 使用 `{flag_for_prompt}` 作为flag占位符

4. **前端定制**
   - 修改 `src/templates/index.html` 中的banner信息
   - 可自定义比赛名称和样式

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `EXFIL_HOST` | 日志服务器地址 (可选) | logger |
| `EXFIL_PORT` | 日志服务器端口 | 5656 |
| `OPENAI_BASE_URL` | AI API 基础地址 | https://api.siliconflow.cn/v1 |
| `SERVER_PORT` | 容器内部服务端口 | 5555 |
| `FLAG` | 题目的动态flag | flag若是没有写入环境变量，会触发错误flag：FLAG{wrong_ask_yolo} |

## 安全机制

### Prompt Injection防护
- 关键词过滤和检测
- 上下文一致性检查
- 敏感信息屏蔽
- 交互频率限制

### 会话安全
- 会话隔离机制
- 超时自动清理
- 请求频率限制

## 项目结构

```
ai/
├── src/                    # 源代码目录
│   ├── server.py          # Flask主服务
│   ├── log_manager.py     # 日志管理器
│   ├── wsgi.py            # WSGI配置
│   └── templates/         # 前端模板
│       └── index.html     # 主界面
├── docker-compose.yml     # Docker编排配置
├── Dockerfile             # 容器构建配置
├── requirements.txt       # Python依赖
├── start.sh              # 启动脚本
└── README.md             # 项目文档
```



## 故障排除

### 常见问题

1. **服务无法启动**
   - 检查Docker服务状态
   - 确认端口11434和5555未被占用

2. **AI无响应**
   - 检查网络连接
   - 验证SiliconFlow API密钥，自查有没有在平台实名认证

3. **日志发送失败**
   - 确认日志服务器地址正确
   - 检查防火墙设置

### 日志查看

```bash
# 查看容器日志
docker compose logs -f

# 查看特定服务日志
docker compose logs ai-service
```

## 许可证

本项目基于开源协议发布，可用于教学和比赛用途。

---

**安全提示**: 在生产环境中使用时，请务必修改所有默认配置和敏感信息！

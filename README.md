# RemoteSync项目说明

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述
基于SSH协议的Linux服务器文件同步工具，提供安全的远程文件下载功能，支持断线重连和日志记录。

## 主要功能
- ✅ SSH安全认证连接
- ⏳ 支持断线自动重连机制（指数退避策略）
- 📁 TOML配置文件驱动运行参数
- 📊 实时下载进度显示
- 🔒 基于环境变量的敏感信息保护
- 📂 自动创建本地目录结构
- 🛡 完善的异常处理与重试机制
- 📝 日志轮转与归档（默认保留7天）

## 环境要求
- Python 3.8+
- Paramiko 3.5+
- 支持SSH协议的Linux服务器

## 快速开始
```bash
# 克隆仓库
git clone https://github.com/JefffffWeng/RemoteSync.git
cd RemoteSync

# 安装依赖
pip install -r requirements.txt

# 准备配置文件
cp config.example.toml config.toml

# 配置环境变量（请替换实际值）
echo "SERVER_IP=your_server_ip
SERVER_PORT=22
SERVER_USERNAME=admin
SERVER_PASSWORD=secure_password" > .env

# 运行程序
python main.py
```

## 配置说明
### config.toml
```toml
[data_path]
remote_path = '/files/data.csv'  # 远程文件路径
local_path = './output/data.csv' # 本地存储路径

[log]
log_dir = './logs/'  # 日志存储目录
```

### .env 文件
```
SERVER_IP=your_server_ip        # 服务器IP地址
SERVER_PORT=22                  # SSH端口
SERVER_USERNAME=admin           # 用户名
SERVER_PASSWORD=secure_password # 密码
```

## 项目结构
```
├── src/
│   ├── server.py    # SSH连接核心模块（连接管理/文件传输）
│   └── utils.py     # 工具函数（日志配置/配置文件加载）
├── main.py          # 主程序入口
├── config.toml      # 应用配置文件
├── requirements.txt # 依赖清单
├── output/          # 下载文件存储目录（自动创建）
└── logs/            # 日志目录（按日轮转）
```

## 注意事项
1. 敏感信息应通过.env文件配置
2. 确保本地存储目录有写入权限（默认./output/）
3. 生产环境建议使用SSH密钥认证代替密码认证
4. 日志配置支持自定义格式和保留策略
5. 文件传输支持自定义进度回调函数
6. 重试机制默认3次重试，每次间隔5秒（指数退避）

## 故障排查
- 连接失败：检查网络连通性/防火墙设置/SSH服务状态
- 认证失败：验证用户名密码/密钥权限
- 权限问题：检查本地文件写入权限
- 详细日志：查看logs/目录下的日志文件

## 📜 开源协议

本项目遵循 [MIT License](LICENSE) 协议。详细信息请参阅项目根目录下的 `LICENSE` 文件。
# 小馋虫校园电商平台 (SCDemo)

> 一个基于Django全栈开发的校园电商系统，集商品管理、在线购物、订单处理、智能配送于一体。

[![Django Version](https://img.shields.io/badge/Django-4.0-brightgreen.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://www.mysql.com/)
[![Redis](https://img.shields.io/badge/Cache-Redis-red.svg)](https://redis.io/)

## ✨ 项目功能

### 用户前端
- **用户注册/登录**：支持手机号注册登录，集成图形验证码。
- **商品浏览**：分类展示商品，支持关键词搜索。
- **购物车管理**：基于本地存储(LocalStorage)的购物车，可随时增删商品。
- **在线下单**：完整的购物流程（添加商品 -> 加入购物车 -> 下单 -> 模拟支付）。
- **订单中心**：查看个人订单状态，确认收货。

### 管理后台
- **商品管理**：对商品进行增、删、改、查（CRUD），支持图片上传。
- **订单管理**：查看所有订单，并为订单分派配送员。
- **用户管理**：管理系统用户和配送员。
- **数据看板**：核心数据展示（可拓展）。

### 特色功能
- **配送员调度系统**：管理员可分配订单，系统追踪配送员状态（空闲/配送中）与工作量。
- **Redis缓存优化**：使用Redis缓存高频访问数据（如商品列表），大幅提升响应速度，并利用Django Signals实现缓存自动更新，保证数据一致性。
- **优雅的UI设计**：基于Bootstrap响应式布局，提供良好的移动端和桌面端体验。

## 🛠 技术栈

### 后端技术
- **框架**：Django 4.0
- **数据库**：MySQL
- **缓存**：Redis
- **任务队列**：Django Signals（自动触发缓存更新）

### 前端技术
- **前端框架**：Bootstrap
- **动态交互**：jQuery, Ajax
- **图表库**：（可选，如预留了Echarts接口）

## 📦 项目结构

```bash
SCDemo/
├── SCDemo/          # 项目主目录（包含settings.py, urls.py等）
├── app01/           # 应用主模块
│   ├── models.py    # 数据模型（商品、用户、订单、配送员）
│   ├── views.py     # 视图逻辑
│   ├── urls.py      # 应用路由
│   ├── signals.py   # 信号（缓存自动清理）
│   └── utils/       # 工具类（缓存工具、验证码生成等）
├── templates/       # 前端模板
├── media/           # 媒体文件（商品图片等）
├── static/          # 静态文件（CSS, JS, 图片）
└── README.md        # 项目说明


🚀 快速开始
前提条件
确保您的系统已安装以下环境：

Python (3.8+)
MySQL (5.7+)
Redis
安装步骤
克隆项目

git clone https://github.com/wlrbe655/SCDemo.git
cd SCDemo
创建虚拟环境并激活

python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
安装依赖

pip install -r requirements.txt
配置数据库 在MySQL中创建一个数据库（例如 scdemo），然后修改 SCDemo/settings.py 中的数据库配置：

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scdemo',       # 数据库名
        'USER': 'your_username', # 数据库用户
        'PASSWORD': 'your_password', # 数据库密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
执行数据库迁移

python manage.py makemigrations
python manage.py migrate
创建超级管理员

python manage.py createsuperuser
启动Redis服务

# 确保Redis服务正在运行
运行开发服务器

python manage.py runserver
访问项目

前端页面: http://127.0.0.1:8000/xcc/list/
管理后台: http://127.0.0.1:8000/admin/ (需先执行createsuperuser命令)

📷 功能截图
（在这里添加几张项目运行的效果图，例如商品列表页、购物车页面、管理后台等）
<img width="2547" height="1354" alt="image" src="https://github.com/user-attachments/assets/44a12590-061d-4a61-919e-dd1fb4f18180" />


🤝 贡献
我们非常欢迎各种形式的贡献！如果您有任何建议或问题，请随时：

提交 Issue
发起 Pull Request
📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

👨‍💻 作者
您的姓名

个人主页: https://github.com/dashboard
邮箱: 3533141699@qq,com
如果这个项目对您有帮助，请给我一个Star！ ⭐





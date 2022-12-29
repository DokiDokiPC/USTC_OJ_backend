# USTC_OJ_backend

### 依赖
* MySQL或 MariaDB
* RabbitMQ

### 安装

```bash
pip install -e .
```

### 创建您的数据库配置

在backend文件夹下创建文件config.toml，并依照以下样例填入你的数据库和RabbitMQ配置

```text
DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/ustcoj?charset=utfmb4"
AMQP_URI = "amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
```

### 自动创建表格

数据库需要您自己创建 并修改配置信息中的数据库名称为您创建的数据库名称

表格创建方法：

```bash
python tests/init_data.py
```

### 使用

```bash
python run.py
```

确保您在根目录(即USTC_OJ_backend)之下运行命令

### API文档

API.md为API说明

### 后台登录

localhost:5000/admin

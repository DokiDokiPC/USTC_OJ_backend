# USTC_OJ_backend

### 创建您的数据库配置
在backend文件夹下创建文件database_config.toml，并依照以下样例填入你的数据库配置
```text
USERNAME = "root"
HOSTNAME = "127.0.0.1"
DATABASE_NAME = "ustcoj"
PASSWORD = "123456"
PORT = "3306"
```

### 自动创建表格
数据库需要您自己创建 并修改配置信息中的数据库名称为您创建的数据库名称

表格创建方法：
```bash
python tests/create_tables.py
```


### 使用

```bash
pip install -e .
python run.py
```

确保您在根目录(即USTC_OJ_backend)之下运行命令

### 文档查看
localhost:5000/docs/api

### 后台登录

localhost:5000/admin

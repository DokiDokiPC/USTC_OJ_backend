# USTC_OJ_backend

### 创建您的数据库配置
仿照database_config_example.toml文件 创建my_database_config.toml文件 并修改配置信息（例如密码等）为您自己的配置。

### 自动创建表格
数据库需要您自己创建 并修改配置信息中的数据库名称为您创建的数据库名称

表格创建方法：
```bash
./create_tables.sh
```


### 使用

```bash
pip install -e .
flask --app backend run
```

Or

```bash
./run.sh
```

确保您在根目录(即USTC_OJ_backend)之下运行命令

### 文档查看
localhost:5000/docs/api

### Admin登录
User增加isAdmin指示用户是否为管理员

localhost:5000/admin

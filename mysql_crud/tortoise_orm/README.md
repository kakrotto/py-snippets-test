### aerich 根据表生成模型代码

```shell
# 创建 aerich 配置文件
aerich init -t config.TORTOISE_ORM

# 初始化，建aerich表
aerich init-db

# 打印数据库中的所有表模型代码到控制台
aerich --app models inspectdb

# user 表模型代码生成到 models.py 文件中,这里如果每次都把模型代码生成到同一文件，模型代码会被覆盖
aerich inspectdb -t user > models.py
aerich inspectdb -t user > models/user.py
```


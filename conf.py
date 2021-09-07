from sqlalchemy.sql.expression import false


DATABASES = {
    "world": {
        "uri": "mysql+pymysql://root:root@localhost:3306/world?charset=utf8mb4",
        "echo": False,
    }
}

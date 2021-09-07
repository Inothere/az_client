from sqlalchemy.sql.expression import false


DATABASES = {
    "world": {
        "uri": "mysql+pymysql://root:passwd@localhost:3307/acore_world?charset=utf8mb4",
        "echo": False,
    }
}

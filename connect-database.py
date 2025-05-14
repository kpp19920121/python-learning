import psycopg2
from psycopg2 import pool
from psycopg2._psycopg import connection


def connect_pgsql(connect :connection=None):
    try:
        if connect is None:
            print("数据库连接不存在，自动创建连接!")
            connect= psycopg2.connect(
                host="192.168.146.125",
                database="postgres",
                user="postgres",
                password="postgres",
                port="5432"  # PostgreSQL 默认端口
            )
        with connect.cursor() as cur:
           cur.execute("select  * from test_users")

           for row in cur.fetchmany(10):
               print(row)

    except Exception as e:
        # 6. 出错回滚
        print(f"数据库错误: {e}")
        raise ValueError(e);
    finally:
        if connect is not None:
            connect.close()
def connect_pgsql_pool():
    pgpool=pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host="192.168.146.125",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432"  # PostgreSQL 默认端口
    )

    connect_pgsql(pgpool.getconn())


if __name__=='__main__':
    #connect_pgsql()
    connect_pgsql_pool()
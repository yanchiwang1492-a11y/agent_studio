from psycopg_pool import ConnectionPool

#配置连接池
pool = ConnectionPool(
    conninfo="host=127.0.0.1 port=5432 dbname=postgres user=postgres password=1",
    max_size=20,#最大连接数，生成环境是20个
    min_size=10,#最小连接数，生成环境是10个
)

# # 1. 创建一个池子（min_size=10，此时池子里已经有 10 把钥匙了）
# pool = ConnectionPool(conninfo="...", min_size=10)
#
# # 2. 从池子里借出一把钥匙
# with pool.connection() as conn:   # ← 这一刻，你从池子里拿走了 1 把钥匙
#     # 3. 用这把钥匙开门，执行 SQL
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM user_info")

class SummaryMemory:

    def __init__(self,session_id:str):
        self.session_id = session_id
    #保存
    def save(self,summary:str):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql =(f"INSERT INTO conversation_summary(session_id, summary) "
                      f"VALUES('{self.session_id}','{summary}') "
                      f"ON CONFLICT(session_id) "
                      f"DO UPDATE SET "
                      f"summary=EXCLUDED.summary,"
                      f"update_time=NOW()")
                cur.execute(sql)
                #提交事务
                con.commit()
    #查询
    def query(self):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql = f"select summary from conversation_summary where session_id ='{self.session_id}'"
                cur.execute(sql)
                #查询单个值
                rs = cur.fetchone()

                if rs:
                    return rs[0]
                else:
                    return ""
if __name__ =="__main__":
    s = SummaryMemory("005")
    s.save('李四很聪明')
    print(s.query())
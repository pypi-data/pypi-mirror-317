
## 同步使用示例

# from connect import Dbmanager

# dbm = Dbmanager()
# with dbm.pool.connection() as conn:
#     with conn.cursor() as cur:
#         cur.execute("SELECT 1")
#         data = cur.fetchone()
#         print(data)



# 异步使用示例

import asyncio
from connect_async import DbmanagerAsync

async def test():
    dbm =await DbmanagerAsync.connect(conn_str='dbname=shop_data user=postgres password=manji1688 host=127.0.0.1 port=5432')
    async with dbm.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
            data = await cur.fetchone()
            print(data)



if __name__ == "__main__":
    asyncio.run(test())

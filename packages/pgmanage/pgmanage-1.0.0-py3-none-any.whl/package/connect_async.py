import atexit
import os
import asyncio
import logging
from psycopg_pool import AsyncConnectionPool

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 设置兼容的事件循环策略
from asyncio import WindowsSelectorEventLoopPolicy
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

class DbmanagerAsync:
    pool = None  # 类变量用于存储连接池
    
    def __init__(self, conn_str: str = None):
        # if pglink is None:
        #     pglink = os.environ.get("PGLINK_URL")
        #     if pglink is None:
        #         raise ValueError("Database connection string not provided and PGLINK_URL environment variable not set.")
        # # # 设置兼容的事件循环策略
        # # if asyncio.get_event_loop().is_closed() or isinstance(asyncio.get_event_loop(), asyncio.ProactorEventLoop):
        # #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        # try:
        #     self.pool = AsyncConnectionPool(conninfo=pglink,open=True)
        #     self.pool.open()
        # except Exception as e:
        #     raise RuntimeError(f"Failed to initialize database connection pool: {e}")
        
        # atexit.register(self._sync_close_pool)  # 使用同步方法注册给 atexit
        pass
    @classmethod
    async def connect(cls,conn_str:str=None):
        """
        初始化数据库连接池
        :param pglink: 数据库连接字符串
        :return: DbmanagerAsync 实例
        """
        instance = cls(conn_str)
        await instance._init_pool_(conn_str)
        return instance
    async def _init_pool_(self,conn_str: str = None):
        if not self.pool:
            if conn_str is None:
                conn_str = os.environ.get("PGLINK_URL")
                if conn_str is None:
                    raise ValueError("Database connection string not provided and PGLINK_URL environment variable not set.")
            self.pool = AsyncConnectionPool(conn_str,open=False)
            await self.pool.open()  # 显式打开连接池
            atexit.register(self._sync_close_pool)  # 使用同步方法注册给 atexit
            
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_pool()

    async def close_pool(self):
        if hasattr(self, 'pool') and self.pool is not None:
            try:
                await self.pool.close()  # 注意这里应该是 await
                logger.info("运行完毕已自动关闭连接池")
            finally:
                self.pool = None

    def _sync_close_pool(self):
        # 确保在同步环境中也能关闭连接池
        if hasattr(self, 'pool') and self.pool is not None:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # 如果事件循环正在运行，使用 run_coroutine_threadsafe
                    future = asyncio.run_coroutine_threadsafe(self.pool.close(), loop)
                    future.result()  # 等待结果
                else:
                    asyncio.run(self.pool.close())
                logger.info("运行完毕已自动关闭连接池")
            finally:
                self.pool = None
# 示例用法
# async def main():
#     async with AsyncDbManager() as db_manager:
#         # 在这里执行数据库操作
#         pass

# asyncio.run(main())
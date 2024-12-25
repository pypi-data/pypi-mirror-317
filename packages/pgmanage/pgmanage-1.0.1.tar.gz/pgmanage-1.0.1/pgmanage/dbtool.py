



import logging
from typing import Dict, List, Any, Optional
import concurrent.futures
from pgmanage import Dbmanager

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pgtool():
    def __init__(self, conn_str: str=None):
        """
        初始化数据库连接池。
        
        :param conn_str: 数据库连接字符串
        """
        self.pool = Dbmanager(conn_str).pool

    def _exec_query(self, query: str, params: Optional[List[Any]] = None) -> bool:
        """执行SQL查询，并处理异常"""
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)
                    conn.commit()
                    return True
                except Exception as e:
                    conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise
    def exec_query(self, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """执行SQL查询，返回查询数据列表字典"""
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)
                    conn.commit()
                    column_names = [desc[0] for desc in cur.description]
                    results = cur.fetchall()
                    result_dicts = [dict(zip(column_names, row)) for row in results]
                    return result_dicts
                except Exception as e:
                    conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise
    def exec_query_rowcount(self, query: str, params: Optional[List[Any]] = None) -> int:
        """执行SQL查询，返回处理的数据行数"""
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)
                    conn.commit()
                    return cur.rowcount
                except Exception as e:
                    conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise
    def infer_data_type(self, value: Any) -> str:
            """
            根据传入的值推断数据类型。
            
            :param value: 要推断的数据值
            :return: 推断出的数据类型
            """
            print(value,type(value))
            if isinstance(value, int) and not isinstance(value, bool):
                return 'INT'
            elif isinstance(value, float):
                return 'FLOAT'
            elif isinstance(value, bool):
                return 'BOOLEAN'
            elif isinstance(value, str):
                return 'VARCHAR'
            elif isinstance(value, list):
                return 'VARCHAR[]'  # PostgreSQL 数组类型
            elif isinstance(value, dict):
                return 'JSONB'  # PostgreSQL JSONB 类型
            elif isinstance(value, (datetime.date, datetime.datetime)):
                return 'TIMESTAMP'
            else:
                return 'VARCHAR'  # 默认类型
            
    def check_table(self, schema: str, table: str) -> bool:
        """
        检查表是否存在。
        
        :param schema: 模式名
        :param table: 表名
        :return: 如果存在返回True，否则False
        """
        query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = %s AND table_name = %s);"
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema, table))
                exists = cur.fetchone()[0]
                if not exists:
                    logger.warning(f"表 '{schema}.{table}' 不存在")
                return exists

    def create_table(self, schema: str, table: str, columns: Dict[str, str], primary_key: Optional[str] = None) -> None:
        """
        创建新表。
        
        :param schema: 模式名
        :param table: 表名
        :param columns: 列定义的字典，键为列名，值为列类型
        :param primary_key: 主键列名，默认为None
        """
        cols_sql = ', '.join([f"{col} {ctype}" for col, ctype in columns.items()])
        pk_sql = f", PRIMARY KEY ({primary_key})" if primary_key else ""
        create_sql = f"CREATE TABLE {schema}.{table} ({cols_sql}{pk_sql});"
        self._exec_query(create_sql)
        logger.info(f"创建表 '{schema}.{table}' 成功")

    def get_columns(self, schema: str, table: str) -> Dict[str, str]:
        """
        获取表的所有列及其数据类型。
        
        :param schema: 模式名
        :param table: 表名
        :return: 字典，键为列名，值为数据类型
        """
        query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s;"
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema, table))
                return {row[0]: row[1] for row in cur.fetchall()}

    def add_column(self, schema: str, table: str, column: str, column_type: str) -> None:
        """
        向表中添加一列。
        
        :param schema: 模式名
        :param table: 表名
        :param column: 新列名
        :param column_type: 新列的数据类型
        """
        add_col_sql = f"ALTER TABLE {schema}.{table} ADD COLUMN {column} {column_type};"
        self._exec_query(add_col_sql)
        logger.info(f"向表 '{schema}.{table}' 添加列 '{column}',类型 '{column_type}' 成功")

    def upsert_batch(self, schema, table, batch, conflict_target, do_update_set, start_index, end_index):
        """执行单个批次的插入或更新"""
        inserted_updated_count = 0
        if not batch:
            return inserted_updated_count
        
        columns = ', '.join(batch[0].keys())
        placeholders = ', '.join(['(%s)' % ', '.join(['%s'] * len(batch[0]))] * len(batch))
        
        values = []
        for record in batch:
            values.extend(record[col] for col in batch[0].keys())

        sql = f"""
        INSERT INTO {schema}.{table} ({columns}) VALUES {placeholders} 
        ON CONFLICT {conflict_target} {do_update_set};
        """
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, values)
                    conn.commit()
                    inserted_updated_count += len(batch)
                    logger.info(f"成功处理第 {start_index + 1} 到 {end_index} 条记录，共 {len(batch)} 条")
        except Exception as e:
            conn.rollback()
            logger.error(f"处理第 {start_index + 1} 到 {end_index} 条记录时发生错误: {e}")
            logger.error(f"错误行号: {e.__traceback__.tb_lineno}")
        return inserted_updated_count
    def upsert_data(self, schema: str, table: str, data: List[Dict[str, Any]], batch_size: int = 1000, 
                           update: bool = False, create: bool = False, add_columns: bool = False, max_workers: int = 5) -> int:
        """
        使用多线程分批插入或更新数据到指定表中。
        
        :param max_workers: 线程池的最大工作线程数，默认为5
        :return: 总的成功插入和更新的记录数
        """
        if not isinstance(data, list) or not data:
            raise ValueError("无效的数据列表输入")

        total_records = len(data)
        inserted_updated_count = 0

        # 检查表是否存在并根据参数决定是否创建
        if not self.check_table(schema, table):
            if create:
                columns = {key: self.infer_data_type(value) for key, value in (data[0] if data else {}).items()}  # 把第一行数据的值类型作为字段类型
                self.create_table(schema, table, columns, primary_key='id' if 'id' in columns else None)
            else:
                raise ValueError(f"表 '{schema}.{table}' 不存在")

        existing_columns = self.get_columns(schema, table)

        if add_columns:
            all_columns = set().union(*(d.keys() for d in data))
            for col in all_columns:
                if col not in existing_columns:
                    sample_value = next((d[col] for d in data if col in d), None)
                    col_type = self.infer_data_type(sample_value)
                    self.add_column(schema, table, col, col_type)

        primary_keys = self.get_primary_keys(schema, table)
        if not primary_keys:
            raise ValueError("没有找到主键,未保证数据一致性暂停写入")

        conflict_target = '({})'.format(', '.join(primary_keys)) if primary_keys else ''
        do_update_set = "DO UPDATE SET " + ', '.join([f"{col} = EXCLUDED.{col}" for col in data[0].keys() if col not in primary_keys]) if update else "DO NOTHING"

        # 创建一个线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            # 提交每个批次的任务给线程池
            for i in range(0, total_records, batch_size):
                start_index = i
                end_index = min(i + batch_size - 1, total_records - 1)
                batch = data[i:i + batch_size]
                future = executor.submit(
                    self.upsert_batch, schema, table, batch, 
                    conflict_target, do_update_set,start_index,end_index)
                futures.append(future)

            # 收集所有线程的结果
            for future in concurrent.futures.as_completed(futures):
                inserted_updated_count += future.result()

        return inserted_updated_count

    def get_primary_keys(self, schema: str, table: str) -> List[str]:
        """
        获取给定表的主键列表。
        
        :param schema: 模式名
        :param table: 表名
        :return: 主键列表
        """
        query = """
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attnum = ANY(i.indkey) AND a.attrelid = i.indrelid
        WHERE  i.indrelid = %s::regclass
        AND    i.indisprimary;
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (f"{schema}.{table}",))
                primary_keys = [row[0] for row in cur.fetchall()]
                if not primary_keys:
                    logger.warning(f"表 '{schema}.{table}' 没有主键")
                    raise ValueError(f"表 '{schema}.{table}' 没有主键")
                return primary_keys

# 使用示例
if __name__ == "__main__":
    db_handler = Pgtool()

    # 假设有一个包含大量记录的数据列表
    data_to_bulk_insert = [
        {'id1': '1','id2': 11, 'id3': 11,'name': 'Alice', 'age': 30, 'email': 'alice@example.com'},
        {'id1': '2','id2': 12, 'id3': 11, 'name': 'Bob', 'age': 25, 'email': 'bob@example.com'},
        # ... 更多数据
    ]
    
    # 生成10万行的测试数据
    data_to_bulk_insert = []
    for i in range(100000):
        data_to_bulk_insert.append({'id': f'{i}', 'name': f'name{i}88', 'age': i % 100, 'email': f'email{i}@example.com','fasle': True})

    result = db_handler.upsert_data('data_test', 'table_test', data_to_bulk_insert, batch_size=10000, 
                                        update=True, create=True, add_columns=True)
    logger.info(f"总共成功插入或更新了 {result} 条记录")


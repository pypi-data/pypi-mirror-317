import os
import sys
sys.path.append(os.getcwd())
from package import Pgtool

# 设置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():

    # 生成10万行的测试数据
    data_to_bulk_insert = []
    for i in range(100000):
        data_to_bulk_insert.append({'id': f'{i}', 'name': f'name{i}88','name2': f'name{i}88', 'age': i % 100, 'email': f'email{i}@example.com','fasle': True})


    # 创建数据库管理器实例
    db_mgr = Pgtool('dbname=shop_data user=postgres password=manji1688 host=127.0.0.1 port=5432')

    # 写入数据，主键冲突时更新所有非主键列 upsert_data
    rows_inserted = db_mgr.upsert_data(
        schema='data_test', 
        table='table_test', 
        data=data_to_bulk_insert,
        batch_size=10000,
        update=True,
        create=True,
        add_columns=True,
        max_workers=10,
    )
    logger.info(f"总共插入 {rows_inserted} 行")

    # 执行 SQL 查询
    query = "SELECT * FROM data_test.table_test LIMIT 10;"
    result = db_mgr.exec_query(query)
    for row in result:
        logger.info(row)
        
    # 删除数据
    query = "delete  FROM data_test.table_test;"
    result = db_mgr.exec_query_rowcount(query)
    logger.info(f"删除结果:{result}")

if __name__ == '__main__':
    main()
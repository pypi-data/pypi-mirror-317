import os
from lljz_tools.client.db_client import MySQLConnectionPool
from lljz_tools.client.mongo_client import MongoClient
from lljz_tools.client.mysql_client import MySQLClient


def test_mysql():
    with MySQLConnectionPool('mysql://root:Hosonsoft2020@192.168.1.220:3307/jmg') as pool:
        with pool.connect() as db:
            db.insert('insert into t (name) values (?)', ('张三', ))
            db.insert_many('insert into t (name) values (?)', [('李四', ), ('王五', )])
            db.commit()
            print(db.select('select * from t limit 10'))
            print(db.select_one('select * from t where id = ?', (1, )))
            print(db.select_all('select * from t'))
            db.update('update t set name = ? where id = ?', ('张三三', 1))
            print(db.select('select * from t limit 10'))
            db.delete('delete from t where id = ?', (2, ))
            print(db.select('select * from t limit 10'))
            db.commit()

def test_mysql_ssh():
    with MySQLConnectionPool(
            uri=str(os.getenv('TSHIRT_MYSQL_TEST_URI')) + '/tshirt_manufacture?autocommit=true',
            ssh_uri=os.getenv('SSH_URI'),  # 通过ssh隧道连接到外网mysql
            show_sql=True
    ) as pool:
        with pool.connect() as db:
            print(db.select('select * from fact_order where id = ?', (1778267193533353985, ), limit=1))
            db.update('update fact_order set sub_id = ? where id = ?', (0, 1778267193533353985))


def test_mysql_client():
    with MySQLClient('mysql://root:Hosonsoft2020@192.168.1.220:3307/jmg') as client:
        print(client.select('select * from t_user where id = ?', (1778267193533353985, ), limit=1))
        print(client.select('select * from t_user where id = ?', (1778267193533353985, ), limit=1))

# 192.168.0.2:27017/intelligent-platform	root	Hosonsoft2023#

def test_mongo_client():
    with MongoClient(
        'mongodb://root:Hosonsoft2023#@192.168.0.71:27017/intelligent-middleground',
        ssh_uri=os.getenv('SSH_URI')
        ) as client:
        print('123')
        print(client.find_one('th_area', {"pid": 5002}))
def test_mongo_client_2():
    with MongoClient(
        'mongodb://root:Hosonsoft2023#@192.168.1.220:27017/intelligent-middleground',
        ) as client:
        print('123')
        print(client.find('th_area', {"pid": 5002}))
if __name__ == '__main__':
    test_mongo_client_2()

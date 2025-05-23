import psycopg2 
import json
from psycopg2 import Error


class Database:
    
    database = None
    @staticmethod
    def read_settings():
        with open("backend/app/settings.json", "r", encoding='utf-8') as file:
            settings = json.load(file)
        return settings
    
    @staticmethod
    def get_instance():
        if Database.database is None:
            Database.database = Database()
        return Database.database


    def __init__(self):
        settings = Database.read_settings()
        self.Host = settings["Host"]
        self.Port = settings["Port"]
        self.Username = settings["Username"]
        self.Password = settings["Password"]
        self.Database = settings["Database"]
        self.connection = self._create_server_connection()
        self._init_database()
        print("数据库已启动")

        
    def _create_server_connection(self):
        connection = None
        try:
            connection = psycopg2.connect(
                host=self.Host, port=self.Port, user=self.Username, password=self.Password, database=self.Database
            )
            print("OpenGauss Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection


    def _init_database(self):
        try:
            self.execute_sql_file("database/init_db.sql")
            result = self.read_query("SELECT COUNT(*) FROM BusRoute")
            if result[0][0] == 0:
                self.execute_sql_file("database/insert_data.sql")
        except Error as err:
            print(f"Error: '{err}'")
        

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query,params)
            self.connection.commit()
            print("Query executed successfully")
        except Error as err:
            self.connection.rollback() 
            print(f"Error: '{err}'")
        finally:
            cursor.close()

    def read_query(self,query, params=None):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query,params)
            result = cursor.fetchall()
            return result
        except Error as err:
            self.connection.rollback() 
            print(f"Error: '{err}'")
        finally:
            cursor.close()

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_commands = file.read()
            
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql_commands)
                self.connection.commit()
                print(f"SQL 文件 '{file_path}' 执行成功")
            except Error as err:
                self.connection.rollback()  # 添加回滚
                print(f"执行 SQL 文件 '{file_path}' 时出错: '{err}'")
            finally:
                cursor.close()
        except FileNotFoundError:
            print(f"SQL 文件 '{file_path}' 未找到")
        except Exception as e:
            print(f"读取 SQL 文件时发生错误: {e}")

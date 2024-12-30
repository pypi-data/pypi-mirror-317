import mysql.connector
from mysql.connector import Error


class mysql_util:
    # mysql数据库链接类
    # __init__(config： dict[str])
    def __init__(self, config):

        self.connection = None

        try:
            connection = mysql.connector.connect(**config)
            self.connection = connection
            print('Connection established')
        except Error as e:
            print(f"The error '{e}' occurred")
            return

        self.cursor = self.connection.cursor(buffered=True, dictionary=True)

        return

    def execute_query(self, query):
        try:
            self.cursor.execute(query)

            print('Query execute successful')
            return self.cursor

        except Error as e:
            print(f"The error '{e}' occurred")
            return

    def commit_query(self):
        self.connection.commit()
        print('Query commit successful')
        return

    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Connection closed')
        return

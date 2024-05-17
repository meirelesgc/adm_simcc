import os

import psycopg2


class Connection:
    def __init__(
        self,
        database: str = os.environ["ADM_DATABASE"],
        user: str = os.environ["ADM_USER"],
        host: str = os.environ["ADM_HOST"],
        password: str = os.environ["ADM_PASSWORD"],
        port: int = os.environ["ADM_PORT"],
    ):
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        self.port = port

        self.connection = None
        self.cursor = None

    def __connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                host=self.host,
                password=self.password,
                port=self.port,
            )
            self.cursor = self.connection.cursor()

        except psycopg2.Error as E:
            print("Erro ao conectar ao banco de dados:", E)

    def __close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def select(self, script_sql: str, rows: int = None):
        self.__connect()
        self.cursor.execute(script_sql)
        if rows:
            query = self.cursor.fetchmany(rows)
        else:
            query = self.cursor.fetchall()
        self.__close()
        return query

    def exec(self, script_sql: str):
        self.__connect()
        try:
            self.cursor.execute(script_sql)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as E:
            print("[Error]", E)
            self.connection.rollback()
            self.__close()
            print(E)
            raise E
        self.__close()

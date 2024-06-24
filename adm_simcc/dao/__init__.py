import os
import psycopg2
import psycopg2.extras

# Garantir que ele consiga converter UUID's
psycopg2.extras.register_uuid()


class Connection:
    def __init__(
        self,
        database: str = os.getenv("ADM_DATABASE", "postgres"),
        user: str = os.getenv("ADM_USER", "postgres"),
        password: str = os.getenv("ADM_PASSWORD", "postgres"),
        host: str = os.getenv("ADM_HOST", "localhost"),
        port: int = os.getenv("ADM_PORT", "5432"),
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

    def select(self, script_sql: str):
        self.__connect()
        try:
            self.cursor.execute(script_sql)
            query = self.cursor.fetchall()
        except psycopg2.errors.InvalidTextRepresentation as E:
            print(f"[Erro\n- Possivelmente de Djavan\n{E.pgcode}")
        finally:
            self.__close()
        return query

    def exec(self, script_sql: str):
        self.__connect()
        try:
            self.cursor.execute(script_sql)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation as E:
            print(E.pgcode)
            raise psycopg2.errors.UniqueViolation
        except (Exception, psycopg2.DatabaseError) as E:
            print(f"[Erro]\n\n{E}")
            self.connection.rollback()
        finally:
            self.__close()

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
        except psycopg2.Error as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")

    def __close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def select(self, SCRIPT_SQL: str, parameters: list = []):
        self.__connect()
        query = None
        try:
            self.cursor.execute(SCRIPT_SQL, parameters)
            query = self.cursor.fetchall()
        except psycopg2.errors.InvalidTextRepresentation as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
        except Exception as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
        finally:
            self.__close()
        return query

    def exec(self, SCRIPT_SQL: str, parameters: list = []):
        self.__connect()
        try:
            self.cursor.execute(SCRIPT_SQL, parameters)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
            self.connection.rollback()
            raise
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
            self.connection.rollback()
            raise
        finally:
            self.__close()

    def execmany(self, SCRIPT_SQL: str, parameters: list = []):
        self.__connect()
        try:
            self.cursor.executemany(SCRIPT_SQL, parameters)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
            self.connection.rollback()
            raise
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"\nTipo: {type(e).__name__}\nMensagem: {e}")
            self.connection.rollback()
            raise
        finally:
            self.__close()

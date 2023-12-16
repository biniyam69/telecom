import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def connect_to_database(connection_params):
    try:
        connection = psycopg2.connect(**connection_params)
        return connection
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None


class Database:
    def __init__(self, host, database, user, password):
        self.connection_params = {
            'dbname': 'telecom',
            'user': 'postgres',
            'password': 'heisenberg',
            'host': 'localhost',
            'port': '5432'
        }
        self.conn = connect_to_database(self.connection_params)

    def read_table_to_dataframe(self, table_name):
        if self.conn:
            query = f"SELECT * FROM {table_name};"
            df = pd.read_sql_query(query, self.conn)
            return df
        else:
            print("Error: No connection detected!")
            return None

    def write_dataframe_to_table(self, df, table_name, if_exists='replace'):
        engine = create_engine(
            f"postgresql://{self.connection_params['user']}:{self.connection_params['password']}@"
            f"{self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['dbname']}"
        )
        df.to_sql(table_name, engine, index=False, if_exists=if_exists)
        print(f"Dataframe successfully written to the '{table_name}' table.")

    def update_table_by_appending(self, df, table_name):
        self.write_dataframe_to_table(df, table_name, if_exists='append')

    def delete_table(self, table_name):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.conn.commit()
            cursor.close()
            print(f"Table '{table_name}' successfully deleted.")
        else:
            print("Error: No connection detected.")

import psycopg2
from dotenv import load_dotenv
import os
import environ
load_dotenv()


class Database:
    """Creates database structure and adds or extracts records."""
    def __init__(self):
        db_host = environ.get('HOST')
        db_port = environ.get('PORT')
        db_database = environ.get('DATABASE')
        db_user = environ.get('USER')
        db_password = environ.get('PASSWORD')

        self.__connection = psycopg2.connect(
            dbname=db_database,
            user=db_user,
            host=db_host,
            password=db_password,
            port=db_port
        )

    def create_database(self) -> None:
        """
        Creates a new table that is to be used for storing predictions. If the table already exists, it is deleted and
        a new table is initialized.
        """
        with self.__connection.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS Predictions;")

            cur.execute(
                """
                        CREATE TABLE Predictions (
                            id SERIAL PRIMARY KEY,
                            date TIMESTAMP DEFAULT NOW(),
                            input_values VARCHAR,
                            predicted_values VARCHAR
                            );
                    """
            )
            self.__connection.commit()

    def create_record(self, request: str, response: str) -> None:
        """
        Inserts the input provided by the user and the output by the model to the table
        :return:
        """
        with self.__connection.cursor() as cur:
            cur.execute(
                """
                        INSERT INTO Predictions(input_values, predicted_values)
                        VALUES (%(user_input)s, %(output)s);
                        """,
                {"user_input": request, "output": response},
            )
            self.__connection.commit()

    def get_recent_records(self, number_of_records) -> list:
        """
        Returns the desired number of most recent results consisting in input-output pairs
        :return:
        """
        with self.__connection.cursor() as cur:
            cur.execute(
                """
            SELECT input_values, predicted_values
            FROM Predictions
            ORDER BY date DESC
            LIMIT %(number)s
            """,
                {"number": number_of_records}
            )
            return cur.fetchall()


if __name__ == "__main__":
    database = Database()
    database.create_database()

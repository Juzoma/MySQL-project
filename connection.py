import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection established successfully.")
    except Error as e:

        print(f"The error '{e}' has occurred")
    return connection


conn = create_connection("vacation.cnx4hijamlfr.us-east-1.rds.amazonaws.com", "admin", "randompassword", "vacation")

cursor = conn.cursor(dictionary=True)
sql = "SELECT * FROM destination;"
cursor.execute(sql)

rows = cursor.fetchall()

for item in rows:
    print(item)


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")

    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Error as e:
        print(f"The error '{e}' occurred")
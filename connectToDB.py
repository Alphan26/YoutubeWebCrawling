# import mysql.connector

# def connectToMySQL():
#     try:
#         con = mysql.connector.connect(host = "localhost", user ="root", password ="1234")
#         # print("\nMySQL connection is succesful\n")
#         cur = con.cursor() 
       
#         return con,cur
        
#     except Exception as e:
#         print(e)
#         print("MySQL connection is unsuccesful, check your connection !!!")

# # con,cur = connectToMySQL()  # type: ignore
import psycopg2
def connectToPostgreSQL():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="Youtube-API",
            user="postgres",
            password="Ae603760."
        )

        cursor = connection.cursor()

        return connection,cursor
    except:
        print("Connection is not successful")

# Port number is set to 5432 default if not specified.


def fetchChannelTable():
    print("\nMySQL connection is succesful")
    con,cur = connectToPostgreSQL() # type: ignore

    cur.execute("SELECT * FROM youtube.ytchannelnames")
    dbResult = cur.fetchall()
    print("All data has been fetched\n")
    print(dbResult)

    return dbResult


import sqlite3
import os


try:
    sqliteConnection = sqlite3.connect('AGHNYA_SQLite.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE AGHNYA_KURUKSHETRA (

                                Id TEXT PRIMARY KEY,
                                User TEXT NOT NULL,
                                CAM TEXT NOT NULL,
                                Date_ datetime NOT NULL,
                                Time_ datetime NOT NULL,
                                Tag TEXT NOT NULL,
                                Probability REAL NOT NULL,
                                Humidity REAL NOT NULL,
                                Temperature REAL NOT NULL,
                                Weather_stats TEXT NOT NULL,
                                Detail_stats TEXT NOT NULL,
                                Wind_speed REAL NOT NULL,
                                Wind_deg REAL NOT NULL);''' 

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    sqlite_insert_query = """INSERT INTO AGHNYA_KURUKSHETRA
                          (Id,User,CAM, Date_, Time_, Tag, Probability, Humidity, Temperature, Weather_stats, Detail_stats, Wind_speed, Wind_deg) 
                          VALUES ('ABCD', 'ANKUR','cam1', '2020-07-28', '17:54','COW',97.894, 35 ,39.5,'Clouds','Broken Clouds', 4.03,303);"""
    cursor.execute(sqlite_insert_query)

    sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Error while working with SQLite", error)
finally:
    if (sqliteConnection):
        print("Total Rows affected since the database connection was opened: ", sqliteConnection.total_changes)
        sqliteConnection.close()
        print("sqlite connection is closed")
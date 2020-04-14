import sqlite3
from sqlite3 import Error

def create_db(name):

    conn = None
    try:
        conn = sqlite3.connect(name) #create a connection object representing the database
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.commit()
 
    return conn


def create_table(conn, table_sql):
    try:
        c = conn.cursor()
        c.execute(table_sql)
    except Error as e:
        print(e)
#  
#        c = conn.cursor() #create a cursor object to manage the table
# 
#     # Create table
#     c.execute('''CREATE TABLE imu
#                  (acc_x integer, acc_y integer, acc_z integer)''')
# 
# # Insert a row of data
# imu_readings = [12, 7, 54];
# c.execute("INSERT INTO imu VALUES (?,?,?)", imu_readings)
# 
# # Save (commit) the changes
# conn.commit()
# 
# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# conn.close()

def insert_row(data, conn, case):
    
    c = conn.cursor()
    
    if case  == 'acc':
        sql_row = '''INSERT INTO acc VALUES(?,?,?)'''
    elif case == 'vel':
        sql_row = '''INSERT INTO vel VALUES(?,?,?)'''
        
    c.execute(sql_row,data)

if __name__ == "__main__":
    
    database = create_db("bella.db")
    
    sql_IMU_acc_table = """ CREATE TABLE IF NOT EXISTS acc(acc_x integer, acc_y integer, acc_z integer);"""
    sql_IMU_vel_table = """ CREATE TABLE IF NOT EXISTS vel(vel_x integer, vel_y integer, vel_z integer);"""
 
    if database is not None:        
        create_table(database, sql_IMU_acc_table)
        create_table(database, sql_IMU_vel_table)
        
        insert_row([1,2,3],database,'acc')
        
        database.close()
        
    else:
        print("Something went wrong!")
    
       
# import serial 
from serial.serialutil import Serial
import time
import mysql.connector
import datetime
port = 'COM1'
t = 1
ser = serial.Serial(port, 9600)
while True:
    connection = mysql.connector.connect(host="localhost", user="root", password="1212", database="comma_patient")
    cursor = connection.cursor()
    temp = ser.readline()
    bp = ser.readline()
    decoded_bytes1 = temp[0:len(temp) - 2].decode("utf-8")
    decoded_bytes2 = bp[0:len(bp) - 2].decode("utf-8")

    y = str(decoded_bytes1)
    f = str(decoded_bytes2)
    z = f.split(".")
    x = y.split(".")
    print(x[0].strip("0"),z[1].strip("0"))
    now = datetime.datetime.now()
    cursor.execute("INSERT INTO patient_info (Time, Temperature,Heart_Beat) VALUES ('%s','%s','%s')" % (now.time(),x[0].strip("0"),z[1].strip("0")))
    connection.commit()
    connection.close()
    
    time.sleep(10)


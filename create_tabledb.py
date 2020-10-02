from tkinter import *
import sqlite3

root=Tk()
root.title("Icon pract")

conn=sqlite3.connect("address.db")
c=conn.cursor()
c.execute("""CREATE TABLE address   
    (First_name text,Last_name text, address text,city text,pin integer)
""")
conn.commit()
conn.close()

root.mainloop()
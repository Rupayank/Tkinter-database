from tkinter import *
import sqlite3
from tkinter import messagebox

root=Tk()
root.title("Icon pract")

#create Table
'''
c.execute("""CREATE TABLE address   
    (First_name text,Last_name text, address text,city text,pin integer)
""")
'''

def update():
    conn=sqlite3.connect('address.db')
    c=conn.cursor()

    record_id=select_box.get()
    # Triple quotes required so that we can write code in multiole lines
    c.execute("""UPDATE address SET
        First_name=:first,
        Last_name=:last,
        address=:address,
        city=:city,
        pin=:pincode

        WHERE oid= :oid""",
        {
            'first':fname_editor.get(),
            'last':lname_editor.get(),
            'address':addr_editor.get(),
            'city':city_editor.get(),
            'pincode':pin_editor.get(),

            'oid':record_id
        })

    conn.commit()
    conn.close()
    editor.destroy()


############################################################   
#Edit function
def edit():
    #print(type(select_box.get()))
    global editor
    editor=Tk()
    editor.title("Edit details")
    editor.geometry("400x600")

    #Conect to database
    conn=sqlite3.connect('address.db')
    c=conn.cursor()

    record_id=select_box.get()
    c.execute("SELECT * from address WHERE oid ="+record_id)
    records=c.fetchall()    

    # conn.commit()
    # conn.close()

    #Create global variables for text box names
    global fname_editor,lname_editor,addr_editor,city_editor,pin_editor

    #Create text box
    fname_editor=Entry(editor,width=25)
    fname_editor.grid(row=0,column=1)
    lname_editor=Entry(editor,width=25)
    lname_editor.grid(row=1,column=1)
    addr_editor=Entry(editor,width=25)
    addr_editor.grid(row=2,column=1)
    city_editor=Entry(editor,width=25)
    city_editor.grid(row=3,column=1)
    pin_editor=Entry(editor,width=25)
    pin_editor.grid(row=4,column=1)
    



    #Create labels
    fname_label=Label(editor,text="First name")
    fname_label.grid(row=0,column=0)
    lname_label=Label(editor,text="Last name")
    lname_label.grid(row=1,column=0)
    addr_label=Label(editor,text="Address")
    addr_label.grid(row=2,column=0)
    city_label=Label(editor,text="City")
    city_label.grid(row=3,column=0)
    pin_label=Label(editor,text="Pin code")
    pin_label.grid(row=4,column=0)

    #Loop through result
    for record in records:
        fname_editor.insert(0,record[0])
        lname_editor.insert(0,record[1])
        addr_editor.insert(0,record[2])
        city_editor.insert(0,record[3])
        pin_editor.insert(0,record[4])
        
    save=Button(editor,text="Save Record", command=update)
    save.grid(row=5,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

    editor.mainloop()


############################################################   
#Funtion to delete record
def delete():
    conn=sqlite3.connect('address.db')
    c=conn.cursor()

    #Delete a record 
    c.execute("DELETE FROM address WHERE oid="+select_box.get())
    
    conn.commit()
    conn.close()



############################################################   
#submit function
def submit():
    #Create connection or connect to one
    conn=sqlite3.connect('address.db')

    #Create cursor
    c=conn.cursor()

    #Insert into table
    c.execute("INSERT INTO address VALUES (:fname, :lname, :address, :city, :pincode)",
        {
            'fname':fname.get(), 
            'lname':lname.get(), 
            'address':addr.get(), 
            'city':city.get(),
            'pincode':pin.get()
        })

    #Commit changes
    conn.commit()
    #Close connection
    conn.close()

    #CLear text boxes
    fname.delete(0,END)
    lname.delete(0,END)
    addr.delete(0,END)
    city.delete(0,END)
    pin.delete(0,END)

    

############################################################   
#Query show
def show():
    conn=sqlite3.connect('address.db')
    c=conn.cursor()

    #Query the database
    c.execute("SELECT *,oid FROM address")
    record=c.fetchall()
    print(record)

    #Loop through records
    print_record=''
    for result in record:
        print_record+=str(result[0])+" "+str(result[1])+"\t"+str(result[5])+"\n"
    
    query_label=Label(root,text=print_record)
    query_label.grid(row=7,column=0,columnspan=2)

    conn.commit()
    conn.close()

############################################################   
#Create text box
fname=Entry(root,width=25)
fname.grid(row=0,column=1)
lname=Entry(root,width=25)
lname.grid(row=1,column=1)
addr=Entry(root,width=25)
addr.grid(row=2,column=1)
city=Entry(root,width=25)
city.grid(row=3,column=1)
pin=Entry(root,width=25)
pin.grid(row=4,column=1)
select_box=Entry(root,width=25)
select_box.grid(row=8,column=1)


############################################################   
#Create labels
fname_label=Label(root,text="First name")
fname_label.grid(row=0,column=0)
lname_label=Label(root,text="Last name")
lname_label.grid(row=1,column=0)
addr_label=Label(root,text="Address")
addr_label.grid(row=2,column=0)
city_label=Label(root,text="City")
city_label.grid(row=3,column=0)
pin_label=Label(root,text="Pin code")
pin_label.grid(row=4,column=0)
select_label=Label(root,text="Select id:")
select_label.grid(row=8,column=0)

############################################################   
#Submit
submit_btn=Button(root,text="Add record",command =submit)
submit_btn.grid(row=5,column=0,columnspan=2,padx=10,pady=10,ipadx=200)

#Query btn
query=Button(root,text="Show record", command=show)
query.grid(row=6,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

#Delete btn
delete=Button(root,text="Delete record", command=delete)
delete.grid(row=9,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

#Edit btn
edit=Button(root,text="Edit record", command=edit,state=ACTIVE)
edit.grid(row=10,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

root.mainloop()
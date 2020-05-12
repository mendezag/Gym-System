import tkinter as tk

from tkinter import *
from tkinter import ttk, PhotoImage
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from tkinter.scrolledtext import *
from PIL import ImageTk, Image

# DB
import sqlite3
import csv

#Database
dbname = 'data.db'
conn= sqlite3.connect(dbname)
c = conn.cursor()


#Create Table data
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS usersdata (firstname TEXT,lastname TEXT, email TEXT, age TEXT, date_of_birth TEXT, address TEXT, phonenumber REAL)')
    

def add_data(firstname,lastname, email, age,date_of_birth,address,phonenumber):
    task =firstname,lastname, email, age,date_of_birth,address,phonenumber
    sql= '''INSERT INTO usersdata(firstname,lastname,email,age,date_of_birth,address,phonenumber) VALUES (?,?,?,?,?,?,?)'''#,(firstname,lastname, email, age,date_of_birth,address,phonenumber))
    c.execute(sql,task)
    conn.commit()
    #print ("add data:", firstname,lastname, email, age,date_of_birth,address,phonenumber)


def view_all_users():
    c.execute('SELECT * FROM usersdata')
    data = c.fetchall()
    for row in data:
        tree.insert('',tk.END, values = row)

def get_single_user(firstname):
    c.execute('SELECT * FROM usersdata WHERE firstname="{}"'.format(firstname))
    data = c.fetchall()
    return data

#OTHER FUNTIONS
def clear_text():
    entry_fname.delete('0',END)
    entry_lname.delete('0',END)
    entry_email.delete('0',END)
    entry_age.delete('0',END)
    entry_address.delete('0',END)
    entry_phone.delete('0',END)
    
def add_details():
    firstname = str (entry_fname.get())
    lastname = str (entry_lname.get())
    email = str (entry_email.get())
    age = str  (entry_age.get())
    date_of_birth = str (calendar.get())
    phone = str (entry_phone.get())
    address = str (entry_address.get())
    add_data(firstname,lastname,email,age,date_of_birth,phone,address)
    #print (firstname,lastname,email,age,date_of_birth,phone,address)
    result = 'Nombre:{}, \nApellido:{},\nEmail:{},\nEdad:{},\nF.Nacimiento:{},\nTelefono:{},\nDireccion:{}'.format(firstname,lastname, email, age,date_of_birth,phone,address)
    tab1_display.insert(tk.END, result)
    messagebox.showinfo(title= "Registro GUI", message = "Añadido a la base de datos!")
    #print ('result:', result)

def clear_display_result():
    tab1_display.delete('1.0',END)

def search_user_by_name():
    firstname = str (entry_search.get())
    result = get_single_user(firstname)
    #c.execute('SELECT * FROM usersdata WHERE firstname ="{}"'.format(firstname))
    #data= c.fetchall()
    #print(result)
    tab2_display.insert(tk.END,result)

def clear_searching_view():
    tab2_display.delete('1.0',END)

def clear_display_view():
    tab1_display.delete('1.0',END)

def clear_entered_search():
    entry_search.delete('0',END)

def clear_tree_view():
    #tab2_display.delete('1.0',END)
    tree.delete('1.0',END)


def export_as_csv():
	filename = str(entry_filename.get())
	myfilename = filename + '.csv'
	with open(myfilename, 'w') as f:
	    writer = csv.writer(f)
	    c.execute('SELECT * FROM usersdata')
	    data = c.fetchall()
	    writer.writerow(['firstname','lastname','email','age','date_of_birth','address','phonenumber'])
	    writer.writerows(data)
	    messagebox.showinfo(title = "Registrio GUI", message = '"Exported As {}"'.format(myfilename))

'''def export_as_xls():
    pass'''

def get_products():
        #Cleaning table
        records = tree.get_children()
        for element in records:
            tree.delete(element)
    
def delete_product():

        firstname =tree.item(tree.selection())['values']
        query = 'DELETE FROM usersdata WHERE firstname="{}"'.format(firstname[0])
        result = c.execute(query)
        conn.commit()
        get_products()
        view_all_users()
        
        return result
    	

#Structure & Layout
window  = Tk()
window.title("GYM 4L - System. ")
window.geometry("750x450")
window.iconbitmap('kg.ico')
#window.iconbitmap('C:/Users/Maximiliano Herrera/Desktop/MH_Gym/img/mancuernas.png')
#imagenLabel=PhotoImage(file='python.gif')
#fondo=PhotoImage(file='box.gif')
#lblfondo=Label(window,image=fondo).place(x=0,y=0)
'''load= Image.open('img/box.gif')
render = ImageTk.PhotoImage(load)
img=Label(window,image=render)
img.image =render
img.place(x=0,y=0)
img.pack()'''


style = ttk.Style(window)
style.configure("lefttab.TNotebook", tabposition = 'wn')

#Tab Layout
tab_control = ttk.Notebook(window)#, style = 'lefttab.TNotebook')

#Add Frames
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)


#Add Tabs to Notebook
tab_control.add(tab1, text = f'{"Inicio"}')
tab_control.add(tab2, text = f'{"Ver"}')
tab_control.add(tab3, text = f'{"Buscar"}')
tab_control.add(tab4, text = f'{"Exportar"}')
tab_control.add(tab5, text = f'{"About"}')

tab_control.pack(expand = 1, fill = "both")

create_table()

#Add header labels
label1 = Label(tab1, text = "Bienvenido! Registre un nuevo cliente", padx=5, pady=5)
label1.grid(column=1, row=0)

label2 = Label(tab2, text = "Ver", padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text = "Buscar", padx=5, pady=5)
label3.grid(column=0, row=0)

#label4 = Label(tab4, text = "Export", padx=5, pady=5)
#label4.grid(column=0, row=0)

label5 = Label(tab5, text = "About", padx=5, pady=5)
label5.grid(column=0, row=0)

#Main Home
l1 = Label(tab1,text = "Nombre", padx=5, pady=5)
l1.grid(column = 0 , row = 1)
fname_raw_entry = StringVar()
entry_fname = Entry(tab1, textvariable = fname_raw_entry, width =50 )
entry_fname.grid( column = 1, row = 1) 

l2 = Label(tab1,text = "Apellido", padx=5, pady=5)
l2.grid(column = 0 , row = 2)
lname_raw_entry = StringVar()
entry_lname = Entry(tab1, textvariable = lname_raw_entry, width =50 )
entry_lname.grid( column = 1, row = 2)

l3 = Label(tab1,text = "Email", padx=5, pady=5)
l3.grid(column = 0 , row = 3)
email_raw_entry = StringVar()
entry_email = Entry(tab1, textvariable = email_raw_entry, width =50 )
entry_email.grid( column = 1, row = 3)

l4 = Label(tab1,text = "Edad", padx=5, pady=5)
l4.grid(column = 0 , row = 4)
age_raw_entry = StringVar()
entry_age = Entry(tab1, textvariable = age_raw_entry, width =50 )
entry_age.grid( column = 1, row = 4)

l5 = Label(tab1, text = "Fecha de nacimiento", padx=5, pady=5)
l5.grid(column=0, row=5)
datebirth_raw_entry = StringVar()
calendar = DateEntry(tab1, width=30, textvariable=datebirth_raw_entry,background='grey',foreground='white',borderwidth=4,year=2020)
calendar.grid(column=1, row=5, padx=10, pady=10)

l6 = Label(tab1,text = "Direccion", padx=5, pady=5)
l6.grid(column = 0 , row = 6)
adrss_raw_entry = StringVar()
entry_address= Entry(tab1, textvariable = adrss_raw_entry, width =50 )
entry_address.grid( column = 1, row = 6)

l7 = Label(tab1,text = "Numero de teléfono", padx=5, pady=5)
l7.grid(column = 0 , row = 7)
phnumber_raw_entry = StringVar()
entry_phone = Entry(tab1, textvariable = phnumber_raw_entry, width =50 )
entry_phone.grid( column = 1, row = 7)

button1 = Button(tab1, text="Añadir", width=12,bg="green",fg="white", command = add_details)
button1.grid(row=8, column=1,padx=5, pady=5)


button2 = Button(tab1, text="Eliminar", width=12,bg="red",fg="white", command = clear_text)
button2.grid(row=8, column=0,padx=10, pady=5)


#Display Screen
tab1_display = ScrolledText(tab1, height=5, width= 40)
tab1_display.grid(row=10, column=1,padx=4, pady=5, columnspan=3)
#tab1_display.geometry("200x200")

#xscrollbar = Scrollbar(tab1_display, orient=HORIZONTAL)
#xscrollbar.pack(side=BOTTOM, fill=X)
#tab1_display.config(xscrollcommand = xscrollbar.set)


button3 = Button(tab1, text="Borrar resultado", width=12,bg="red",fg="white", command = clear_display_view)
button3.grid(row=13, column=1,padx=10, pady=10)

#View
#label_view1 = Label(tab2,text= "View", padx =5 ,pady=5)
#label_view1.grid(row=2,column=0)
button_view = Button(tab2, text = "Ver Todos" , width= 12, bg = "green", fg = "white", command= view_all_users )
button_view.grid(row=0, column =0, padx=10, pady=10)
tree= ttk.Treeview(tab2,height=15,column=("column1","column2","column3","column4","column5","column6","column7"),show='headings')
tree.heading("#1",text="Nombre")
tree.heading("#2",text="Apellido")
tree.heading("#3",text="Email")
tree.heading("#4",text="Edad")
tree.heading("#5",text="F.Nacimiento")
tree.heading("#6",text="Direccion")
tree.heading("#7",text="Telefono")
tree.grid(row=10,column=0,columnspan=3,padx=5,pady=5)


#Search
label_search = Label(tab3, text = "Buscar Nombre", padx=5, pady=5)
label_search.grid(row=1, column=0)
search_raw_entry = StringVar()
entry_search = Entry(tab3,textvariable=search_raw_entry, width=30)
entry_search.grid(row=1, column=1)

button_clearsearch = Button(tab3,text="Vaciar",width=12,bg="red",fg="white",command=clear_entered_search)
button_clearsearch.grid(row=2,column=1,padx=10,pady=10)

button_clearresult = Button(tab3,text="Borrar Resultado", width=12,bg="red",fg="white",command=clear_searching_view)
button_clearresult.grid(row=2,column=2,padx=10,pady=10)

button_search = Button(tab3,text="Buscar",width =12,bg="green",fg="white",command=search_user_by_name)
button_search.grid(row=1,column=2,padx=10,pady=10)

tab2_display=ScrolledText(tab3,height=5, width=60)
tab2_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#Export 
label_export1 = Label(tab4,text="File Name",padx=5,pady=5)
label_export1.grid(column=0,row=2)
filename_raw_entry = StringVar()
entry_filename = Entry(tab4,textvariable=filename_raw_entry,width=30)
entry_filename.grid(row=2,column=1)

button_export3 = Button(tab4,text="Export To CSV",width=12,bg='green',fg='#fff',command=export_as_csv)
button_export3.grid(row=3,column=1,padx=10,pady=10)

button_delete = Button(tab2,text="Eliminar Cliente",width=12,bg='red',fg='#fff',command=delete_product)
button_delete.grid(row=14,column=0,padx=10,pady=10)
#About
label_about = Label(tab5, text = "GYM 4L V 0.1.0 \nAgustinmendez.am2@hotmail.com", padx = 5, pady = 5)
label_about.grid(column = 0 , row = 1)



window.mainloop()
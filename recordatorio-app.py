import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
# Create database connection and connect to table
try:
       con = sql.connect('recordatorio_db.db')
       cur = con.cursor()
       cur.execute('''CREATE TABLE notes_table
                        (date text, notes_title text, notes text)''')
except:
       print("Conectado a la Base de Datos")
# Insert a row of data
def add_notes():
       #obtener valores input
       f_aviso = fecha_entry.get()
       texto_titulo = titulo_entry.get()
       texto = texto_entry.get("1.0", "end-1c")
       #crear un prompt para valores faltantes
       if (len(f_aviso) <=0) & (len(texto_titulo)<=0) & (len(texto)<=1):
               messagebox.showerror(message = "Ingrese los detalles requeridos" )
       else:
       #Insert valores a la bd
               cur.execute("INSERT INTO notes_table VALUES ('%s','%s','%s')" %(f_aviso, texto_titulo, texto))
               messagebox.showinfo(message="Recordatorio Agregado")
       #Commit para preservar los cambios
               con.commit()
#Mostrar los recordatorios
def view_notes():
       #Obtener las notas ingresadas
       f_aviso = fecha_entry.get()
       titulo = titulo_entry.get()
       #If no input is given, retrieve all notes
       if (len(f_aviso) <=0) & (len(titulo)<=0):
               sql_statement = "SELECT * FROM notes_table"
              
       #recuperar texto por una titulo
       elif (len(f_aviso) <=0) & (len(texto_titulo)>0):
               sql_statement = "SELECT * FROM notes_table where notes_title ='%s'" %titulo
       #Recuperar texto por una fecha
       elif (len(f_aviso) >0) & (len(texto_titulo)<=0):
               sql_statement = "SELECT * FROM notes_table where date ='%s'"%f_aviso
       #Retrieve notes matching the date and title
       else:
               sql_statement = "SELECT * FROM notes_table where date ='%s' and notes_title ='%s'" %(f_aviso, titulo)
              
       #Execute the query
       cur.execute(sql_statement)
       #Obtain all the contents of the query
       row = cur.fetchall()
       print(row)
       #Check if none was retrieved
       if len(row)<=0:
               messagebox.showerror(message="No se encontro nigun recordatorio")
       else:
               #Print the notes
               for i in row:
                       messagebox.showinfo(message="fecha: "+i[0]+"\nTitulo: "+i[1]+"\nRecordar: "+i[2])
#Delete the notes
def delete_notes():
       #Obtain input values
       f_aviso = fecha_entry.get()
       titulo = titulo_entry.get()
       #Ask if user wants to delete all notes
       choice = messagebox.askquestion(message="Esta seguro de borrar la nota?")
       #If yes is selected, delete all
       if choice == 'yes':
               sql_statement = "DELETE FROM notes_table" 
       else:
       #Delete notes matching a particular date and title
               if (len(f_aviso) <=0) & (len(titulo)<=0): 
                       #Raise error for no inputs
                       messagebox.showerror(message = "Ingrese los detalles requeridos" )
                       return
               else:
                      sql_statement = "DELETE FROM notes_table where date ='%s' and notes_title ='%s'" %(f_aviso, titulo)
       #Execute the query
       cur.execute(sql_statement)
       messagebox.showinfo(message="Recordatorio(s) Borrado")
       con.commit()
#Update the notes
def update_notes():
       #Obtain user input
       f_aviso = fecha_entry.get()
       titulo = titulo_entry.get()
       texto = texto_entry.get("1.0", "end-1c")
       #Check if input is given by the user
       if (len(f_aviso) <=0) & (len(titulo)<=0) & (len(texto)<=1):
               messagebox.showerror(message = "Ingrese los detalles requeridos" )
       #update the note
       else:
               sql_statement = "UPDATE notes_table SET notes = '%s' where date ='%s' and notes_title ='%s'" %(texto, f_aviso, titulo)
              
       cur.execute(sql_statement)
       messagebox.showinfo(message="Recordatorio actualizado")
       con.commit()


       
#Invoke call to class to view a window
#llamar una class para ver una ventana
window = Tk()
#setear las dimensiones de la ventana y el nombre
window.geometry("500x300")
window.title("recordatorio - RSam")
 
titulo_label = Label(window, text="Recordatorio - RSam").pack()

#Leer inputs
#Datos input
fecha_label = Label(window, text="fecha:").place(x=10,y=20)
fecha_entry = Entry(window,  width=20)
fecha_entry.place(x=50,y=20)
#titulo recordatorio input
titulo_label = Label(window, text="titulo:").place(x=10,y=50)
titulo_entry = Entry(window,  width=30)
titulo_entry.place(x=80,y=50)
#texto input
texto_label = Label(window, text="Nota:").place(x=10,y=90)
texto_entry = Text(window, width=50,height=5)
texto_entry.place(x=60,y=90)
 
#Perform notes functions
button1 = Button(window,text='Agregar Nota', bg = 'Turquoise',fg='Red',command=add_notes).place(x=10,y=190)
button2 = Button(window,text='Mostrar Nota', bg = 'Turquoise',fg='Red',command=view_notes).place(x=110,y=190)
button3 = Button(window,text='Borarr Nota', bg = 'Turquoise',fg='Red',command=delete_notes).place(x=210,y=190)
button4 = Button(window,text='Actualizar Nota', bg = 'Turquoise',fg='Red',command=update_notes).place(x=320,y=190)
 
#close the app
window.mainloop()
con.close()

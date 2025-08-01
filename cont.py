import tkinter as tk
from tkinter import messagebox
import sqlite3

# DB Setup
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
''')
conn.commit()

# Functions
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name == "" or phone == "":
        messagebox.showwarning("Warning", "Name and Phone are required!")
        return

    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Contact added successfully!")
    clear_fields()
    view_contacts()

def view_contacts():
    contact_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts")
    for row in cursor.fetchall():
        contact_list.insert(tk.END, f"{row[0]} - {row[1]} | {row[2]}")

def search_contact():
    query = search_entry.get()
    contact_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    for row in cursor.fetchall():
        contact_list.insert(tk.END, f"{row[0]} - {row[1]} | {row[2]}")

def delete_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact to delete.")
        return
    contact_id = contact_list.get(selected[0]).split(" - ")[0]
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    messagebox.showinfo("Success", "Contact deleted!")
    view_contacts()

def update_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact to update.")
        return
    contact_id = contact_list.get(selected[0]).split(" - ")[0]
    cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                   (name_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get(), contact_id))
    conn.commit()
    messagebox.showinfo("Success", "Contact updated!")
    clear_fields()
    view_contacts()

def fill_fields(event):
    selected = contact_list.curselection()
    if not selected:
        return
    contact_id = contact_list.get(selected[0]).split(" - ")[0]
    cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
    contact = cursor.fetchone()
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

    name_entry.insert(0, contact[1])
    phone_entry.insert(0, contact[2])
    email_entry.insert(0, contact[3])
    address_entry.insert(0, contact[4])

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x600")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Address").pack()
address_entry = tk.Entry(root)
address_entry.pack()

tk.Button(root, text="Add Contact", command=add_contact).pack(pady=5)
tk.Button(root, text="Update Contact", command=update_contact).pack(pady=5)
tk.Button(root, text="Delete Contact", command=delete_contact).pack(pady=5)

tk.Label(root, text="Search by Name/Phone").pack()
search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root, text="Search", command=search_contact).pack(pady=5)
tk.Button(root, text="Show All Contacts", command=view_contacts).pack(pady=5)

contact_list = tk.Listbox(root, width=60)
contact_list.pack(pady=10)
contact_list.bind('<<ListboxSelect>>', fill_fields)

view_contacts()
root.mainloop()

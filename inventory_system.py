import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
con=sqlite3.connect("inventory.db");cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE,category TEXT,price REAL,stock INTEGER)")
con.commit()
def refresh():
    for i in tree.get_children():tree.delete(i)
    for r in cur.execute("SELECT name,category,price,stock FROM products ORDER BY name"):tree.insert("", "end", values=r)
def add():
    try:
        cur.execute("INSERT INTO products(name,category,price,stock) VALUES(?,?,?,?)",(name.get(),cat.get(),float(price.get()),int(stock.get())));con.commit();refresh()
    except (ValueError,sqlite3.IntegrityError):messagebox.showerror("Error","Check values or use a unique product name.")
def update_stock(delta):
    s=tree.selection()
    if not s:return
    n=tree.item(s[0])["values"][0];cur.execute("UPDATE products SET stock=MAX(0,stock+?) WHERE name=?",(delta,n));con.commit();refresh()
root=tk.Tk();root.title("Inventory Management System");root.geometry("800x500")
name=tk.StringVar();cat=tk.StringVar();price=tk.StringVar();stock=tk.StringVar()
f=tk.Frame(root);f.pack(pady=10)
for lab,var in [("Product",name),("Category",cat),("Price",price),("Stock",stock)]:
    tk.Label(f,text=lab).pack(side="left");tk.Entry(f,textvariable=var,width=13).pack(side="left",padx=3)
tk.Button(f,text="Add",command=add).pack(side="left");tk.Button(f,text="+1 Stock",command=lambda:update_stock(1)).pack(side="left");tk.Button(f,text="-1 Stock",command=lambda:update_stock(-1)).pack(side="left")
tree=ttk.Treeview(root,columns=("Product","Category","Price","Stock"),show="headings")
for c in ("Product","Category","Price","Stock"):tree.heading(c,text=c)
tree.pack(fill="both",expand=True,padx=10,pady=10);refresh();root.mainloop()

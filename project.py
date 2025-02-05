import tkinter as tk
from tkinter import messagebox
import cx_Oracle
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Oracle connection parameters
username = 'hr'
password = 'hr'
hostname = 'localhost'
port = 1521
sid = 'XE'

# Create connection string
dsn_tns = cx_Oracle.makedsn(hostname, port, sid=sid)

# Function to handle the saree purchase process
def purchase_saree():
    saree_type = saree_type_combobox.get()
    color = color_combobox.get()
    border_type = border_type_combobox.get()
    price = price_scale.get()

    # Validate inputs
    if not saree_type or not color or not border_type:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        # Connect to the Oracle database
        connection = cx_Oracle.connect(username, password, dsn_tns)
        cursor = connection.cursor()

        # Insert data into the saree_selection table
        cursor.execute("""
            INSERT INTO saree_selection (saree_id, saree_type, color, border_type, price)
            VALUES (saree_selection_seq.NEXTVAL, :1, :2, :3, :4)
        """, (saree_type, color, border_type, price))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Show success message
        messagebox.showinfo("Success", "Saree purchased successfully!")

    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Create the main window with ttkbootstrap theme
root = ttk.Window(themename="flatly")
root.title("Saree Selection")
root.geometry("600x500")
root.resizable(False, False)

# Header label
header_label = ttk.Label(root, text="Saree Selection", font=("Arial", 18, "bold"), bootstyle=PRIMARY)
header_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create frame for form inputs
form_frame = ttk.Frame(root)
form_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Create Saree Type dropdown
label_saree_type = ttk.Label(form_frame, text="Saree Type:", font=("Arial", 12))
label_saree_type.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
saree_type_combobox = ttk.Combobox(form_frame, values=["Silk", "Cotton", "Georgette"], font=("Arial", 12))
saree_type_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)

# Create Color dropdown
label_color = ttk.Label(form_frame, text="Color:", font=("Arial", 12))
label_color.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
color_combobox = ttk.Combobox(form_frame, values=["Red", "Blue", "Green"], font=("Arial", 12))
color_combobox.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)

# Create Border Type dropdown
label_border_type = ttk.Label(form_frame, text="Border Type:", font=("Arial", 12))
label_border_type.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
border_type_combobox = ttk.Combobox(form_frame, values=["Gold", "Silver", "None"], font=("Arial", 12))
border_type_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)

# Create Price scale
label_price = ttk.Label(form_frame, text="Price:", font=("Arial", 12))
label_price.grid(row=3, column=0, padx=12, pady=12, sticky=tk.W)
price_scale = ttk.Scale(form_frame, from_=1000, to=5000, orient=tk.HORIZONTAL, bootstyle="primary")
price_scale.grid(row=3, column=1, padx=10, pady=10, sticky=tk.EW)
label_price_value = ttk.Label(form_frame, text="₹1000", font=("Arial", 12), bootstyle=SECONDARY)
label_price_value.grid(row=3, column=2, padx=12, pady=12)

# Update price value when scale changes
def update_price_value(val):
    label_price_value.config(text=f"₹{int(val)}")

price_scale.bind("<Motion>", lambda event: update_price_value(price_scale.get()))

# Create a Purchase button
button_purchase = ttk.Button(root, text="Purchase Saree", command=purchase_saree, bootstyle=SUCCESS)
button_purchase.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.EW)

# Configure grid weights for responsive design
root.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()

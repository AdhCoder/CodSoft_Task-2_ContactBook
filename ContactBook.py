import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from ttkthemes import ThemedTk

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        # Create and set the theme
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")  
        
        # Initialize variables
        self.contacts = []

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Contact Information Frame
        contact_info_frame = ttk.LabelFrame(self.root, text="Contact Information")
        contact_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(contact_info_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(contact_info_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(contact_info_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(contact_info_frame, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = ttk.Entry(contact_info_frame)
        self.phone_entry = ttk.Entry(contact_info_frame)
        self.email_entry = ttk.Entry(contact_info_frame)
        self.address_entry = ttk.Entry(contact_info_frame)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        ttk.Button(contact_info_frame, text="Add Contact", command=self.add_contact).grid(row=4, column=1, pady=10)

        # Contact List Frame
        contact_list_frame = ttk.LabelFrame(self.root, text="Contact List")
        contact_list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Treeview to display contact list
        self.contact_tree = ttk.Treeview(contact_list_frame, columns=("Name", "Phone"))
        self.contact_tree.heading("#0", text="ID")
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone", text="Phone")
        self.contact_tree.column("#0", width=30, anchor="center")
        self.contact_tree.column("Name", width=150)
        self.contact_tree.column("Phone", width=100)
        self.contact_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

     

        # Scrollbar
        scrollbar = ttk.Scrollbar(contact_list_frame, orient="vertical", command=self.contact_tree.yview)
        self.contact_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons
        ttk.Button(contact_list_frame, text="View Contacts", command=self.view_contacts).grid(row=1, column=0, pady=10, sticky="ew")
        ttk.Button(contact_list_frame, text="Search Contact", command=self.search_contact).grid(row=1, column=1, pady=10, sticky="ew")
        ttk.Button(contact_list_frame, text="Update Contact", command=self.update_contact).grid(row=1, column=2, pady=10, sticky="ew")
        ttk.Button(contact_list_frame, text="Delete Contact", command=self.delete_contact).grid(row=1, column=3, pady=10, sticky="ew")

        # Make the frames expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        contact_id = len(self.contacts) + 1
        self.contacts.append({"id": contact_id, "name": name, "phone": phone, "email": email, "address": address})

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

        self.view_contacts()

    def view_contacts(self):
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)

        for contact in self.contacts:
            self.contact_tree.insert("", "end", text=contact["id"], values=(contact["name"], contact["phone"]))

    def search_contact(self):
        search_query = simpledialog.askstring("Search Contact", "Enter name or phone number:")

        if search_query:
            results = []
            for contact in self.contacts:
                if search_query.lower() in contact["name"].lower() or search_query in contact["phone"]:
                    results.append(contact)

            if results:
                messagebox.showinfo("Search Results", f"Found {len(results)} contact(s).")
                self.display_search_results(results)
            else:
                messagebox.showinfo("Search Results", "No matching contacts found.")

    def display_search_results(self, results):
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)

        for contact in results:
            self.contact_tree.insert("", "end", text=contact["id"], values=(contact["name"], contact["phone"]))

    def update_contact(self):
        selected_item = self.contact_tree.selection()

        if not selected_item:
            messagebox.showwarning("Update Contact", "Please select a contact to update.")
            return

        contact_id = int(self.contact_tree.item(selected_item, "text"))
        selected_contact = next((contact for contact in self.contacts if contact["id"] == contact_id), None)

        if selected_contact:
            updated_name = simpledialog.askstring("Update Contact", "Enter updated name:", initialvalue=selected_contact["name"])
            updated_phone = simpledialog.askstring("Update Contact", "Enter updated phone number:", initialvalue=selected_contact["phone"])
            updated_email = simpledialog.askstring("Update Contact", "Enter updated email:", initialvalue=selected_contact["email"])
            updated_address = simpledialog.askstring("Update Contact", "Enter updated address:", initialvalue=selected_contact["address"])

            selected_contact["name"] = updated_name if updated_name else selected_contact["name"]
            selected_contact["phone"] = updated_phone if updated_phone else selected_contact["phone"]
            selected_contact["email"] = updated_email if updated_email else selected_contact["email"]
            selected_contact["address"] = updated_address if updated_address else selected_contact["address"]

            self.view_contacts()

    def delete_contact(self):
        selected_item = self.contact_tree.selection()

        if not selected_item:
            messagebox.showwarning("Delete Contact", "Please select a contact to delete.")
            return

        contact_id = int(self.contact_tree.item(selected_item, "text"))
        self.contacts = [contact for contact in self.contacts if contact["id"] != contact_id]

        self.view_contacts()

if __name__ == "__main__":
    root = ThemedTk(theme="clam") 
    app = ContactBookApp(root)
    root.mainloop()
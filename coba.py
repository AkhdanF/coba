import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class MoneyManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Money Management App")
        self.master.geometry("600x400")

        self.balance = 0.0
        self.transactions = []  

        self.balance_label = tk.Label(self.master, text="Balance: $0.00", font=("Arial", 14))
        self.balance_label.pack(pady=10)

        self.name_label = tk.Label(self.master, text="Name:", font=("Arial", 12))
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.master, width=20, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.amount_label = tk.Label(self.master, text="Amount:", font=("Arial", 12))
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(self.master, width=20, font=("Arial", 12))
        self.amount_entry.pack(pady=5)

        self.add_income_button = tk.Button(self.master, text="Add Income", command=self.add_income, font=("Arial", 12))
        self.add_income_button.pack(pady=5)

        self.add_expense_button = tk.Button(self.master, text="Add Expense", command=self.add_expense, font=("Arial", 12))
        self.add_expense_button.pack(pady=5)

        self.tree = ttk.Treeview(self.master, columns=("Name", "Amount", "Type"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.pack(pady=10)
        
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="your_user",
            password="your_password",
            database="money_management"
        )

        self.cursor = self.db_connection.cursor()
        
        self.create_table()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                type VARCHAR(10) NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

    def add_income(self):
        self.add_transaction("Income")

    def add_expense(self):
        self.add_transaction("Expense")

    def add_transaction(self, transaction_type):
        try:
            name = self.name_entry.get()
            amount = float(self.amount_entry.get())


            self.balance += amount
            self.transactions.append({"Name": name, "Amount": amount, "Type": transaction_type})
            
            self.cursor.execute("INSERT INTO transactions (name, amount, type) VALUES (%s, %s, %s)",
                                (name, amount, transaction_type))
            self.db_connection.commit()

            self.update_balance_label()
            self.update_transaction_table()

            self.name_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_transaction_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for transaction in self.transactions:
            if transaction["Type"] == "Income":
                bg_color = "#B2FF66"
                font_color = "#000000"
            else:
                bg_color = "#FF6666"
                font_color = "#000000"

            self.tree.insert("", "end", values=(transaction["Name"], f"${transaction['Amount']:.2f}", transaction["Type"]), tags=(transaction["Type"],), iid=transaction["Type"])

            self.tree.tag_configure(transaction["Type"], background=bg_color, foreground=font_color)
            
    def __del__(self):
        self.cursor.close()
        self.db_connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = MoneyManagementApp(root)
    root.mainloop()

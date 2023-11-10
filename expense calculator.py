import tkinter as tk
from tkinter import ttk
from tkinter import Entry, Label, Button, Listbox, Scrollbar
import calendar

# Initialize an empty list to store expenses
expenses = []

def record_expense():
    date = date_entry.get()
    description = desc_entry.get()
    amount = int(amount_entry.get())  # Convert to an integer
    expense = {
        "Date": date,
        "Description": description,
        "Amount": amount
    }
    expenses.append(expense)
    update_expense_listbox()
    clear_input_fields()

def clear_input_fields():
    date_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def update_expense_listbox():
    expense_listbox.delete(0, tk.END)
    for expense in expenses:
        date = expense['Date']
        amount = "₹{:d}".format(expense['Amount'])  # Change currency symbol to ₹
        description = expense['Description']
        expense_listbox.insert(tk.END, f"{date} - {description} - {amount}")

def edit_expense():
    selected_index = expense_listbox.curselection()
    if not selected_index:
        return
    selected_index = selected_index[0]
    # Retrieve the selected expense
    selected_expense = expenses[selected_index]
    date_entry.delete(0, tk.END)
    date_entry.insert(tk.END, selected_expense["Date"])
    desc_entry.delete(0, tk.END)
    desc_entry.insert(tk.END, selected_expense["Description"])
    amount_entry.delete(0, tk.END)
    amount_entry.insert(tk.END, selected_expense["Amount"])
    # Remove the selected expense from the list
    expenses.pop(selected_index)
    update_expense_listbox()

def delete_expense():
    selected_index = expense_listbox.curselection()
    if not selected_index:
        return
    selected_index = selected_index[0]
    # Remove the selected expense from the list
    expenses.pop(selected_index)
    update_expense_listbox()

def generate_report():
    if not expenses:
        result_label.config(text="No expenses to generate a report for.")
        return
    # Initialize dictionaries for monthly and yearly reports
    monthly_report = {}
    yearly_report = {}
    for expense in expenses:
        date = expense["Date"]
        year, month, _ = map(int, date.split('/'))
        amount = expense["Amount"]
        # Update monthly report
        if year not in yearly_report:
            yearly_report[year] = 0
        yearly_report[year] += amount
        # Update yearly report
        if year not in monthly_report:
            monthly_report[year] = {}
        if month not in monthly_report[year]:
            monthly_report[year][month] = 0
        monthly_report[year][month] += amount
    result_text = "Yearly Report:\n"
    for year, total in yearly_report.items():
        result_text += f"{year}: ₹{total}\n"
    result_text += "\nMonthly Report:\n"
    for year, months in monthly_report.items():
        for month, total in months.items():
            month_name = calendar.month_name[month]
            result_text += f"{month_name} {year}: ₹{total}\n"
    result_label.config(text=result_text)

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Input fields and labels
date_label = Label(root, text="Date (DD/MM/YYYY):")
date_label.pack()
date_entry = Entry(root)
date_entry.pack()
desc_label = Label(root, text="Description:")
desc_label.pack()
desc_entry = Entry(root)
desc_entry.pack()
amount_label = Label(root, text="Amount (₹):")
amount_label.pack()
amount_entry = Entry(root)
amount_entry.pack()

# Buttons
record_button = Button(root, text="Record Expense", command=record_expense)
record_button.pack()
edit_button = Button(root, text="Edit Expense", command=edit_expense)
edit_button.pack()
delete_button = Button(root, text="Delete Expense", command=delete_expense)
delete_button.pack()
generate_button = Button(root, text="Generate Report", command=generate_report)
generate_button.pack()

# Expense list
expense_list_label = Label(root, text="Expenses:")
expense_list_label.pack()
expense_listbox = Listbox(root, selectmode=tk.SINGLE, width=40)
expense_listbox.pack()

# Add a scrollbar for the expense list
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
expense_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=expense_listbox.yview)

# Result label
result_label = Label(root, text="")
result_label.pack()

root.mainloop()

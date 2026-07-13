import csv
from matplotlib import pyplot as plt
from datetime import datetime
from pathlib import Path

File_Name = "Transactions.csv"


def initialize_file():
    file_path = Path(File_Name)
    if not file_path.exists():
        with open(File_Name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["date", "type", "category", "description", "amount"])

def add_transaction():
    transactionType = input("Enter transaction type (income/expense): ").strip().lower()    

    if transactionType not in ['income', 'expense']:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return
    
    category = input("Enter transaction category: ").strip()
    description = input("Enter transaction description: ").strip()

    try:
        amount = float(input("Enter transaction amount: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    
    date = datetime.now().strftime("%Y-%m-%d")

    with open(File_Name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, transactionType, category, description, amount])

    print("Transaction added successfully.")


def view_transactions():
    with open(File_Name, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        print("\nDate | Type | Category | Description | Amount")
        print("-" * 60)

        for row in reader:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | ${row[4]}")

def edit_transaction():
    view_transactions()
    transaction_id = input("Enter the date of the transaction to edit (YYYY-MM-DD): ").strip()

    transactions = []
    edited = False

    with open(File_Name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["date"] == transaction_id:
                print(f"Editing transaction: {row}")
                new_type = input(f"Enter new type (income/expense) [{row['type']}]: ").strip().lower() or row["type"]
                new_category = input(f"Enter new category [{row['category']}]: ").strip()
                new_description = input(f"Enter new description [{row['description']}]: ").strip()
                new_amount = input(f"Enter new amount [{row['amount']}]: ").strip()
                edited = True
                row["type"] = new_type
                row["category"] = new_category if new_category else row["category"]
                row["description"] = new_description if new_description else row["description"]
                row["amount"] = new_amount if new_amount else row["amount"]
            transactions.append(row)

        if edited:
            with open(File_Name, "w", newline="") as csvfile:
                fieldnames = ["date", "type", "category", "description", "amount"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(transactions)

def delete_transaction():
    view_transactions()
    transaction_id = input("Enter the date of the transaction to delete (YYYY-MM-DD): ").strip()

    transactions = []
    deleted = False

    with open(File_Name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["date"] == transaction_id:
                deleted = True
                continue
            transactions.append(row)

    if deleted:
        with open(File_Name, "w", newline="") as csvfile:
            fieldnames = ["date", "type", "category", "description", "amount"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        print("Transaction deleted successfully.")
    else:
        print("Transaction not found.")

def show_summary():
    income = 0
    expenses = 0

    with open(File_Name, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            amount = float(row["amount"])

            if row["type"] == "income":
                income += amount
            elif row["type"] == "expense":
                expenses += amount

    balance = income - expenses

    print("\nFinance Summary")
    print("-" * 30)
    print(f"Total Income:   ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Balance:        ${balance:.2f}")

def monthly_summary():
    month = input("Enter the month for summary (YYYY-MM): ").strip()
    income = 0
    expenses = 0

    with open(File_Name, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["date"].startswith(month):
                amount = float(row["amount"])
                if row["type"] == "income":
                    income += amount
                elif row["type"] == "expense":
                    expenses += amount

    balance = income - expenses

    print(f"\nMonthly Summary for {month}")
    print("-" * 30)
    print(f"Total Income:   ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Balance:        ${balance:.2f}")

def barchart_summary():
    month = input("Enter the month for bar chart summary (YYYY-MM): ").strip()
    categories = {}

    with open(File_Name, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["date"].startswith(month):
                category = row["category"]
                amount = float(row["amount"])
                if row["type"] == "expense":
                    categories[category] = categories.get(category, 0) + amount
                if row["type"] == "income":
                    categories[category] = categories.get(category, 0) + amount

    if categories:
        plt.figure(figsize=(10, 6))
        plt.bar(categories.keys(), categories.values())
        plt.xlabel("Categories")
        plt.ylabel("Amount")
        plt.title(f"Monthly Summary for {month}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No transactions found for {month}.")

def main():
    initialize_file()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Edit transaction")
        print("4. Delete transaction")
        print("5. Show summary")
        print("6. Monthly summary")
        print("7. Bar chart summary")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            edit_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            show_summary()
        elif choice == "6":
            monthly_summary()
        elif choice == "7":
            barchart_summary()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
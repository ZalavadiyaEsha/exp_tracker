import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
FILE = "expenses.csv"
class ExpenseTracker:
    def __init__(self):
        if os.path.exists(FILE):
            self.data = pd.read_csv(FILE)
        else:
            self.data = pd.DataFrame(
                columns=["Date", "Amount", "Category", "Description"]
            )
            self.data.to_csv(FILE, index=False)
        if not self.data.empty:
            self.data["Amount"] = pd.to_numeric(
                self.data["Amount"], errors="coerce"
            )
            self.data = self.data.dropna(subset=["Amount"])
    def add_expense(self, date, amount, category, description):
        new_expense = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        self.data.loc[len(self.data)] = new_expense
        self.data.to_csv(FILE, index=False)
        print("Expense added successfully!")
    def get_summary(self):
        if self.data.empty:
            print("No expenses found.")
            return
        amounts = self.data["Amount"].to_numpy()
        print("Total Expense:", np.sum(amounts))
        print("Average Expense:", np.mean(amounts))
        print("\nCategory-wise Expenses:")
        print(self.data.groupby("Category")["Amount"].sum())
    def filter_expenses(self, condition):
        if condition == "category":
            category = input("Enter category: ").strip()
            result = self.data[
                self.data["Category"].str.lower() == category.lower()
            ]
        elif condition == "date":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            result = self.data[self.data["Date"] == date]
        elif condition == "amount":
            amount = float(input("Enter minimum amount: "))
            result = self.data[self.data["Amount"] >= amount]
        else:
            print("Invalid filter.")
            return
        if result.empty:
            print("No matching expenses found.")
        else:
            print(result.to_string(index=False))
    def generate_report(self):
        if self.data.empty:
            print("No expenses found.")
            return
        print("\n----- EXPENSE REPORT -----")
        print("Total:", self.data["Amount"].sum())
        print("Average:", self.data["Amount"].mean())
        print("Number of Expenses:", len(self.data))
        print("\nCategory-wise Report:")
        print(self.data.groupby("Category")["Amount"].sum())
        dates = pd.to_datetime(self.data["Date"], errors="coerce")
        monthly_data = self.data.copy()
        monthly_data["Month"] = dates.dt.to_period("M")
        print("\nMonthly Expenses:")
        print(monthly_data.groupby("Month")["Amount"].sum())
    def show_graphs(self):
        if self.data.empty:
            print("No expenses to display.")
            return
        category = self.data.groupby("Category")["Amount"].sum()
        category.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()
        graph_data = self.data.copy()
        graph_data["Date"] = pd.to_datetime(graph_data["Date"], errors="coerce")
        graph_data = graph_data.dropna(subset=["Date"])
        monthly = graph_data.groupby(
            graph_data["Date"].dt.to_period("M").astype(str)
        )["Amount"].sum()
        if not monthly.empty:
            monthly.plot(kind="line", marker="o")
            plt.title("Monthly Expenses")
            plt.xlabel("Month")
            plt.ylabel("Amount")
            plt.tight_layout()
            plt.show()
        category.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Expense Percentage")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
        sns.histplot(data=self.data, x="Amount", bins=5)
        plt.title("Expense Amount Distribution")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
def main():
    tracker = ExpenseTracker()
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Summary")
        print("4. Filter Expenses")
        print("5. Generate Report")
        print("6. Show Graphs")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            try:
                date = input("Enter date (YYYY-MM-DD): ").strip()
                date = pd.to_datetime(
                    date, format="%Y-%m-%d", errors="raise"
                ).strftime("%Y-%m-%d")
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                category = input("Enter category: ").strip()
                if category == "":
                    print("Category cannot be empty.")
                    continue
                description = input("Enter description: ").strip()
                tracker.add_expense(date, amount, category, description)
            except ValueError:
                print("Please enter a valid date and amount.")
        elif choice == "2":
            if tracker.data.empty:
                print("No expenses found.")
            else:
                print(tracker.data.to_string(index=False))
        elif choice == "3":
            tracker.get_summary()
        elif choice == "4":
            print("1. Category")
            print("2. Date")
            print("3. Amount")
            option = input("Choose filter: ").strip()
            if option == "1":
                tracker.filter_expenses("category")
            elif option == "2":
                tracker.filter_expenses("date")
            elif option == "3":
                try:
                    tracker.filter_expenses("amount")
                except ValueError:
                    print("Please enter a valid amount.")
            else:
                print("Invalid option.")
        elif choice == "5":
            tracker.generate_report()
        elif choice == "6":
            tracker.show_graphs()
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Try again.")
if __name__ == "__main__":
    main()
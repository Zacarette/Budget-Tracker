# TODO:
# Go back button
# Edit database system
# Add output if no values in display_exense and display_income
# Change date input format
# Search feature by date and name
# Sort by $ high to low and low to high, and date recent to past and past to recent
# Change how many database entries are showed to the user by default when they select the menu option

import sqlite3 # Import SQLite3 to interact with databases
import datetime # Import datetime to get current date

connection = sqlite3.connect("Budget_Tracker.db") # Create or connect to database with that file name

cursor = connection.cursor() # Create cursor object to execute SQL commands on the database

# ----- Dev Note -----
# Uncomment the following code to reset databases for testing purposes
# cursor.execute("DROP TABLE IF EXISTS Income_Tracker")
# cursor.execute("DROP TABLE IF EXISTS Expense_Tracker")
# cursor.execute("DROP TABLE IF EXISTS Totals_and_Balance")
# connection.commit()

# Create expense tracker table or connect to it
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Expense_Tracker (" \
    "Expense_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
    "Expense_Type TEXT," \
    "Expense_Amount REAL," \
    "Entry_Date TEXT)"
)

# Create income tracker table or connect to it
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Income_Tracker (" \
    "Income_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
    "Income_Type TEXT," \
    "Income_Amount REAL," \
    "Entry_Date TEXT)"
)

# Create totals and balance table or connect to it
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Totals_and_Balance (" \
    "Type TEXT PRIMARY KEY," \
    "Total_Income REAL," \
    "Total_Expense REAL," \
    "Total_Remaining REAL," \
    "As_of TEXT)"
)

# Main menu loop
def run_interface():
    
    while True:

        # Prompt user for menu selection  
        try:
            print("\nWhich menu you would like to navigate to?")
            user_selection = int(input("1. Log expense\n2. Log income\n3. View expense\n4. View income\n5. View Balance\n6. Exit\n\nEnter corresponding number here: "))

            # Match input that user selected
            match user_selection:
                case 1:
                    expense_inputs()
                case 2:
                    income_inputs()
                case 3:
                    display_expense()
                case 4:
                    display_income()
                case 5:
                    display_totals()
                case 6:
                    return
                case _:
                    print("\nInvalid input. Please enter a number from the menu.") # Handles int inputs not 1-6

        # Handles non-int input
        except ValueError:
            print("\nInvalid input. Please enter a number from the menu.")

# Get expense inputs
def expense_inputs():

    while True:

        # Prompt user for separate expense values
        try:
            expense_amounts = int(input("\nHow many separate expense values would you like to track?: "))
            break

        # Handles non-int input
        except ValueError: 
            print("\nInvalid input. Please enter a number.") 

    for i in range(expense_amounts):
            
        while True:

            # Prompt user for expense name and amount, then rounds it to hundreths and gets current date
            try:
                expense_type = input(f"\nEnter the name of expense {i+1}: ")
                individual_expenses = float(input(f"Enter the expense amount from {expense_type}: $"))
                rounded_expense = round(individual_expenses, 2)
                expense_entry_date = datetime.date.today().strftime("%m/%d/%Y")

                # Inserts expense info into database and commits
                cursor.execute(
                    "INSERT INTO Expense_Tracker (Expense_Type, Expense_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (expense_type, rounded_expense, expense_entry_date)
                )
                connection.commit()
                
                # Output expense input to user via CLI
                print("\n-----Expense Added-----")
                print("Name:", expense_type)
                print("Amount:", rounded_expense)
                print("Date:", expense_entry_date)
                print("-----------------------")
                break

            # Handles non-int input
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")
    
    # Updates totals in database and pauses for user to view  
    update_in_background()
    input("\nPress Enter to return to menu...")

# Get income inputs 
def income_inputs():
            
    while True:

        # Prompts user for separate income values
        try: 
            income_amounts = int(input("\nHow many separate income values would you like to track?: "))
            break

        # Handles non-int input
        except ValueError:
            print("\nInvalid input. Please enter a number.")

    for i in range(income_amounts):

        while True:
            
            # Prompt user for income name and amount, then rounds it to hundreths and gets current date
            try:
                income_type = input(f"\nEnter the name income {i+1}: ")
                individual_incomes = float(input(f"Enter the income you received from {income_type}: $"))
                rounded_income = round(individual_incomes, 2)
                income_entry_date = datetime.date.today().strftime("%m/%d/%Y")
                
                # Inserts income info into database and commits
                cursor.execute(
                    "INSERT INTO Income_Tracker (Income_Type, Income_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (income_type, rounded_income, income_entry_date)
                )
                connection.commit()

                # Output income input to user via CLI
                print("\n-----Income Added-----")
                print("Name:", income_type)
                print("Amount:", rounded_income)
                print("Date:", income_entry_date)
                print("-----------------------")
                break
            
            # Handles non-int input
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")
    
    # Updates totals in database and pauses for user to view          
    update_in_background()
    input("\nPress Enter to return to menu...")

# Calculate totals and remaining balance
def do_total_calculations():

    today = datetime.date.today().strftime("%m/%d/%Y")

    # Calculate total income and expense from databases; defaults to 0 if null
    income_sum = cursor.execute(
        "SELECT SUM(Income_Amount) FROM Income_Tracker"
    ).fetchone()[0] or 0
    expense_sum = cursor.execute(
        "SELECT SUM(Expense_Amount) FROM Expense_Tracker"
    ).fetchone()[0] or 0

    remaining_balance = income_sum - expense_sum

    # Insert totals and balance in database and commit
    cursor.execute(
        "INSERT OR REPLACE INTO Totals_and_Balance (Type, Total_Income, Total_Expense, Total_Remaining, As_of) VALUES ('Totals', ?, ? , ?, ?)",
        (income_sum, expense_sum, remaining_balance, today)
    )
    connection.commit()

    return income_sum, expense_sum, remaining_balance

# Auto updates total and balance database after inputs in income and expense
def update_in_background():

    do_total_calculations()

# Displays current totals and balance to user
def display_totals():
    
    income_sum, expense_sum, remaining_balance = do_total_calculations() # Get updated totals

    # Output total and balance info to user via CLI
    print("\nYour total income is:" , f"${income_sum:,.2f}")
    print("Your total expenses are:" , f"${expense_sum:,.2f}")
    print("Your remaining balance after expenses is:" , f"${remaining_balance:,.2f}")
    input("\nPress Enter to return to menu...")

# Displays income entries from database to user
def display_income():
    
    # Get number of income entries
    income_id_amount = cursor.execute(
        "SELECT COUNT(Income_ID) FROM Income_Tracker"
    ).fetchone()[0]
    
    # Fetch all income data
    column_income_name = cursor.execute(
        "SELECT Income_Type FROM Income_Tracker"
    ).fetchall()
    column_income_amount = cursor.execute(
        "SELECT Income_Amount FROM Income_Tracker"
    ).fetchall()
    column_income_date = cursor.execute(
        "SELECT Entry_Date FROM Income_Tracker"
    ).fetchall()

    # Loop and display data from each entry
    for i in range (income_id_amount):
        income_name = column_income_name[i][0]
        income_amount = column_income_amount[i][0]
        format_income_amount = f"${income_amount:,.2f}"
        income_date = column_income_date[i][0]

        print(f"\n-------Income ID: {i+1}-------")
        print(f"Income Name: {income_name}")
        print(f"Income Amount: {format_income_amount}")
        print(f"Entry Date: {income_date}")
        print("--------------------------")

    input("\nPress Enter to return to menu...")

# Displays expense entries from database to user
def display_expense():
    
    # Get number of expense entries
    expense_id_amount = cursor.execute(
        "SELECT COUNT(Expense_ID) FROM Expense_Tracker"
    ).fetchone()[0]
    
    # Fetch all expense data
    column_expense_name = cursor.execute(
        "SELECT Expense_Type FROM Expense_Tracker"
    ).fetchall()
    column_expense_amount = cursor.execute(
        "SELECT Expense_Amount FROM Expense_Tracker"
    ).fetchall()
    column_expense_date = cursor.execute(
        "SELECT Entry_Date FROM Expense_Tracker"
    ).fetchall()

    # Loop and display data from each entry
    for i in range (expense_id_amount):
        expense_name = column_expense_name[i][0]
        expense_amount = column_expense_amount[i][0]
        format_expense_amount = f"${expense_amount:,.2f}"
        expense_date = column_expense_date[i][0]

        print(f"\n-------Expense ID: {i+1}-------")
        print(f"Expense Name: {expense_name}")
        print(f"Expense Amount: {format_expense_amount}")
        print(f"Entry Date: {expense_date}")
        print("--------------------------")

    input("\nPress Enter to return to menu...")

# Start program by launching the CLI main menu
if __name__ == "__main__":
    run_interface()

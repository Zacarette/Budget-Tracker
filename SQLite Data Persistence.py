# TODO:
# .00 money validation
# Search feature by date and name
# Sort by $ high to low and low to high, and date recent to past and past to recent
# Change how many database entries are showed to the user by default when they select the menu option

# OPTIONAL TODO:
# Looping edit for same entry edits
# Validation on edit date for future dates like in first input

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
            print("".center(80, "="))
            print(" Main Menu ".center(80))
            print("".center(80, "="))
            print("Which menu you would like to navigate to?")
            user_selection = int(input("1. Log Expense\n2. Log Income\n3. View Expense\n4. View Income\n5. Edit Expense or Income\n6. View Balance\n0. Exit Program\n\nEnter corresponding number here: "))
            print("")

            # Match input that user selected
            match user_selection:
                case 1:
                    expense_inputs()
                case 2:
                    income_inputs()
                case 3:
                    display_expense_menu()
                case 4:
                    display_income_menu()
                case 5:
                    edit_datebase()
                case 6:
                    display_totals()
                case 0:
                    return
                case _:
                    print("Invalid input. Please enter a number from the menu.\n") # Handles int inputs not 1-6

        # Handles non-int input
        except ValueError:
            print("\nInvalid input. Please enter a number from the menu.\n")

# Get expense inputs
# TODO: add comments for date inputs
def expense_inputs():

    while True:

        # Prompt user for separate expense values
        try:
            print("".center(80, "="))
            print(" Log Expense Menu ".center(80,))
            print("".center(80, "="))
            expense_amounts = int(input("\nHow many separate expense values would you like to track? (Or enter 0 to go back to main menu): "))
            print("".center(80, "─"))

            if (expense_amounts == 0):
                print()
                return
            
            break

        # Handles non-int input
        except ValueError: 
            print("\nInvalid input. Please enter a valid whole number.\n") 

    for i in range(expense_amounts):
            
        while True:

            # Prompt user for expense name and amount, then rounds it to hundreths and gets current date, gives them options to go back and exit
            try:
                expense_type = input(f"Enter the name of expense {i+1} (Or enter '0' to go back): ")

                if (expense_type == "0"):
                    print()
                    expense_inputs()
                    return

                individual_expenses = float(input(f"Enter the expense amount from {expense_type} (Or enter '0' to cancel and exit to main menu): $"))

                if (individual_expenses == 0):
                    return
                
                rounded_expense = round(individual_expenses, 2)

                while True:
                        
                        try:

                            expense_entry_date = input("Enter the date of the expense in this format (YYYY-MM-DD): ")
                
                            check_expense_date = datetime.datetime.strptime(expense_entry_date, "%Y-%m-%d")
                            current_date = datetime.datetime.today()
                            
                            if (current_date >= check_expense_date):
                                
                                format_expense_date = datetime.date.strftime(check_expense_date, "%Y-%m-%d")
                                print()
                                break
                            
                            else:

                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                if (future_date == "y"):

                                    format_expense_date = datetime.date.strftime(check_expense_date, "%Y-%m-%d")
                                    print()
                                    break

                        except ValueError:
                            print("\nInvalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.")

                # Inserts expense info into database and commits
                cursor.execute(
                    "INSERT INTO Expense_Tracker (Expense_Type, Expense_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (expense_type, rounded_expense, format_expense_date)
                )
                connection.commit()
                
                # Output expense input to user via CLI
                print(" Expense Added ".center(80, "-"))
                print("Name:", expense_type)
                print("Amount:", f"${rounded_expense:,.2f}")
                print("Date:", format_expense_date)
                print("".center(80, "-"))
                print("".center(80, "─"))
                break

            # Handles non-int input
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")
    
    # Updates totals in database and pauses for user to view  
    update_in_background()
    input("\nPress Enter to return to menu...")
    print()

# Displays expense entries from database to user
def display_expense_menu():
    
    display_expense()
    input("Press Enter to return to menu...")

def display_expense():
    
    # Get number of expense entries
    expense_id_amount = cursor.execute(
        "SELECT COUNT(Expense_ID) FROM Expense_Tracker"
    ).fetchone()[0] or 0
    
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

    # If no expense entries
    if (expense_id_amount == 0):
        print("".center(80, "="))
        print(" Expense List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Expense Database")
        print("".center(80, "-"))
    
    # Loop and display data from each entry
    else:

        print("".center(80, "="))
        print(" Expense List ".center(80))
        print("".center(80, "="))

        for i in range (expense_id_amount):

            expense_name = column_expense_name[i][0]
            expense_amount = column_expense_amount[i][0]
            format_expense_amount = f"${expense_amount:,.2f}"
            expense_date = column_expense_date[i][0]

            print(f"Expense ID: {i+1}".center(80, "-"))
            print(f"Expense Name: {expense_name}")
            print(f"Expense Amount: {format_expense_amount}")
            print(f"Entry Date: {expense_date}")
            print("".center(80, "-"))
    
    print("".center(80, "─"))
    print()

# Get income inputs
# TODO: add comments for date inputs
def income_inputs():
            
    while True:

        # Prompts user for separate income values
        try:
            print("".center(80, "="))
            print(" Log Income Menu ".center(80,))
            print("".center(80, "=")) 
            income_amounts = int(input("\nHow many separate income values would you like to track? (Or enter 0 to go back to main menu): "))
            print("".center(80, "─"))

            if (income_amounts == 0):
                print()
                return
            
            break

        # Handles non-int input
        except ValueError:
            print("\nInvalid input. Please enter a valid whole number.\n")

    for i in range(income_amounts):

        while True:
            
            # Prompt user for income name and amount, then rounds it to hundreths and gets current date, gives them options to go back and exit
            try:
                income_type = input(f"Enter the name of income {i+1} (Or enter '0' to go back): ")

                if (income_type == "0"):
                    print()
                    expense_inputs()
                    return
                
                individual_incomes = float(input(f"Enter the income you received from {income_type} (Or enter '0' to cancel and exit to main menu): $"))

                if (individual_incomes == 0):
                    return

                rounded_income = round(individual_incomes, 2)
                
                while True:
                        
                        try:

                            income_entry_date = input("Enter the date of the income in this format (YYYY-MM-DD): ")
                
                            check_income_date = datetime.datetime.strptime(income_entry_date, "%Y-%m-%d")
                            current_date = datetime.datetime.today()
                            
                            if (current_date >= check_income_date):
                                
                                format_income_date = datetime.date.strftime(check_income_date, "%Y-%m-%d")
                                print()
                                break
                            
                            else:

                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                if (future_date == "y"):

                                    format_income_date = datetime.date.strftime(check_income_date, "%Y-%m-%d")
                                    print()
                                    break

                        except ValueError:
                            print("\nInvalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.")
                
                # Inserts income info into database and commits
                cursor.execute(
                    "INSERT INTO Income_Tracker (Income_Type, Income_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (income_type, rounded_income, format_income_date)
                )
                connection.commit()

                # Output income input to user via CLI
                print(" Income Added ".center(80, "-"))
                print("Name:", income_type)
                print("Amount:", f"${rounded_income:,.2f}")
                print("Date:", format_income_date)
                print("".center(80, "-"))
                print("".center(80, "─"))
                break
            
            # Handles non-int input
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")

    # Updates totals in database and pauses for user to view          
    update_in_background()
    input("\nPress Enter to return to main menu...")
    print()

def display_income_menu():

    display_income()
    input("\nPress Enter to return to menu...")

# Displays income entries from database to user
def display_income():
    
    # Get number of income entries; defaults to 0 if null
    income_id_amount = cursor.execute(
        "SELECT COUNT(Income_ID) FROM Income_Tracker"
    ).fetchone()[0] or 0
    
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

    # If no income entries
    if (income_id_amount == 0):
        print("".center(80, "="))
        print(" Income List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Income Database")
        print("".center(80, "-"))

    # Loop and display data from each entry
    else:

        print("".center(80, "="))
        print(" Income List ".center(80))
        print("".center(80, "="))
    
        for i in range (income_id_amount):

            income_name = column_income_name[i][0]
            income_amount = column_income_amount[i][0]
            format_income_amount = f"${income_amount:,.2f}"
            income_date = column_income_date[i][0]

            print(f"Income ID: {i+1}".center(80, "-"))
            print(f"Income Name: {income_name}")
            print(f"Income Amount: {format_income_amount}")
            print(f"Entry Date: {income_date}")
            print("".center(80, "-"))
    
    print("".center(80, "─"))
    print()

# Displays current totals and balance to user
def display_totals():
    
    income_sum, expense_sum, remaining_balance = do_total_calculations() # Get updated totals

    # Output total and balance info to user via CLI
    print("".center(80, "="))
    print(" View Balance Menu ".center(80))
    print("".center(80, "="))
    print("".center(80, "-"))
    print("Your total income is:" , f"${income_sum:,.2f}")
    print("Your total expenses are:" , f"${expense_sum:,.2f}")
    print("Your remaining balance after expenses is:" , f"${remaining_balance:,.2f}")
    print("".center(80, "-"))
    input("\nPress Enter to return to menu...")
    print()

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

def edit_datebase():

    while True:

        try:
            print("".center(80, "="))
            print(" Edit Database Menu ".center(80))
            print("".center(80, "="))
            edit = int(input("Which would you like to edit?\n1. Expense\n2. Income\n\nEnter the corrisponding number here(Or enter 0 to go back to main menu): "))
            match edit:
                case 1:
                    edit_expense()
                    break
                case 2:
                    edit_income()
                    break
                case 0:
                    return
                case _:
                    print("\nInvalid input. Please enter a number from the menu.\n") # Handles int inputs not 0, 1, or 2
    
        except ValueError:
            print("\nInvalid input. Please enter a number from the menu.\n")

# TODO: Comments
def edit_expense():

    check_amount = cursor.execute(
        "SELECT COUNT(Expense_ID) FROM Expense_Tracker"
    ).fetchone()[0] or 0

    if (check_amount != 0):
        
        while True:

            try:
                print()
                display_expense()
                id_search = int(input("Enter the corresponding Expense ID that you would like to edit(Or enter 0 to go back): "))

                if (id_search == 0):
                    edit_datebase()
                    break

                database_search = cursor.execute(
                    "SELECT * FROM Expense_Tracker WHERE Expense_ID = (?)",
                    (id_search,)
                ).fetchone()

                if (database_search is not None):

                    expense_id,  expense_name,  expense_amount,  expense_date = database_search

                    while True:
                    
                        try:
                            print()
                            print(f"Expense ID: {expense_id}".center(80, "-"))
                            print(f"Expense Name: {expense_name}")
                            print(f"Expense Amount:", f"${expense_amount:,.2f}")
                            print(f"Entry Date: {expense_date}")
                            print("".center(80, "-"))
                            edit_selection = int(input("Which do you want to edit?\n1. Expense Name\n2. Expense Amount\n3. Entry Date\n\nEnter corresponding numbere here (Or enter 0 to select a different expense): "))

                            if (edit_selection == 0):
                                break

                            match edit_selection:
                                case 1:
                                    edit_name = input("What would you like to change the name to?: ")
                                    cursor.execute(
                                        "UPDATE Expense_Tracker SET Expense_Type = (?) WHERE Expense_ID = (?)",
                                        (edit_name, id_search,)
                                    )
                                    connection.commit()

                                    input("\nName change saved, press enter to return to main menu...")
                                    print()
                                    return

                                case 2:
                                    edit_amount = float(input("What would you like to change the amount to?: $"))
                                    cursor.execute(
                                        "UPDATE Expense_Tracker SET Expense_Amount = (?) WHERE Expense_ID = (?)",
                                        (edit_amount, id_search,)
                                    )
                                    connection.commit()

                                    input("\nAmount change saved, press enter to return to main menu...")
                                    print()
                                    return

                                case 3:
                                    while True:

                                        try:

                                            edit_date = input("What would you like to change the date to? (YYYY-MM-DD): ")
                                            check_edit_date = datetime.datetime.strptime(edit_date, "%Y-%m-%d")
                                            format_expense_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                            cursor.execute(
                                                "UPDATE Expense_Tracker SET Entry_Date = (?) WHERE Expense_ID = (?)",
                                                (format_expense_date, id_search)
                                            )
                                            connection.commit()

                                            input("\nDate change saved, press enter to return to main menu...")
                                            print()
                                            return
                                        
                                        except ValueError:
                                            print("Invalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n")

                                case _:
                                    print("\nInvalid input. Please select a number from the menu.")

                        except ValueError:
                            print("\nInvalid input. Please select a number from the menu.")  
                else:
                    print("\nNo Expense ID with that number. Try again.")

            except ValueError:
                print("\nInvalid input. Enter the ID number for the expense you would like to edit.")
        
    else:
        print()
        print("".center(80, "="))
        print(" Expense List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Expense Database")
        print("".center(80, "-"))
        input("\nPress enter to return to the main menu...")

# TODO: Comments
def edit_income():

    check_amount = cursor.execute(
        "SELECT COUNT(Income_ID) FROM Income_Tracker"
    ).fetchone()[0] or 0

    if (check_amount != 0):
        
        while True:

            try:
                print()
                display_income()
                id_search = int(input("Enter the corresponding Income ID that you would like to edit(Or enter 0 to go back): "))

                if (id_search == 0):
                    edit_datebase()
                    break

                database_search = cursor.execute(
                    "SELECT * FROM Income_Tracker WHERE Income_ID = (?)",
                    (id_search,)
                ).fetchone()

                if (database_search is not None):

                    income_id,  income_name,  income_amount,  income_date = database_search

                    while True:
                    
                        try:
                            print()
                            print(f"Income ID: {income_id}".center(80, "-"))
                            print(f"Income Name: {income_name}")
                            print(f"Income Amount:", f"${income_amount:,.2f}")
                            print(f"Entry Date: {income_date}")
                            print("".center(80, "-"))
                            edit_selection = int(input("Which do you want to edit?\n1. Income Name\n2. Income Amount\n3. Entry Date\n\nEnter corresponding numbere here (Or enter 0 to select a different income): "))

                            if (edit_selection == 0):
                                break

                            match edit_selection:
                                case 1:
                                    edit_name = input("What would you like to change the name to?: ")
                                    cursor.execute(
                                        "UPDATE Income_Tracker SET Income_Type = (?) WHERE Income_ID = (?)",
                                        (edit_name, id_search,)
                                    )
                                    connection.commit()

                                    input("\nName change saved, press enter to return to main menu...")
                                    print()
                                    return

                                case 2:
                                    edit_amount = float(input("What would you like to change the amount to?: $"))
                                    cursor.execute(
                                        "UPDATE Income_Tracker SET Income_Amount = (?) WHERE Income_ID = (?)",
                                        (edit_amount, id_search,)
                                    )
                                    connection.commit()

                                    input("\nAmount change saved, press enter to return to main menu...")
                                    print()
                                    return

                                case 3:
                                    while True:

                                        try:

                                            edit_date = input("What would you like to change the date to? (YYYY-MM-DD): ")
                                            check_edit_date = datetime.datetime.strptime(edit_date, "%Y-%m-%d")
                                            format_income_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                            cursor.execute(
                                                "UPDATE Income_Tracker SET Entry_Date = (?) WHERE Income_ID = (?)",
                                                (format_income_date, id_search)
                                            )
                                            connection.commit()
                                            
                                            input("\nDate change saved, press enter to return to main menu...")
                                            print()
                                            return
                                        
                                        except ValueError:
                                            print("Invalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n")

                                case _:
                                    print("\nInvalid input. Please select a number from the menu.")

                        except ValueError:
                            print("\nInvalid input. Please select a number from the menu.")  
                else:
                    print("\nNo Income ID with that number. Try again.")

            except ValueError:
                print("\nInvalid input. Enter the ID number for the income you would like to edit.")
        
    else:
        print()
        print("".center(80, "="))
        print(" Income List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Income Database")
        print("".center(80, "-"))
        input("\nPress enter to return to the main menu...")

# Start program by launching the CLI main menu
if __name__ == "__main__":
    run_interface()

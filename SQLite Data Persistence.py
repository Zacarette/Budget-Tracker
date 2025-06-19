# TODO:
# Refactor code, when refactoring remember to make seperate functions to help with case flow control structure

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
            user_selection = int(input("1. Log Expense\n2. Log Income\n3. View All Expenses\n4. View All Incomes\n5. Edit Expense or Income\n6. View Balance\n7. Search Databases\n0. Exit Program\n\nEnter corresponding number here: "))
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
                case 7:
                    search_datebase()
                case 0:
                    return
                case _:
                    print("Invalid input. Please enter a number from the menu.\n") # Handles int inputs not 1-6

        # Handles non-int input
        except ValueError:
            print("\nInvalid input. Please enter a number from the menu.\n")

# Get expense inputs
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

            # Prompt user for expense name and gives them options to go back and exit
            try:

                expense_type = input(f"Enter the name of expense {i+1} (Or enter '0' to go back): ")

                if (expense_type == "0"):
                    print()
                    expense_inputs()
                    return

                # Prompts user for expense amount
                while True:

                    try:

                        individual_expenses = input(f"Enter the expense amount from {expense_type} (Or enter '0' to cancel and exit to main menu): $")
                        check_decimal = individual_expenses.split(".")
                
                        if (individual_expenses == "0"):
                            return
                        
                        if ("." in individual_expenses):

                            if (len(check_decimal[1]) > 2):
                                print("\nDecimal Place exceeds the hundredths place. Enter a number no more than two decimal places long.\n")
                            
                            else:
                                checked_expense = float(individual_expenses)
                                break

                        else:
                            checked_expense = float(individual_expenses)
                            break
                    
                    except ValueError:
                        print("\nInvalid input. Enter a valid input consisting only of numbers and '.' (decimal).\n")

                # Validate if users entry date is real and in correct format
                while True:
                        
                        try:

                            expense_entry_date = input("Enter the date of the expense in this format (YYYY-MM-DD): ")
                
                            check_expense_date = datetime.datetime.strptime(expense_entry_date, "%Y-%m-%d")
                            current_date = datetime.datetime.today()
                            
                            if (current_date >= check_expense_date):
                                
                                format_expense_date = datetime.date.strftime(check_expense_date, "%Y-%m-%d")
                                print()
                                break
                            
                            # Date is real but in the future, validate the user is intending to enter a future date
                            else:

                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                if (future_date == "y"):

                                    format_expense_date = datetime.date.strftime(check_expense_date, "%Y-%m-%d")
                                    print()
                                    break

                        except ValueError:
                            print("\nInvalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n")

                # Inserts expense info into database and commits
                cursor.execute(
                    "INSERT INTO Expense_Tracker (Expense_Type, Expense_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (expense_type, checked_expense, format_expense_date)
                )
                connection.commit()
                
                # Output expense input to user via CLI
                print(" Expense Added ".center(80, "-"))
                print("Name:", expense_type)
                print("Amount:", f"${checked_expense:,.2f}")
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

# Displays expense entries from database to user with user continuation validation
def display_expense_menu():
    
    display_expense()
    input("Press Enter to return to menu...")

# Displays expense entries
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
            
            # Prompt user for income name and gives them options to go back
            try:
                income_type = input(f"Enter the name of income {i+1} (Or enter '0' to go back): ")

                if (income_type == "0"):
                    print()
                    expense_inputs()
                    return
                
                # Validates if the users input exceeds the hundredths place
                while True:

                    # Prompts user for income amount
                    try:

                        individual_incomes = input(f"Enter the income amount from {income_type} (Or enter '0' to cancel and exit to main menu): $")
                        check_decimal = individual_incomes.split(".")
                
                        if (individual_incomes == "0"):
                            return
                        
                        if ("." in individual_incomes):

                            if (len(check_decimal[1]) > 2):
                                print("\nDecimal Place exceeds the hundredths place. Enter a number no more than two decimal places long.\n")
                            
                            else:
                                checked_income = float(individual_incomes)
                                break

                        else:
                            checked_income = float(individual_incomes)
                            break
                    
                    except ValueError:
                        print("\nInvalid input. Enter a valid input consisting only of numbers and '.' (decimal).\n")
                
                # Validate if users entry date is real and in correct format
                while True:
                        
                        try:

                            income_entry_date = input("Enter the date of the income in this format (YYYY-MM-DD): ")
                
                            check_income_date = datetime.datetime.strptime(income_entry_date, "%Y-%m-%d")
                            current_date = datetime.datetime.today()
                            
                            if (current_date >= check_income_date):
                                
                                format_income_date = datetime.date.strftime(check_income_date, "%Y-%m-%d")
                                print()
                                break
                            
                            # Date is real but in the future, validate the user is intending to enter a future date
                            else:

                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                if (future_date == "y"):

                                    format_income_date = datetime.date.strftime(check_income_date, "%Y-%m-%d")
                                    print()
                                    break

                        except ValueError:
                            print("\nInvalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n")
                
                # Inserts income info into database and commits
                cursor.execute(
                    "INSERT INTO Income_Tracker (Income_Type, Income_Amount, Entry_Date) VALUES (?, ?, ?)",
                    (income_type, checked_income, format_income_date)
                )
                connection.commit()

                # Output income input to user via CLI
                print(" Income Added ".center(80, "-"))
                print("Name:", income_type)
                print("Amount:", f"${checked_income:,.2f}")
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

# Displays income entries from database to user with user continuation validation
def display_income_menu():

    display_income()
    input("\nPress Enter to return to menu...")

# Displays income entries
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

# Edit menu loop
def edit_datebase():

    while True:

        # Prompt for which database table the user would like to edit
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
            print("\nInvalid input. Please enter a number from the menu.\n") # Handles all other invalid inputs

# Edit expense loop
def edit_expense():

    check_amount = cursor.execute(
        "SELECT COUNT(Expense_ID) FROM Expense_Tracker"
    ).fetchone()[0] or 0

    # If check_amount is not 0, run loop to get user info
    if (check_amount != 0):
        
        while True:

            try:
                print()
                display_expense()
                print("NOTE: If you make multiple edits they will update and save but will not be shown until you exit out the entry you are currently editing.\n")
                id_search = int(input("Enter the corresponding Expense ID that you would like to edit(Or enter 0 to go back): "))

                if (id_search == 0):
                    edit_datebase()
                    break

                database_search = cursor.execute(
                    "SELECT * FROM Expense_Tracker WHERE Expense_ID = (?)",
                    (id_search,)
                ).fetchone()

                # If the Expense ID the user entered is valid gather info from that entry
                if (database_search is not None):

                    expense_id, expense_name, expense_amount, expense_date = database_search

                    while True:
                        
                        # Display info gathered from selected entry
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

                                # Updates and commits expense name change(no validation here, up the the user to create meaningful names on their own)
                                case 1:
                                    edit_name = input("What would you like to change the name to?: ")
                                    cursor.execute(
                                        "UPDATE Expense_Tracker SET Expense_Type = (?) WHERE Expense_ID = (?)",
                                        (edit_name, id_search,)
                                    )
                                    connection.commit()

                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue

                                # Updates and commits expense amount change
                                case 2:

                                    # Check if their updated amount exceeds the hundreths place, if valid commits amount change
                                    while True:

                                        try:

                                            edit_amount = input("What would you like to change the amount to?: $")
                                            check_decimal = edit_amount.split(".")

                                            if ("." in edit_amount):

                                                if (len(check_decimal[1]) > 2):
                                                    print("\nDecimal Place exceeds the hundredths place. Enter a number no more than two decimal places long.\n")

                                                else:

                                                    checked_expense = float(edit_amount)
                                                    break

                                            else:

                                                checked_expense = float(edit_amount)
                                                break
                                        
                                        except ValueError:
                                            print("\nInvalid input. Enter a valid input consisting only of numbers and '.' (decimal).\n")
                                    
                                    cursor.execute(
                                        "UPDATE Expense_Tracker SET Expense_Amount = (?) WHERE Expense_ID = (?)",
                                        (checked_expense, id_search,)
                                    )
                                    connection.commit()
                                                    
                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue

                                # Updates and commits date change
                                case 3:

                                    # Validation for expense date change, if valid commits date change
                                    while True:

                                        try:

                                            edit_date = input("What would you like to change the date to? (YYYY-MM-DD): ")
                                            check_edit_date = datetime.datetime.strptime(edit_date, "%Y-%m-%d")
                                            format_expense_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                            
                                            current_date = datetime.datetime.today()
                            
                                            if (current_date >= check_edit_date):
                                
                                                format_expense_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                                print()
                                                break
                            
                                            # Date is real but in the future, validate the user is intending to enter a future date
                                            else:

                                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                                if (future_date == "y"):

                                                    format_expense_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                                    print()
                                                    break
                                        
                                        except ValueError:
                                            print("Invalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n") # Invalid date format or input
                                    
                                    cursor.execute(
                                        "UPDATE Expense_Tracker SET Entry_Date = (?) WHERE Expense_ID = (?)",
                                        (format_expense_date, id_search)
                                    )
                                    connection.commit()

                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue

                        except ValueError:
                            print("\nInvalid input. Please select a number from the menu.") # Error message for other entries

                else:
                    print("\nNo Expense ID with that number. Try again.") # Error messaage for invalid Expense ID

            except ValueError:
                print("\nInvalid input. Enter the ID number for the expense you would like to edit.") # Error message for values not accepted

    # Database table is empty    
    else:
        print()
        print("".center(80, "="))
        print(" Expense List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Expense Database")
        print("".center(80, "-"))
        input("\nPress enter to return to the main menu...")

# Edit income loop
def edit_income():

    check_amount = cursor.execute(
        "SELECT COUNT(Income_ID) FROM Income_Tracker"
    ).fetchone()[0] or 0

    # If check_amount is not 0, run loop to get user info
    if (check_amount != 0):
        
        while True:

            try:
                print()
                display_income()
                print("NOTE: If you make multiple edits they will update and save but will not be shown until you exit out the entry you are currently editing.\n")
                id_search = int(input("Enter the corresponding Income ID that you would like to edit(Or enter 0 to go back): "))

                if (id_search == 0):
                    edit_datebase()
                    break

                database_search = cursor.execute(
                    "SELECT * FROM Income_Tracker WHERE Income_ID = (?)",
                    (id_search,)
                ).fetchone()

                # If the Income ID the user entered is valid gather info from that entry
                if (database_search is not None):

                    income_id,  income_name,  income_amount,  income_date = database_search

                    while True:
                        
                        # Display info gathered from selected entry
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

                                # Updates and commits income name change(no validation here, up the the user to create meaningful names on their own)
                                case 1:
                                    edit_name = input("What would you like to change the name to?: ")
                                    cursor.execute(
                                        "UPDATE Income_Tracker SET Income_Type = (?) WHERE Income_ID = (?)",
                                        (edit_name, id_search,)
                                    )
                                    connection.commit()

                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue
                                
                                # Updates and commits income amount change
                                case 2:

                                    # Check if their updated amount exceeds the hundreths place, if valid commits amount change
                                    while True:

                                        try:

                                            edit_amount = input("What would you like to change the amount to?: $")
                                            check_decimal = edit_amount.split(".")

                                            if ("." in edit_amount):

                                                if (len(check_decimal[1]) > 2):
                                                    print("\nDecimal Place exceeds the hundredths place. Enter a number no more than two decimal places long.\n")

                                                else:

                                                    checked_income = float(edit_amount)
                                                    break

                                            else:

                                                checked_income = float(edit_amount)
                                                break
                                        
                                        except ValueError:
                                            print("\nInvalid input. Enter a valid input consisting only of numbers and '.' (decimal).\n")
                                    
                                    cursor.execute(
                                        "UPDATE Income_Tracker SET Income_Amount = (?) WHERE Income_ID = (?)",
                                        (checked_income, id_search,)
                                    )
                                    connection.commit()
                                                    
                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue

                                # Updates and commits date change
                                case 3:

                                    # Validation for income date change, if valid commits date change
                                    while True:

                                        try:

                                            edit_date = input("What would you like to change the date to? (YYYY-MM-DD): ")
                                            check_edit_date = datetime.datetime.strptime(edit_date, "%Y-%m-%d")
                                            format_income_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                            
                                            current_date = datetime.datetime.today()
                            
                                            if (current_date >= check_edit_date):
                                
                                                format_income_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                                print()
                                                break
                            
                                            # Date is real but in the future, validate the user is intending to enter a future date
                                            else:

                                                future_date = input("\nDate is in the future, are you sure you want to enter it into the database? (y/n): ")
                                
                                                if (future_date == "y"):

                                                    format_income_date = datetime.date.strftime(check_edit_date, "%Y-%m-%d")
                                                    print()
                                                    break
                                        
                                        except ValueError:
                                            print("Invalid input. Enter a date in YYYY-MM-DD format and make sure it is a real date.\n") # Invalid date format or input
                                    
                                    cursor.execute(
                                        "UPDATE Income_Tracker SET Entry_Date = (?) WHERE Income_ID = (?)",
                                        (format_income_date, id_search)
                                    )
                                    connection.commit()

                                    while True:
                                    
                                        try:

                                            checking = int(input("\nName change saved. Press 1 to edit something else from this entry or 0 to return to the main menu.\n\nEnter here: "))

                                            if (checking == 1):
                                                print()
                                                break

                                            elif (checking == 0):
                                                return
                                            
                                            else:
                                                print("\nInvalid Input.")
                                            
                                        except ValueError:
                                            print("\nInvalid Input.")

                                    continue

                                case _:
                                    print("\nInvalid input. Please select a number from the menu.") # Default case for inputs not on the menu

                        except ValueError:
                            print("\nInvalid input. Please select a number from the menu.") # Error message for other entries

                else:
                    print("\nNo Income ID with that number. Try again.") # Error messaage for invalid Expense ID

            except ValueError:
                print("\nInvalid input. Enter the ID number for the income you would like to edit.") # Error message for values not accepted

    # Database table is empty     
    else:
        print()
        print("".center(80, "="))
        print(" Income List ".center(80))
        print("".center(80, "="))
        print("".center(80, "-"))
        print("No Data Found in Income Database")
        print("".center(80, "-"))
        input("\nPress enter to return to the main menu...")

# Search menu loop
def search_datebase():
    
    while True:

        try:
            print("".center(80, "="))
            print(" Search Database Menu ".center(80))
            print("".center(80, "="))
            search = int(input("Which would you like to search for?\n1. Expense\n2. Income\n\nEnter the corrisponding number here(Or enter 0 to go back to main menu): "))
            match search:
                case 1:
                    search_expense()
                    break
                case 2:
                    search_income()
                    break
                case 0:
                    run_interface()
                case _:
                    print("\nInvalid input. Please enter a number from the menu.\n") # Handles int inputs not 0, 1, or 2
    
        except ValueError:
            print("\nInvalid input. Please enter a number from the menu.\n") # Handles all other invalid inputs

# Search expenses by name, date, and price
def search_expense():

    check_amount = cursor.execute(
        "SELECT COUNT(Expense_ID) FROM Expense_Tracker"
    ).fetchone()[0] or 0

    while True:
    
        try:

            # If check_amount is not 0, prompt user for how they would like to search
            if (check_amount != 0):

                search_type = int(input("\nHow would you like to search for an expense?\n1. By Name\n2. By Date\n3. By Price\n\nEnter the corrisponding number here(Or enter 0 to go back): "))

                if  (search_type == 0):
                    search_datebase()
                
                match search_type:
                    
                    # Searches for what the user entered and returns entries containing those characters
                    case 1:

                        while True:

                            user_search = input("\nEnter the name you would like to search for: ")
                            print()

                            user_search_match = (f"%{user_search}%")

                            name_search = cursor.execute(
                                "SELECT * FROM Expense_Tracker WHERE Expense_Type LIKE (?)",
                                (user_search_match,)
                            ).fetchall()
                        
                            if (len(name_search) != 0):

                                for i in name_search:

                                    id = i[0]
                                    name = i[1]
                                    amount = i[2]
                                    date = i[3]

                                    print(f"Expense ID: {id}".center(80, "-"))
                                    print(f"Expense Name: {name}")
                                    print("Expense Name:", f"${amount:,.2f}")
                                    print(f"Entry Date: {date}")
                                    print("".center(80, "-"))
      
                                input("\nPress Enter to return to main menu...")
                                return

                            else:
                                print("No matches found. Please try again or enter a different name.")

                    # Searches and returns dates descending or ascending depending on what user selects
                    case 2:
                        
                        while True:

                            try:
                        
                                search_order = int(input("\nWould you like to sort dates by descending or ascending?:\n1. Descending(Newest to Oldest)\n2. Ascending(Oldest to Newest)\n\nEnter the corrisponding number here (Or enter 0 to go back): "))

                                match search_order:

                                    case 1:

                                        offset = 0

                                        while True:

                                            desc = cursor.execute(
                                                "SELECT * FROM Expense_Tracker ORDER BY Entry_Date DESC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(desc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Expense ID: {id}".center(80, "-"))
                                                print(f"Expense Name: {name}")
                                                print(f"Expense Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 2:

                                        offset = 0

                                        while True:

                                            asc = cursor.execute(
                                                "SELECT * FROM Expense_Tracker ORDER BY Entry_Date ASC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )

                                            results = list(asc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Expense ID: {id}".center(80, "-"))
                                                print(f"Expense Name: {name}")
                                                print(f"Expense Name:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 0:
                                        break
                                    
                                    case _:
                                        print("Invalid Input. Please enter a valid number from the menu.")

                            except ValueError:
                                print("Invalid Input. Please enter a valid number from the menu.")

                    # Searches and returns prices descending or ascending depending on what user selects
                    case 3:

                        while True:

                            try:
                        
                                search_order = int(input("\nWould you like to sort price by descending or ascending?:\n1. Descending($$$ to $)\n2. Ascending($ to $$$)\n\nEnter the corrisponding number here (Or enter 0 to go back): "))

                                match search_order:

                                    case 1:

                                        offset = 0

                                        while True:

                                            desc = cursor.execute(
                                                "SELECT * FROM Expense_Tracker ORDER BY Expense_Amount DESC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(desc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Expense ID: {id}".center(80, "-"))
                                                print(f"Expense Name: {name}")
                                                print(f"Expense Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 2:

                                        offset = 0

                                        while True:

                                            asc = cursor.execute(
                                                "SELECT * FROM Expense_Tracker ORDER BY Expense_Amount ASC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(asc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Expense ID: {id}".center(80, "-"))
                                                print(f"Expense Name: {name}")
                                                print(f"Expense Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 0:
                                        break
                                    
                                    case _:
                                        print("Invalid Input. Please enter a valid number from the menu.")

                            except ValueError:
                                print("Invalid Input. Please enter a valid number from the menu.")

                    case _:
                        print("Invalid input. Please enter a corrisponding number from the menu.") # Handles int inputs not corrisponding with the main menu

        except ValueError:
            print("Invalid input. Please enter a corrisponding number from the menu.") # Handles all other invalid inputs

# Search incomes by name, date, and price
def search_income():

    check_amount = cursor.execute(
        "SELECT COUNT(Income_ID) FROM Income_Tracker"
    ).fetchone()[0] or 0

    while True:
    
        try:

            # If check_amount is not 0, prompt user for how they would like to search
            if (check_amount != 0):

                search_type = int(input("\nHow would you like to search for an income?\n1. By Name\n2. By Date\n3. By Price\n\nEnter the corrisponding number here(Or enter 0 to go back): "))

                if  (search_type == 0):
                    search_datebase()
                
                match search_type:
                    
                    # Searches for what the user entered and returns entries containing those characters
                    case 1:

                        while True:

                            user_search = input("\nEnter the name you would like to search for: ")
                            print()

                            user_search_match = (f"%{user_search}%")

                            name_search = cursor.execute(
                                "SELECT * FROM Income_Tracker WHERE Income_Type LIKE (?)",
                                (user_search_match,)
                            ).fetchall()
                        
                            if (len(name_search) != 0):

                                for i in name_search:

                                    id = i[0]
                                    name = i[1]
                                    amount = i[2]
                                    date = i[3]

                                    print(f"Income ID: {id}".center(80, "-"))
                                    print(f"Income Name: {name}")
                                    print(f"Income Name:", f"${amount:,.2f}")
                                    print(f"Entry Date: {date}")
                                    print("".center(80, "-"))
      
                                input("\nPress Enter to return to main menu...")
                                return

                            else:
                                print("No matches found. Please try again or enter a different name.")

                    # Searches and returns dates descending or ascending depending on what user selects
                    case 2:
                        
                        while True:

                            try:
                        
                                search_order = int(input("\nWould you like to sort dates by descending or ascending?:\n1. Descending(Newest to Oldest)\n2. Ascending(Oldest to Newest)\n\nEnter the corrisponding number here (Or enter 0 to go back): "))

                                match search_order:

                                    case 1:

                                        offset = 0

                                        while True:

                                            desc = cursor.execute(
                                                "SELECT * FROM Income_Tracker ORDER BY Entry_Date DESC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(desc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Income ID: {id}".center(80, "-"))
                                                print(f"Income Name: {name}")
                                                print(f"Income Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 2:

                                        offset = 0

                                        while True:

                                            asc = cursor.execute(
                                                "SELECT * FROM Income_Tracker ORDER BY Entry_Date ASC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )

                                            results = list(asc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Income ID: {id}".center(80, "-"))
                                                print(f"Income Name: {name}")
                                                print(f"Income Name:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 0:
                                        break
                                    
                                    case _:
                                        print("Invalid Input. Please enter a valid number from the menu.")

                            except ValueError:
                                print("Invalid Input. Please enter a valid number from the menu.")

                    # Searches and returns prices descending or ascending depending on what user selects
                    case 3:

                        while True:

                            try:
                        
                                search_order = int(input("\nWould you like to sort price by descending or ascending?:\n1. Descending($$$ to $)\n2. Ascending($ to $$$)\n\nEnter the corrisponding number here (Or enter 0 to go back): "))

                                match search_order:

                                    case 1:

                                        offset = 0

                                        while True:

                                            desc = cursor.execute(
                                                "SELECT * FROM Income_Tracker ORDER BY Income_Amount DESC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(desc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Income ID: {id}".center(80, "-"))
                                                print(f"Income Name: {name}")
                                                print(f"Income Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 2:

                                        offset = 0

                                        while True:

                                            asc = cursor.execute(
                                                "SELECT * FROM Income_Tracker ORDER BY Income_Amount ASC LIMIT 5 OFFSET (?)",
                                                (offset,)
                                            )
                                        
                                            results = list(asc)

                                            for i in results:
                                            
                                                id = i[0]
                                                name = i[1]
                                                amount = i[2]
                                                date = i[3]

                                                print(f"Income ID: {id}".center(80, "-"))
                                                print(f"Income Name: {name}")
                                                print(f"Income Amount:", f"${amount:,.2f}")
                                                print(f"Entry Date: {date}")
                                                print("".center(80, "-"))
      
                                            if (len(results) < 5):
                                            
                                                input("\nEnd of entries. Press Enter to return to main menu...")
                                                return
                                            
                                            else:

                                                try:

                                                    next_choices = int(input("\nPress 1 to see next entries or 0 to return to main menu.\n\nEnter here: "))

                                                    if (next_choices == 1):
                                                        offset += 5
                                                        continue

                                                    elif (next_choices == 0):
                                                        return

                                                except ValueError:
                                                    print("\nInvalid Input.")
                                    
                                    case 0:
                                        break
                                    
                                    case _:
                                        print("Invalid Input. Please enter a valid number from the menu.")

                            except ValueError:
                                print("Invalid Input. Please enter a valid number from the menu.")

                    case _:
                        print("Invalid input. Please enter a corrisponding number from the menu.") # Handles int inputs not corrisponding with the main menu

        except ValueError:
            print("Invalid input. Please enter a corrisponding number from the menu.") # Handles all other invalid inputs

# Start program by launching the CLI main menu
if __name__ == "__main__":
    run_interface()

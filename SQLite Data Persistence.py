import sqlite3 # Import SQLite3 to interact with databases
import datetime # Import datetime to get current date

connection = sqlite3.connect("Budget_Tracker.db") # Create or connect to database with that file name

cursor = connection.cursor() # Create cursor object to execute SQL commands on the database

# Dev Note: Uncomment the following code to reset databases for testing purposes
# cursor.execute("DROP TABLE IF EXISTS Income_Tracker")
# cursor.execute("DROP TABLE IF EXISTS Expense_Tracker")
# cursor.execute("DROP TABLE IF EXISTS Totals_and_Balance")
# connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS Expense_Tracker (Transaction_Number INTEGER PRIMARY KEY AUTOINCREMENT, Expense_Amount REAL, Entry_Date TEXT)") # Create expense tracker table or connect to it
cursor.execute("CREATE TABLE IF NOT EXISTS Income_Tracker (Transaction_Number INTEGER PRIMARY KEY AUTOINCREMENT, Income_Amount REAL, Entry_Date TEXT)") # Create income tracker table or connect to it
cursor.execute("CREATE TABLE IF NOT EXISTS Totals_and_Balance (Type TEXT PRIMARY KEY, Total_Income REAL, Total_Expense REAL, Total_Remaining REAL, As_of TEXT)") # Create totals and balance table or connect to it

def run_interface(): # Interface function
    
    while True: # Statement to loop interface
            
        try:
            print("\nWhich menu you would like to navigate to?") # Interface navigation prompt
            user_selection = int(input("1. Log expense\n2. Log income\n3. View balance\n4. Exit\n\nEnter corresponding number here: ")) # Get user input

            match user_selection: # Match user input to following cases
                case 1:
                    expense_calculations() # Case 1 runs income_calculations function
                case 2:
                    income_calculations() # Case 2 runs expense_calculations fuction
                case 3:
                    total_calculations() # Case 3 runs total_calculations function
                case 4:
                    return # Case 4 exits program 
                case _:
                    print("\nInvalid input. Please enter a number from the menu.") # Default Case
        
        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number from the menu.") # Error statment

def expense_calculations(): # Expense info function

    while True: # Loop

        try:
            entry_date_expense = datetime.date.today().strftime("%m/%d/%Y") # Get current date
            expense_amounts = int(input("\nHow many seperate expense values would you like to track?: ")) # Get input for how many expenses user would like to track
            print() # \n
            break # Break if valid

        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number.") # Error statment

    for i in range(expense_amounts): # Loop through "i" number of times until it has reached the users input
            
        while True: # Loop

            try:
                individual_expenses = float(input(f"Enter the expense from source {i+1}: $")) # Get input for monthly expense "i"
                rounded_expense = round(individual_expenses, 2) # Round entry to the hundredths
                cursor.execute("INSERT INTO Expense_Tracker (Expense_Amount, Entry_Date) VALUES (?, ?)", (rounded_expense, entry_date_expense)) # Insert information into SQLite Expense_Tracker database
                connection.commit() # Commit entries
                break

            except ValueError: # Error Exception
                print("\nInvalid input. Please enter a number.\n") # Error statments
            
    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

def income_calculations(): # Income info function
            
    while True: # Loop

        try: 
            entry_date_income = datetime.date.today().strftime("%m/%d/%Y") # Get current date
            income_amounts = int(input("\nHow many seperate income values would you like to track?: ")) # Get input for how many sources of income they have to loop through the right amount
            print() # \n
            break # Break if valid

        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number.") # Error statment

    for i in range(income_amounts): # Loop through "i" number of times until it has reached the users input

        while True: # Loop
            
            try:
                individual_incomes = float(input(f"Enter the income you received from source {i+1}: $")) # Get input for their monthly income from "i" source
                rounded_income = round(individual_incomes, 2) # Round entry to the hundredths
                cursor.execute("INSERT INTO Income_Tracker (Income_Amount, Entry_Date) VALUES (?, ?)", (rounded_income, entry_date_income)) # Insert information into Income_Tracker database
                connection.commit() # Commit entries
                break # Break if valid

            except ValueError: # Error Exception
                print("\nInvalid input. Please enter a number.\n") # Error statment
            
    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

def total_calculations(): # Final calculations

    today = datetime.date.today().strftime("%m/%d/%Y") # Get current date

    income_sum = cursor.execute("SELECT SUM(Income_Amount) FROM Income_Tracker").fetchone()[0] or 0 # Get the sum of column Income from database Income_Tracker or set to 0 if null
    expense_sum = cursor.execute("SELECT SUM(Expense_Amount) FROM Expense_Tracker").fetchone()[0] or 0 # Get the sum of column Expense from database Expense_Tracker or set to 0 if null
    remaining_balance = income_sum - expense_sum # Get the difference of income_sum and expense_sum
    cursor.execute("INSERT OR REPLACE INTO Totals_and_Balance (Type, Total_Income, Total_Expense, Total_Remaining, As_of) VALUES ('Totals', ?, ? , ?, ?)", (income_sum, expense_sum, remaining_balance, today)) # Insert information into Expense_Tracker database
    connection.commit() # Commit entries
        
    # Dev Note: Uncomment the following code for testing purposes
    # print("\nYour total income from entered values is:" , f"${income_sum:,.2f}") # Output total incomes to user
    # print(f"Your total expense from entered values is:" , f"${expense_sum:,.2f}") # Output total expenses to user
    # print(f"Your remaining balance after expenses is:" , f"${remaining_balance:,.2f}") # Output remaining balance to user

    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

run_interface() # Run run_interface function to begin loop and start program

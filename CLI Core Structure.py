income_values = [] # Define list that will hold users income values
expense__values = [] # Define list that will hold users expense values

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
            expense_amounts = int(input("\nHow many seperate expense values would you like to track?: ")) # Get input for how many expenses user would like to track
            print() # \n
            break # Break if valid

        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number.") # Error statment

    for i in range(expense_amounts): # Loop through "i" number of times until it has reached the users input
            
        while True: # Loop

            try:
                individual_expenses = float(input(f"Enter the expense from source {i+1}: $")) # Get input for monthly expense "i"
                expense__values.append(individual_expenses) # Add input to list
                break

            except ValueError: # Error Exception
                print("\nInvalid input. Please enter a number.\n") # Error statment
            
    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

def income_calculations(): # Income info function
            
    while True: # Loop

        try: 
            income_amounts = int(input("\nHow many seperate income values would you like to track?: ")) # Get input for how many sources of income they have to loop through the right amount
            print() # \n
            break # Break if valid

        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number.") # Error statment

    for i in range(income_amounts): # Loop through "i" number of times until it has reached the users input

        while True: # Loop
            
            try:
                individual_values = float(input(f"Enter the income you received from source {i+1}: $")) # Get input for their monthly income from "i" source
                income_values.append(individual_values) # Add input to list
                break # Break if valid

            except ValueError: # Error Exception
                print("\nInvalid input. Please enter a number.\n") # Error statment
            
    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

def expense_calculations(): # Expense info function

    while True: # Loop

        try:
            expense_amounts = int(input("\nHow many seperate expense values would you like to track?: ")) # Get input for how many expenses user would like to track
            print() # \n
            break # Break if valid

        except ValueError: # Error Exception
            print("\nInvalid input. Please enter a number.") # Error statment

    for i in range(expense_amounts): # Loop through "i" number of times until it has reached the users input
            
        while True: # Loop

            try:
                individual_expenses = float(input(f"Enter the expense from source {i+1}: $")) # Get input for monthly expense "i"
                expense__values.append(individual_expenses) # Add input to list
                break

            except ValueError: # Error Exception
                print("\nInvalid input. Please enter a number.\n") # Error statment
            
    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

def total_calculations(): # Final calculations

    income_sum = (sum(income_values)) # Calculates sum and assigns it to variable
    expense_sum = (sum(expense__values)) # Calculates sum and assigns it to variable
    remaining_balance = income_sum - expense_sum # Calculates difference and assigns it to variable
        
    print("\nYour total income from entered values is:" , f"${income_sum:,.2f}") # Output total incomes to user
    print(f"Your total expense from entered values is:" , f"${expense_sum:,.2f}") # Output total expenses to user
    print(f"Your remaining balance after expenses is:" , f"${remaining_balance:,.2f}") # Output remaining balance to user

    input("\nPress Enter to return to menu...") # Pauses program until user presses Enter

run_interface() # Run run_interface function to begin loop and start program

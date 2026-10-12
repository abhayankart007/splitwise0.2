# ---------- Data storage ----------
friends = []    # list of friend names, e.g. ["Rahul", "Aman"]
expenses = []   # list of expenses, where each expense is a dictionary


# ---------- Helper functions (input validation) ----------
def get_number(prompt, low, high):
    """Ask the user for a whole number between low and high (inclusive)."""
    while True:
        text = input(prompt)
        try:
            number = int(text)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
        if number < low or number > high:
            print(f"Please enter a number between {low} and {high}.")
        else:
            return number


def get_amount(prompt):
    """Ask the user for a positive amount of money."""
    while True:
        text = input(prompt)
        try:
            amount = float(text)
        except ValueError:
            print("Invalid input. Please enter a number (for example 250 or 99.5).")
            continue
        if amount <= 0:
            print("The amount must be greater than 0.")
        else:
            return amount


def show_friends_list():
    """Print all friends with numbers: 1, 2, 3, ..."""
    number = 1
    for name in friends:
        print(f"  {number}. {name}")
        number = number + 1


# ---------- Feature 1: Add a friend ----------
def add_friend():
    name = input("Enter your friend's name: ").strip().title()
    if name == "":
        print("The name cannot be empty.")
    elif name in friends:
        print(f"{name} is already in your friends list.")
    else:
        friends.append(name)
        print(f"{name} has been added.")


# ---------- Feature 2: Add an expense ----------
def add_expense():
    if len(friends) < 2:
        print("You need at least 2 friends to add an expense.")
        return

    description = input("What is the expense for? (e.g. Dinner): ").strip()
    if description == "":
        description = "Expense"

    amount = get_amount("Enter the total amount (₹): ")

    # Choose who paid
    print("\nWho paid?")
    show_friends_list()
    payer_number = get_number("Enter the payer's number: ", 1, len(friends))
    payer = friends[payer_number - 1]

    # Choose who shares the expense
    print("\nWho should share this expense?")
    show_friends_list()
    participants = []
    while len(participants) == 0:
        text = input("Enter numbers separated by commas (e.g. 1,3) or 'all': ").strip().lower()
        if text == "all":
            participants = friends.copy()
        else:
            valid = True
            for part in text.split(","):
                part = part.strip()
                if not part.isdigit():
                    valid = False
                    break
                number = int(part)
                if number < 1 or number > len(friends):
                    valid = False
                    break
                name = friends[number - 1]
                if name not in participants:   # avoid duplicates
                    participants.append(name)
            if not valid or len(participants) == 0:
                print("Invalid input. Please try again.")
                participants = []

    expense = {
        "description": description,
        "amount": amount,
        "payer": payer,
        "participants": participants,
    }
    expenses.append(expense)

    share = amount / len(participants)
    print(f"\nExpense added. Each participant's share: ₹{share:.2f}")


# ---------- Feature 3: Show all expenses ----------
def show_expenses():
    if len(expenses) == 0:
        print("No expenses have been added yet.")
        return

    number = 1
    for e in expenses:
        share = e["amount"] / len(e["participants"])
        print(f"\n{number}. {e['description']} - ₹{e['amount']:.2f}")
        print(f"   Paid by: {e['payer']}")
        print(f"   Split between: {', '.join(e['participants'])} (₹{share:.2f} each)")
        number = number + 1


# ---------- Balance calculation (the most important part) ----------
def calculate_balances():
    """
    Calculate the net balance of every friend:
      positive (+) = this friend should RECEIVE money
      negative (-) = this friend should PAY money
    """
    balances = {}
    for name in friends:
        balances[name] = 0.0

    for e in expenses:
        share = e["amount"] / len(e["participants"])

        balances[e["payer"]] = balances[e["payer"]] + e["amount"]

        for person in e["participants"]:
            balances[person] = balances[person] - share

    return balances


# ---------- Feature 4: Show each friend's balance ----------
def show_balances():
    if len(friends) == 0:
        print("No friends have been added yet.")
        return

    balances = calculate_balances()
    print("\n--- Balances ---")
    for name in friends:
        amount = round(balances[name], 2)
        if amount > 0.01:
            print(f"{name} should receive ₹{amount:.2f}")
        elif amount < -0.01:
            print(f"{name} owes ₹{-amount:.2f}")
        else:
            print(f"{name} is all settled up")


# ---------- Feature 5: Suggest settlements ----------
def suggest_settlements():
    balances = calculate_balances()
    creditors = []   
    debtors = []     

    for name in friends:
        amount = round(balances[name], 2)
        if amount > 0.01:
            creditors.append([name, amount])
        elif amount < -0.01:
            debtors.append([name, -amount])  

    if len(debtors) == 0:
        print("Everyone is settled up. Nobody owes anything.")
        return

    print("\n--- Settlement Suggestions ---")
    i = 0
    j = 0
    while i < len(debtors) and j < len(creditors):
        pay = min(debtors[i][1], creditors[j][1])
        print(f"{debtors[i][0]} pays ₹{pay:.2f} to {creditors[j][0]}")

        debtors[i][1] = debtors[i][1] - pay
        creditors[j][1] = creditors[j][1] - pay

        if debtors[i][1] < 0.01:
            i = i + 1
        if creditors[j][1] < 0.01:
            j = j + 1


# ---------- Menu and main program ----------
def show_menu():
    print("\n===== SPLITWISE FOR FRIENDLY-USE =====")
    print("\nChoose an option form the menu :")
    print("1. Add friend")
    print("2. Add expense")
    print("3. Show all expenses")
    print("4. Show balances")
    print("5. Suggest settlements")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = get_number("Enter your choice (1-6): ", 1, 6)

        if choice == 1:
            add_friend()
        elif choice == 2:
            add_expense()
        elif choice == 3:
            show_expenses()
        elif choice == 4:
            show_balances()
        elif choice == 5:
            suggest_settlements()
        else:
            print("Thank you for using Splitwise 0.2 ; Goodbye!")
            break


main()
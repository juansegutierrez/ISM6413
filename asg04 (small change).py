#8Asg04
# Juan S. Gutierrez, Mauricio Cervantes, Gabriella E. Battenfield

import json

# Named constants
fixed_fee = 2800          # Monthly Management Fee base amount
budget_rate = 0.18        # Percentage of monthly ad spend added to the management fee
commission_rate = 0.06    # Flat commission rate paid to the sales associate

DEFAULT_FILENAME = "contractList.json"


def get_associate_name():
    """Ask for the sales associate's name (or q/Q to quit) and return it."""
    a = input("Enter the name of the sales associate or q to quit: \n")
    return a


def validate_positive(value):
    """Return True if value is a positive number (greater than zero)."""
    return value > 0


def get_valid_number(prompt):
    """Ask the user for a number using prompt, re-asking until a valid
    positive number is entered. Returns the validated float."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print("That is not a valid number. Please try again.")
            continue

        if validate_positive(value):
            return value
        else:
            print("Please enter a positive number (greater than zero).")


def get_contract_info():
    """Ask for the business name, budget, and setup fee (validated).
    Return all three."""
    n = input("What is the name of the business for this contract? \n")
    b = get_valid_number("What is the monthly advertising budget? \n")
    s = get_valid_number("What is the agreed Digital Advertising Setup Fee? \n")
    return n, b, s


def calculate_contract(b, s):
    """Given budget (b) and setup fee (s), calculate and return f, TAR, c."""
    f = fixed_fee + budget_rate * b
    TAR = s + 12 * f
    c = TAR * commission_rate
    return f, TAR, c


def collect_contracts(contractList):
    """Repeatedly ask for a sales associate name and contract details,
    appending each finished contract to contractList, until the user
    enters q/Q. Returns the updated contractList."""
    a = get_associate_name()
    while a != "q" and a != "Q":
        n, b, s = get_contract_info()
        f, TAR, c = calculate_contract(b, s)
        contractList.append([a, n, b, s, f, TAR, c])
        a = get_associate_name()
    return contractList


def printList(contractList):
    """Print the full contract table, then the 3-line summary totals."""
    if not contractList:
        print("\nThere are no calculations to display")
        print("Load a file or perform new calculations\n")
        return

    print("*" *9)
    print()
    print("The Results of Total Revenue and Commission Calculations")
    print()
    print("*" * 9)
    print("{:<15}{:<25}{:<12}{:<12}{:<12}{:<17}{:<12}".format(
        "Associate", "Business", "Budget", "Setup Fee", "Mgmt Fee",
        "Annual Revenue", "Commission"))

    total_f = 0
    total_TAR = 0
    total_c = 0

    for contract in contractList:
        a, n, b, s, f, TAR, c = contract
        print("{:<15}{:<25}{:<12.2f}{:<12.2f}{:<12.2f}{:<17.2f}{:<12.2f}".format(
            a, n, b, s, f, TAR, c))
        total_f += f
        total_TAR += TAR
        total_c += c

    print("*" * 9)
    print()
    print("The total monthly management fee is \u03a3(f) = ${:.2f}.".format(total_f))
    print("The total annual revenue for all the projects is \u03a3(TAR) = ${:.2f}.".format(total_TAR))
    print("The total commission to all the sales associates is \u03a3(c) = ${:.2f}.".format(total_c))


def store_data(contractList, filename):
    """Write contractList to filename as JSON."""
    with open(filename, "w") as outfile:
        json.dump(contractList, outfile)


def load_data(filename):
    """Read a contractList back from filename (JSON) and return it."""
    with open(filename, "r") as infile:
        contractList = json.load(infile)
    return contractList


def get_filename(prompt_text):
    """Ask for a filename; blank input means use the default file."""
    filename = input(prompt_text)
    if filename.strip() == "":
        filename = DEFAULT_FILENAME
    elif not filename.endswith(".json"):
        filename += ".json"
    return filename


def print_menu():
    print()
    print("Main Menu:")
    print("A)dd calculations to an existing file")
    print("L)oad a file and view results")
    print("P)rint current results")
    print("R)eset and perform new TAR calculations")
    print("S)ave current calculations to a file")


def main():
    contractList = []

    print("Sales and Sales Associate Commission Tracker by Group 8")

    choice = ""
    while choice != "q" and choice != "Q":
        print_menu()
        choice = input("Q)uit: \n")

        if choice == "a" or choice == "A":
            if not contractList:
                print("\nThere are no calculations to display")
                print("Load a file or perform new calculations\n")
            else:
                contractList = collect_contracts(contractList)
                printList(contractList)

        elif choice == "l" or choice == "L":
            filename = get_filename(
                "Enter a file name. Hit enter for the default file (contractList)\n")
            try:
                contractList = load_data(filename)
                printList(contractList)
            except FileNotFoundError:
                print("\nFile '{}' was not found. Please check the name and try again.\n".format(filename))
            except json.JSONDecodeError:
                print("\nFile '{}' could not be read. It may not be a valid saved file.\n".format(filename))

        elif choice == "p" or choice == "P":
            printList(contractList)
            input("\nHit enter to go to the main menu\n")

        elif choice == "r" or choice == "R":
            contractList = []
            contractList = collect_contracts(contractList)
            printList(contractList)

        elif choice == "s" or choice == "S":
            filename = get_filename(
                "Enter file name. Hit enter for the default file (contractList)\n")
            store_data(contractList, filename)

        elif choice == "q" or choice == "Q":
            print("Goodbye!")

        else:
            print("\nInvalid selection. Please choose A, L, P, R, S, or Q.\n")


main()

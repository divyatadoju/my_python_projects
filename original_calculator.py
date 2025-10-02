import calclogo


def add(n1,n2):
    return n1 + n2
def subtract(n1,n2):
    return n1 - n2
def multiply(n1,n2):
    return n1 * n2
def divide(n1,n2):
    return n1 % n2

operations = {
    "+" : add,
    "-" :subtract,
    "*" : multiply,
    "%" : divide
}


def caluculator():
    print (calclogo.logo)

    should_accumulate = True

    num1 = float(input ("what is first num? "))

    while should_accumulate:

            for symbol in operations:
                print(symbol)
            operation_symbol = input("pick an operation: ")
            num2 = float(input("what is second num? "))
            answer = operations[operation_symbol](num1, num2)
            print(f"{num1} {operation_symbol} {num2} = {answer}")
            choice = input(f"type y to continue calculating with {answer} or type n to start new calculation: ")

            if choice == "y":
               num1 = answer

            else:
                should_accumulate = False
                print("\n" * 20)
            caluculator()

caluculator()





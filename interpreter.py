import instruction
import math
# this file is the main file for the interpretation of the MarketLang language

# first of all, we need to define all of the avalible instructions in the language
# we will use the instruction class to do this

# every single inportant logic of the interpreter will be in the runtime class
class Runtime:
    def __init__(self):
        self.instructions = {}
        self.wallet = 10000
        self.user_instructions = {}
        self.variables = {}


runtime = Runtime()
# unpayed instructions
runtime.instructions["price"] = instruction.PriceInstruction("price",runtime)
runtime.instructions["buy"] = instruction.BuyInstruction("buy",runtime)
runtime.instructions["sell"] = instruction.SellInstruction("sell",runtime)
runtime.instructions["count"] = instruction.CountInstruction("count",runtime)
runtime.instructions["wallet"] = instruction.WalletInstruction("wallet",runtime)
runtime.instructions["wait"] = instruction.WaitInstruction("wait",runtime)
runtime.instructions["print"] = instruction.PrintInstruction("print",runtime)

# payed instructions
runtime.instructions["if"] = instruction.PayedInstruction("if",runtime)


# now we need to add 3 free variables to the runtime
runtime.variables["VAR0"] = 0
runtime.variables["VAR1"] = 0
runtime.variables["VAR2"] = 0


for inst in runtime.instructions.keys():
    if runtime.instructions[inst].__class__.__name__ == "UnPayedInstruction":
        runtime.user_instructions[inst] = math.inf
    runtime.user_instructions[inst] = 0

# now we need to define the main function that will interpret the code
def main(path: str):
    # open the file
    currency_symbols = ["€", "$", "£", "¥", "₿"]
    with open(path, "r") as file:
        # read the file
        code = file.read()
        # split the code into lines
        code = code.split("\n")
        # interpret each line
        for line in range(len(code)):
            # split the line into words
            words = code[line].split()
            # check if the first word is an instruction
            if words[0] in runtime.instructions:
                runtime.instructions[words[0]].execute(*words[1:])
            # check if the first word is a variable
            elif words[0] in runtime.variables:
                val = compute_type(words[2])
                if words[1] == "=":
                    runtime.variables[words[0]] = val
                elif words[1] == "+=":
                    runtime.variables[words[0]] += val
                elif words[1] == "-=":
                    runtime.variables[words[0]] -= val
                elif words[1] == "*=":
                    runtime.variables[words[0]] *= val
                elif words[1] == "/=":
                    if val == 0:
                        return Exception(f"Division by zero on line {line+1}: {code[line]}")
                    runtime.variables[words[0]] /= val
                elif words[1] == "++":
                    runtime.variables[words[0]] += 1
                elif words[1] == "--":
                    runtime.variables[words[0]] -= 1
                else:
                    return Exception(f"Invalid variable operation on line {line+1}: {code[line]}")
                
                
            # check if the first word is a comment
            elif words[0][0] in currency_symbols:
                continue
            
            else:
                return Exception(f"Invalid instruction on line {line+1}: {code[line]}")
    return runtime.wallet

def compute_type(value):
    if value[0] == "\"" and value[-1] == "\"":
        return str(value)
    else:
        try:
            return float(value)
        except:
            return Exception(f"Invalid value: {value}")

if __name__ == "__main__":
    print(main("code.Mlang"))



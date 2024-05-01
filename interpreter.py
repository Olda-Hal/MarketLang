import instruction
import math
import logger
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
        self.logger = logger.Logger("console.log")
        self.codeblocks = {}
    
    def stop(self):
        self.logger.log("-----------Program stopped-----------")
        self.logger.log(f"Final wallet: {self.wallet}\nFinal variables: {self.variables}\nFinal user instructions: {self.user_instructions}")
        self.logger.close()


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

currency_symbols = ["€", "$", "£", "¥", "₿"]

# now we need to define the main function that will interpret the code
def main(path: str):
    # open the file    
    with open(path, "r") as file:
        # read the file
        code = file.read()
        # split the code into lines
        code = code.split("\n")

        # record all the codeblocks, if there is an error, end code execution
        if not record_codeblocks(code):
            return

        # interpret each line
        for line in range(len(code)):
            # split the line into words
            words = code[line].split()
            # check if the line is empty
            if len(words) == 0:
                continue
            # check if the first word is an instruction
            if words[0] in runtime.instructions:
                runtime.instructions[words[0]].execute(*words[1:])
            # check if the first word is a variable
            elif words[0] in runtime.variables:
                if not compute_variable_operation(words, line, code):
                    return
                
                
                
                
            # check if the first word is a comment
            elif words[0][0] in currency_symbols:
                continue
            
            else:
                runtime.logger.log( Exception(f"Invalid instruction on line {line+1}: {code[line]}"))
                pass
    return runtime.wallet

# this function finds all the codeblocks in the code that can be jumped to by to goto statements
def record_codeblocks(code):
    for line in range(len(code)):
        words = code[line].split(maxsplit=1)
        if words[0] == "block":
            if words[1] in runtime.codeblocks.keys():
                runtime.logger.log(Exception(f"Codeblock {words[1]} already exists"))
                return
            runtime.codeblocks[words[1]] = line
    return True

def compute_type(value):
    if value[0] == "\"" and value[-1] == "\"":
        return str(value)
    else:
        try:
            return float(value)
        except:
            return Exception(f"Invalid value: {value}")

def compute_variable_operation(words, line, code):
    val = compute_type(words[2])
    try:
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
                runtime.logger.log(Exception(f"Division by zero on line {line+1}: {code[line]}"))
                return
            runtime.variables[words[0]] /= val
        elif words[1] == "++":
            runtime.variables[words[0]] += 1
        elif words[1] == "--":
            runtime.variables[words[0]] -= 1
        elif words[1] == "<-":
            if words[2] in runtime.instructions:
                val = runtime.instructions[words[2]].execute(*words[3:])
                if isinstance(val, Exception):
                    runtime.logger.log(val)
                    return
                runtime.variables[words[0]] = val
        else:
            runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {code[line]}"))
            return
    except:
        runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {code[line]}"))
        return
    return True

if __name__ == "__main__":
    main("code.Mlang")
    runtime.stop()



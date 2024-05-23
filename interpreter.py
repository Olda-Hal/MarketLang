import instruction
import math
import logger
import expression_executor
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
        self.rented_instructions = 0
        self.logger = logger.Logger("console.log", level=0)
        self.codeblocks = {}
        self.current_line = 0
        self.code = []
        self.code_is_running = True
        self.executed_lines = 0
        self.runtime_execution_limit = 100000
        self.memory = {}
    
    def stop(self):
        self.code_is_running = False
        self.logger.log("-----------Program stopped-----------")
        self.logger.log(f"Final wallet: {self.wallet}\nFinal variables: {self.variables}\nFinal user instructions: {self.user_instructions}")


runtime = Runtime()
# unpayed instructions
runtime.instructions["price"] = instruction.PriceInstruction("price",runtime)
runtime.instructions["buy"] = instruction.BuyInstruction("buy",runtime)
runtime.instructions["sell"] = instruction.SellInstruction("sell",runtime)
runtime.instructions["count"] = instruction.CountInstruction("count",runtime)
runtime.instructions["wallet"] = instruction.WalletInstruction("wallet",runtime)
runtime.instructions["wait"] = instruction.WaitInstruction("wait",runtime)
runtime.instructions["print"] = instruction.PrintInstruction("print",runtime)
runtime.instructions["end"] = instruction.EndInstruction("end",runtime)
runtime.instructions["rent"] = instruction.RentInstruction("rent",runtime)
runtime.instructions["release"] = instruction.ReleaseInstruction("release",runtime)

# payed instructions
runtime.instructions["if"] = instruction.IfInstruction("if",runtime)
runtime.instructions["goto"] = instruction.GotoInstruction("goto",runtime)
runtime.instructions["getchar"] = instruction.GetCharInstruction("getchar",runtime)
runtime.instructions["readmem"] = instruction.ReadMemInstruction("readmem",runtime)
runtime.instructions["writemem"] = instruction.WriteMemInstruction("writemem",runtime)


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
def main(code : str):
    runtime.code = code
    # split the code into lines
    runtime.code = runtime.code.split("\n")
    for line in range(len(runtime.code)):
        # split all lines to separate arguments
        runtime.code[line] = runtime.code[line].split()
    
    # add the end instruction to the end of the code
    runtime.code.append(["end"])

    # record all the codeblocks, if there is an error, end code execution
    if not record_codeblocks(runtime.code):
        return
    # read the first line of the code and set the logger level by the number


    # interpret each line
    while(runtime.code_is_running):
        if not interpret_next_line():
            break
        runtime.executed_lines += 1
        if runtime.executed_lines > runtime.runtime_execution_limit:
            runtime.logger.log(Exception("Code execution limit reached"))
            break

def interpret_next_line():
    line = runtime.code[runtime.current_line]
    # if the line is empty, skip it
    if len(line) == 0:
        runtime.current_line += 1
        return True
    # if the line is a comment, skip it
    if line[0][0] in currency_symbols:
        runtime.current_line += 1
        return True
    
    # if the line is a code block (not an instruction), skip it
    if line[0] == "block":
        runtime.current_line += 1
        return True
    if line[0] == "end":
        runtime.stop()
        return
    
    if line[0] == "#loglevel":
        runtime.logger.loglevel = int(line[1])
        runtime.current_line += 1
        return True
    
    if line[0] == "#looplimit":
        runtime.runtime_execution_limit = int(line[1])
        runtime.current_line += 1
        return True
    
    if line[0] == "else":
            runtime.current_line += 2
            return True
    # if the line contains a valid instruction, execute it
    if line[0] in runtime.instructions:
        # check if the user owns the instruction and if they have enough of it buy it for them
        # chcecks only if the instruction is payed
        if isinstance(runtime.instructions[line[0]], instruction.PayedInstruction):
            if runtime.user_instructions[line[0]] > 0:
                runtime.user_instructions[line[0]] -= 1
            else:
                if not runtime.instructions["buy"].execute(line[0], 1):
                    runtime.stop()
                    return
                
                if runtime.logger.loglevel >= 1:
                    runtime.logger.log(Warning(f"User does not own instruction {line[0]}. automatically bought it for them."))
        if line[0] == "if":
            execute = runtime.instructions[line[0]].execute(*line[1:])
            if not execute:
                runtime.current_line += 1
                if runtime.code[runtime.current_line+1][0] == "else":
                    runtime.current_line += 1
        
                
        else:
            runtime.instructions[line[0]].execute(*line[1:])
    # if the line contains a variable operation, execute it
    elif line[0] in runtime.variables:
        if not compute_variable_operation(line, runtime.current_line, runtime.code):
            return
    else:
        # if the instruction is invalid, log the error and stop the code
        result = ' '.join(runtime.code[runtime.current_line])
        runtime.logger.log( Exception(f"Invalid instruction on line {runtime.current_line+1}: {result}"))
        
        return
    runtime.current_line += 1
    return True


# this function finds all the codeblocks in the code that can be jumped to by to goto statements
def record_codeblocks(code):
    for line in range(len(code)):
        if len(runtime.code[line]) == 0:
            continue	
        if runtime.code[line][0] == "block":
            if runtime.code[line][1] in runtime.codeblocks.keys():
                runtime.logger.log(Exception(f"Codeblock {runtime.code[line][1]} already exists"))
                return
            runtime.codeblocks[runtime.code[line][1]] = line
    return True

def compute_type(value):
    value = ' '.join(value)
    if value[0] == "\"" and value[-1] == "\"":
        return str(value)
    else:
        try:
            val = expression_executor.eval_expr(value, runtime.variables)
            return val

        except:
            runtime.logger.log(Exception(f"Invalid value: {value}"))

def compute_variable_operation(words, line, code):
    try:
        if words[1] == "=":
            val = compute_type(words[2:])
            runtime.variables[words[0]] = val
        elif words[1] == "+=":
            val = compute_type(words[2:])
            runtime.variables[words[0]] += val
        elif words[1] == "-=":
            val = compute_type(words[2:])
            runtime.variables[words[0]] -= val
        elif words[1] == "*=":
            val = compute_type(words[2:])
            runtime.variables[words[0]] *= val
        elif words[1] == "/=":
            val = compute_type(words[2:])
            if val == 0:
                result = ' '.join(runtime.code[runtime.current_line])
                runtime.logger.log(Exception(f"Division by zero on line {line+1}: {result}"))
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
                result = ' '.join(runtime.code[runtime.current_line])
                runtime.logger.log(Exception(f"Invalid operation on line {line+1}: {result}"))
                return
        else:
            result = ' '.join(runtime.code[runtime.current_line])
            runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {result}"))
            return
    except:
        result = ' '.join(runtime.code[runtime.current_line])
        runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {result}"))
        return
    return True

# main function that interprets the code
def start(code: str) -> str:
    main(code)
    if runtime.code_is_running:
        runtime.stop()
    return runtime.logger.result

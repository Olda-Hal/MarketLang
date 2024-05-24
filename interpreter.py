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

class Interpreter:
    def __init__(self):
        self.runtime = Runtime()
        # unpayed instructions
        self.runtime.instructions["price"] = instruction.PriceInstruction("price",self.runtime)
        self.runtime.instructions["buy"] = instruction.BuyInstruction("buy",self.runtime)
        self.runtime.instructions["sell"] = instruction.SellInstruction("sell",self.runtime)
        self.runtime.instructions["count"] = instruction.CountInstruction("count",self.runtime)
        self.runtime.instructions["wallet"] = instruction.WalletInstruction("wallet",self.runtime)
        self.runtime.instructions["wait"] = instruction.WaitInstruction("wait",self.runtime)
        self.runtime.instructions["print"] = instruction.PrintInstruction("print",self.runtime)
        self.runtime.instructions["end"] = instruction.EndInstruction("end",self.runtime)
        self.runtime.instructions["rent"] = instruction.RentInstruction("rent",self.runtime)
        self.runtime.instructions["release"] = instruction.ReleaseInstruction("release",self.runtime)

        # payed instructions
        self.runtime.instructions["if"] = instruction.IfInstruction("if",self.runtime)
        self.runtime.instructions["goto"] = instruction.GotoInstruction("goto",self.runtime)
        self.runtime.instructions["getchar"] = instruction.GetCharInstruction("getchar",self.runtime)
        self.runtime.instructions["readmem"] = instruction.ReadMemInstruction("readmem",self.runtime)
        self.runtime.instructions["writemem"] = instruction.WriteMemInstruction("writemem",self.runtime)


        # now we need to add 3 free variables to the runtime
        self.runtime.variables["VAR0"] = 0
        self.runtime.variables["VAR1"] = 0
        self.runtime.variables["VAR2"] = 0


        for inst in self.runtime.instructions.keys():
            if self.runtime.instructions[inst].__class__.__name__ == "UnPayedInstruction":
                self.runtime.user_instructions[inst] = math.inf
            self.runtime.user_instructions[inst] = 0

        self.currency_symbols = ["€", "$", "£", "¥", "₿"]

    # now we need to define the main function that will interpret the code
    def main(self, code : str):
        self.runtime.code = code
        # split the code into lines
        self.runtime.code = self.runtime.code.split("\n")
        for line in range(len(self.runtime.code)):
            # split all lines to separate arguments
            self.runtime.code[line] = self.runtime.code[line].split()
        
        # add the end instruction to the end of the code
        self.runtime.code.append(["end"])

        # record all the codeblocks, if there is an error, end code execution
        if not self.record_codeblocks(self.runtime.code):
            return
        # read the first line of the code and set the logger level by the number


        # interpret each line
        while(self.runtime.code_is_running):
            if not self.interpret_next_line():
                break
            self.runtime.executed_lines += 1
            if self.runtime.executed_lines > self.runtime.runtime_execution_limit:
                self.runtime.logger.log(Exception("Code execution limit reached"))
                break

    def interpret_next_line(self):
        line = self.runtime.code[self.runtime.current_line]
        # if the line is empty, skip it
        if len(line) == 0:
            self.runtime.current_line += 1
            return True
        # if the line is a comment, skip it
        if line[0][0] in self.currency_symbols:
            self.runtime.current_line += 1
            return True
        
        # if the line is a code block (not an instruction), skip it
        if line[0] == "block":
            self.runtime.current_line += 1
            return True
        if line[0] == "end":
            self.runtime.stop()
            return
        
        if line[0] == "#loglevel":
            self.runtime.logger.loglevel = int(line[1])
            self.runtime.current_line += 1
            return True
        
        if line[0] == "#looplimit":
            self.runtime.runtime_execution_limit = int(line[1])
            self.runtime.current_line += 1
            return True
        
        if line[0] == "else":
                self.runtime.current_line += 2
                return True
        # if the line contains a valid instruction, execute it
        if line[0] in self.runtime.instructions:
            # check if the user owns the instruction and if they have enough of it buy it for them
            # chcecks only if the instruction is payed
            if isinstance(self.runtime.instructions[line[0]], instruction.PayedInstruction):
                if self.runtime.user_instructions[line[0]] > 0:
                    self.runtime.user_instructions[line[0]] -= 1
                else:
                    if not self.runtime.instructions["buy"].execute(line[0], 1):
                        self.runtime.stop()
                        return
                    
                    if self.runtime.logger.loglevel >= 1:
                        self.runtime.logger.log(Warning(f"User does not own instruction {line[0]}. automatically bought it for them."))
            if line[0] == "if":
                execute = self.runtime.instructions[line[0]].execute(*line[1:])
                if not execute:
                    self.runtime.current_line += 1
                    if self.runtime.code[self.runtime.current_line+1][0] == "else":
                        self.runtime.current_line += 1
            
                    
            else:
                self.runtime.instructions[line[0]].execute(*line[1:])
        # if the line contains a variable operation, execute it
        elif line[0] in self.runtime.variables:
            if not self.compute_variable_operation(line, self.runtime.current_line, self.runtime.code):
                return
        else:
            # if the instruction is invalid, log the error and stop the code
            result = ' '.join(self.runtime.code[self.runtime.current_line])
            self.runtime.logger.log( Exception(f"Invalid instruction on line {self.runtime.current_line+1}: {result}"))
            
            return
        self.runtime.current_line += 1
        return True


    # this function finds all the codeblocks in the code that can be jumped to by to goto statements
    def record_codeblocks(self, code):
        for line in range(len(code)):
            if len(self.runtime.code[line]) == 0:
                continue	
            if self.runtime.code[line][0] == "block":
                if self.runtime.code[line][1] in self.runtime.codeblocks.keys():
                    self.runtime.logger.log(Exception(f"Codeblock {self.runtime.code[line][1]} already exists"))
                    return
                self.runtime.codeblocks[self.runtime.code[line][1]] = line
        return True

    def compute_type(self, value):
        value = ' '.join(value)
        if value[0] == "\"" and value[-1] == "\"":
            return str(value)
        else:
            try:
                val = expression_executor.eval_expr(value, self.runtime.variables)
                return val

            except:
                self.runtime.logger.log(Exception(f"Invalid value: {value}"))

    def compute_variable_operation(self,words, line, code):
        try:
            if words[1] == "=":
                val = self.compute_type(words[2:])
                self.runtime.variables[words[0]] = val
            elif words[1] == "+=":
                val = self.compute_type(words[2:])
                self.runtime.variables[words[0]] += val
            elif words[1] == "-=":
                val = self.compute_type(words[2:])
                self.runtime.variables[words[0]] -= val
            elif words[1] == "*=":
                val = self.compute_type(words[2:])
                self.runtime.variables[words[0]] *= val
            elif words[1] == "/=":
                val = self.compute_type(words[2:])
                if val == 0:
                    result = ' '.join(self.runtime.code[self.runtime.current_line])
                    self.runtime.logger.log(Exception(f"Division by zero on line {line+1}: {result}"))
                    return
                self.runtime.variables[words[0]] /= val
            elif words[1] == "++":
                self.runtime.variables[words[0]] += 1
            elif words[1] == "--":
                self.runtime.variables[words[0]] -= 1
            elif words[1] == "<-":
                if words[2] in self.runtime.instructions:
                    val = self.runtime.instructions[words[2]].execute(*words[3:])
                    if isinstance(val, Exception):
                        self.runtime.logger.log(val)
                        return
                    self.runtime.variables[words[0]] = val
                else:
                    result = ' '.join(self.runtime.code[self.runtime.current_line])
                    self.runtime.logger.log(Exception(f"Invalid operation on line {line+1}: {result}"))
                    return
            else:
                result = ' '.join(self.runtime.code[self.runtime.current_line])
                self.runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {result}"))
                return
        except:
            result = ' '.join(self.runtime.code[self.runtime.current_line])
            self.runtime.logger.log(Exception(f"Invalid variable operation on line {line+1}: {result}"))
            return
        return True

    # main function that interprets the code
    def start(self, code: str) -> str:
        self.main(code)
        if self.runtime.code_is_running:
            self.runtime.stop()
        return self.runtime.logger.result

import GBM_generator
import random
from typing import *
# this file contains the class definition for the instruction class
# this class is used to hold the information about the price of the instruction

class Instruction:
    def __init__(self, name: str, runtime: object) -> None:
        self.name = name
        self.runtime = runtime
    
    def get_price(self) -> float:
        return 0
    
    def buy(self, count: int):
        price = self.get_price(self.mu)*count
        return price

    def sell(self, count: int):
        price = self.get_price(self.mu)*count
        return price

class PayedInstruction(Instruction):
    def __init__(self, name: str, runtime: object, start_price: int=100) -> None:
        self.generator = GBM_generator.GBM_generator()
        self.generator.simulate_gbm(x0=start_price)
        self.mu = 0
        self.last_price = start_price
        super().__init__(name, runtime)
    
    def get_price(self) -> float:
        self.last_price = self.generator.generator.send(self.mu)
        return self.last_price
    
    
    def wait(self):
        if self.mu > 0:
            self.mu -= random.uniform(0, 5)
        elif self.mu < 0:
            self.mu += random.uniform(0, 5)
        self.get_price()
        return self.last_price
    
class UnpayedInstruction(Instruction):
    def __init__(self, name: str, runtime: object) -> None:
        super().__init__(name, runtime)
    
    def get_price(self) -> float:
        return 0

class PriceInstruction(UnpayedInstruction):

    def __init__(self, name: str, runtime: object) -> None:
        super().__init__(name, runtime)

    def execute(self, inst: str) -> Union[Exception, bool]:
        try:
            if inst not in self.runtime.instructions:
                return Exception("Instruction not found")
            else:
                return self.runtime.instructions[inst].get_price()
        except Exception as e:
            return e

class BuyInstruction(UnpayedInstruction):

    def __init__(self, name: str, runtime: object) -> None:
        super().__init__(name, runtime)

    def execute(self, inst: str, count: int) -> Union[Exception, bool]:
        try:
            if inst not in self.runtime.instructions:
                return Exception("Instruction not found")
            else:
                if count < 0:
                    return Exception("Invalid count")
                if self.runtime.user_instructions[inst].__class__.__name__ == "UnpayedInstruction":
                    return Exception("Instruction is not buyable")
                price = self.runtime.instructions[inst].buy(count)
                if price > self.runtime.wallet:
                    return Exception("Not enough money")
                else:
                    self.runtime.wallet -= price
                    self.runtime.user_instructions[inst] += count
                    return True
        except Exception as e:
            return e

class SellInstruction(UnpayedInstruction):
    
        def __init__(self, name: str, runtime: object) -> None:
            super().__init__(name, runtime)
    
        def execute(self, inst: str, count: int) -> Union[Exception, bool]:
            try:
                if inst not in self.runtime.instructions:
                    return Exception("Instruction not found")
                else:
                    if count < 0:
                        return Exception("Invalid count")
                    if self.runtime.user_instructions[inst].__class__.__name__ == "UnpayedInstruction":
                        return Exception("Instruction is not sellable")
                    price = self.runtime.instructions[inst].sell(count)
                    if self.runtime.user_instructions[inst] < count:
                        return Exception("Not enough instructions")
                    else:
                        self.runtime.wallet += price
                        self.runtime.user_instructions[inst] -= count
                        return True
            except Exception as e:
                return e

class CountInstruction(UnpayedInstruction):
    
    def __init__(self, name: str, runtime: object) -> None:
        super().__init__(name, runtime)
    
    def execute(self, inst: str) -> Union[Exception, int]:
        try:
            if inst not in self.runtime.instructions:
                return Exception("Instruction not found")
            else:
                if self.runtime.user_instructions[inst].__class__.__name__ == "UnpayedInstruction":
                    return Exception("You have infinite number of these instructions")
                return self.runtime.user_instructions[inst]
        except Exception as e:
            return e

class WalletInstruction(UnpayedInstruction):
    
    def __init__(self, name: str, runtime: object) -> None:
        super().__init__(name, runtime)
    
    def execute(self) -> float:
        return self.runtime.wallet

class WaitInstruction(UnpayedInstruction):
        
        def __init__(self, name: str, runtime: object) -> None:
            super().__init__(name, runtime)
        
        def execute(self) -> Union[Exception, bool]:
            for inst in self.runtime.instructions.keys():
                if self.runtime.instructions[inst].__class__.__name__ == "PayedInstruction":
                    self.runtime.instructions[inst].wait()

class PrintInstruction(UnpayedInstruction):
        
        def __init__(self, name: str, runtime: object) -> None:
            super().__init__(name, runtime)
        
        def execute(self, variable_name: str) -> Union[Exception, bool]:
            try:
                if variable_name not in self.runtime.variables:
                    return Exception("Variable not found")
                else:
                    print(self.runtime.variables[variable_name])
                    return True
            except Exception as e:
                return e
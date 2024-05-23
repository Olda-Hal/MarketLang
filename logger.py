# this file is used to write all logs from the program to a file
from typing import *


class Logger:
    def __init__(self, path: str = "console.log", level: int =1) -> None:
        self.path = path
        self.result = ""
        self.loglevel = level
    
    
    def log(self, text: Union[Exception, str]) -> None:
        if isinstance(text, Warning):
            self.result += f"Warning: {text}\n"
        elif isinstance(text, Exception):
            self.result += f"Error: {text}\n"
        else:
            self.result += f"{text}\n"
    
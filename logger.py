# this file is used to write all logs from the program to a file
from typing import *


class Logger:
    def __init__(self, path: str = "console.log") -> None:
        self.path = path
        self.file = open(path, "w")
    
    
    def log(self, text: Union[Exception, str]) -> None:
        if isinstance(text, Exception):
            self.file.write(f"\nError: {text}\n\n")
        else:
            self.file.write(f"{text}\n")
    
    def close(self) -> None:
        self.file.close()
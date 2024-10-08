# Documentation
this is the documentation for everything about the Mlang language.

# Instructions (operations)
there are three types of instructions: free, variable and payed. free instructions are free to use and do not require any payment. variable instructions are used to work with variables and require you to rent a variable before you can use it. payed instructions are payed and require you to buy them before you can use them. you may use the `price` operation to get the price of an operation and the `buy` operation to buy it.

# Syntax
mlang has a symple syntax. every line of code is a single instruction. every instruction is separated by a new line. every keyword and values is separated by a space. every operation has a specific syntax that you have to follow. every operation has a specific number of arguments that you have to provide. All the operations are case insensitive. 

## Free operations
these operations are free to use and do not require any payment

###  price
this operation is used to get the price of a payed operation
```mlang
price <operation>
```
this operation will return the price of the operation in MLang coins. if the operation is free, it will return 0
this operation may be used in the following way:
```mlang
VAR0 = price if
```

### buy
this operation is used to buy a payed operation
```mlang
buy <operation>
```
this operation will buy the operation and add it to the user's account. if you do not have enough MLang coins, this operation will throw an exception
this operation may be used in the following way:
```mlang
buy if
```

### sell
this operation is used to sell a payed operation
```mlang
sell <operation>
```
this operation will sell the operation and remove it from the user's account. if you do not have the operation, this operation will throw an exception
this operation may be used in the following way:
```mlang
sell if
```

### count
this operation is used to return the number of operations in the user's account
```mlang
count <operation>
```
this operation will return the number of operations in the user's account. if the operation is not in the user's account, it will return 0
if you try to count a free operation, it will return infinity
if you try to count unexisting operation, it will return an exception
this operation may be used in the following way:
```mlang
VAR0 = count if
```

### wallet
this operation is used to return the number of MLang coins in the user's account
```mlang
wallet
```
this operation may be used in the following way:
```mlang
VAR0 = wallet
```

### wait
this operation is used to wait for a certain amount of time in the stock market
```mlang
wait <time>
```
this operation may be used to wait until the stock market reaches a certain price for a specific operation
```mlang
wait 100
```
this code waits for 100 "ticks" in the stock market. this means that if the stock market is in decline, the price will probably go down. you may use this instruction in a loop to wait for the price to go up or down

### print
this operation is used to print a message to the console
```mlang
print <message>
```
this operation is used only for debugging purposes therefore it is free to use. this operation may be used in the following way:
if the message doesnt look like a variable, it will be printed as is, otherwise it will be replaced with the variable's value. Because of this you dont need to write any quotes around the message
```mlang
print hello world
print VAR0
```
### end
this operation is used to end the program
```mlang
end
```
if you want to end the program in the middle of the code, you may use this operation. The interpreter will automatically insert the end instruction at the end of the file. this operation may be used in the following way:
```mlang
VAR0 <- wallet
if VAR0 <= 10
end
```

## Variable operations
these operations are free to use and do not require any payment. they are used to work with variables. variables are used to store values and can be used in operations
by default you have 3 free variables: VAR0, VAR1, VAR2. you may use these variables to store values. you may also buy more variables if you need them.

### rent
this operation is used to rent a variable
```mlang
rent <variable name>
```
this operation will rent a variable and add it to the user's account. if you do not have enough MLang coins, this operation will throw an exception.
renting a variable means that you will be able to use it in your code, but for every `wait` operation you will have to pay a fee. this fee is calculated as the number of variables you have rented multiplied by the time you are waiting. if you do not have enough MLang coins to pay the fee, the variable will be blocked until you pay the fee. The fee is always 1 coin per tick per variable.
this operation may be used in the following way:
```mlang
rent MYNEWVAR
```

### release
this operation is used to release a variable from the user's account and stop paying the fee for it
```mlang
release <variable name>
```
this operation will release a variable from the user's account. if you do not have the variable, this operation will throw an exception. if you have rented the variable, you will stop paying the fee for it. but bevare that everything stored in the variable will be lost forever.
this operation may be used in the following way:
```mlang
release MYNEWVAR
```

### operations
every variable has some basic operations that can be performed on it. these operations are:
- `=`: assign a value to the variable
- `+=`: add a value to the variable
- `-=`: subtract a value from the variable
- `*=`: multiply the variable by a value
- `/=`: divide the variable by a value
- `++`: increment the variable by 1
- `--`: decrement the variable by 1
- `<-`: assign a return value from a operation to the variable 

if you try to do an operation on a variable that you have not rented, it will throw an exception.
if you try to devide by 0, it will throw an exception.
if you try to do any operation on a type that doesnt support it, it will throw an exception.

these operations may be used in the following way:
```mlang
VAR0 = 10
VAR0 = VAR1 * 5
VAR0 += 5
VAR0 -= 3
VAR0 *= 2
VAR0 /= 4
VAR0 ++
VAR0 --
VAR0 <- price if
```

## Payed operations
these operations are payed and require you to buy them before you can use them. you may use the `price` operation to get the price of an operation and the `buy` operation to buy it.
if you dont own the operation, it will be bought automatically when you try to use it, bevare that this action will be logged in the log file. if you dont have enough MLang coins, it will throw an exception.

### goto
this operation is used to jump to a specific block of the code.
```mlang
goto <block>
```
blocks are defined by the following syntax:
```mlang
block <block name>
```
this is used insted of defining line number for the goto oper. this way you can easily change the order of the blocks without changing the goto operations.
this operation may be used in the following way:
```mlang
block start
print hello world
goto start
```
this will create an infinite loop that prints "hello world" to the console (this wont really be forever because it will stop as soon as you bankrupt)

### if
this operation is used to execute the following line of code only if a condition is met you may pair it with the `goto` operation to create a loop or a bigger code block
```mlang
if <condition>
```
this operation may be used in the following way:
```mlang
VAR0 = 10
if VAR0 > 5
goto myIfBlock
```

### else
this operation is used to execute the following line of code only if the condition in the `if` operation is not met. It may be chained with the `if` operation to create more complex conditions. cost of this is included in the previous `if` operation
```mlang
if VAR0 > 5
print "VAR0 is greater than 5"
else
print "VAR0 is less than or equal to 5"
```

### getchar
this operation is used to get a single character from a string
```mlang
VAR0 = "hello"
VAR1 <- getchar VAR0 2
print VAR1
```

### readmem
this operation is used to read a memory list
```mlang
VAR0 = readmem <POS>
```
this operation may be used in the following way:
```mlang
VAR1 = 10
VAR0 = readmem 0
print VAR0
VAR0 = readmem VAR1
print VAR0
```

### writemem
this operation is used to write a value to a memory list
```mlang
writemem <POS> <VALUE>
```
this operation may be used in the following way:
```mlang
VAR0 = 10
writemem 0 VAR0
writemem VAR0 20
```

# Memory list
Memory List is an alternative way to store int values. it is a infinite list of values that can be accessed by their position. you may use the `readmem` operation to read a value from the memory list and the `writemem` operation to write a value to the memory list. the memory list is initialized with 0s. if you try to read from a position that is not initialized, it will return 0. You may access memory values with negative positions (it has infinite members in both directions). The main disadvantage of the memory list is that you have to pay for every read and write operation.


# Types
Mlang has two types of values: numbers and strings. numbers are used to store numerical values and strings are used to store text values. the numerical values are stored as 64 bit floating point numbers and the text values are stored as UTF-8 encoded strings.

# Comments
comments are used to write notes in the code that are not executed. because we want to increase the amount of money flowing through our code, you can create a comment by any common money symbol (€, $, £, ¥, ₿)

# Logger
the logger is used to log all the actions that are performed in the code. this is used to track the flow of the code. the log is a file that is created in the same directory as the code and is named `console.log`. the logger logs every exception, suspicious action (Warning) and every print statement. 
Logger has few levels of logging. you may set the level by setting the enviroment variable `loglevel` by the following way:
```mlang
#loglevel 0
$ this sets the log level to 0
```
the levels are:
- 0: no logging (only errors)
- 1: level 0 + warnings
- 2: level 1 + every event in the code (every line execution)

default log level is 0. you may change the log level at any time in the code.

# Infinite loops
if you create an infinite loop in the code, the code will stop executing and throw an exception. this is done to prevent the code from running forever and to prevent the user from going bankrupt. The hard limit is 100 000 lines executed. if you reach this limit, the code will stop executing and throw an exception.
you may change the limit by setting the enviroment variable `looplimit` by the following way:
```mlang
#looplimit 100000
$ this sets the loop limit to 100000
```
the biggest limit is 1 000 000. default limit is 100 000. you may change the limit at any time in the code.
# -------------------------------
# Basic Data Types in Python
# -------------------------------

# STRING
# this will print text to the terminal
print("\n---string---")  # \n is a special sign that creates a new line in the terminal
# store the word "hello" as a STRING type ty 'my_variable'
my_variable = "hello"
# take 'my_variable' and attach the word " world"
my_variable = my_variable + " world"
# you can also write the addition like this
# I will you this syntax from now on because it is simply shorter
my_variable += "!"  # literraly the same as: 'my_variable = my_variable + "!"'
# now 'my_varible' stores "hello world!"
# try it by printing it out
print(my_variable)

# INTEGER
print("\n---integer---")
# you can also store different datatypes like INTEGER
# INTEGER ('int' in Python) stores number without decimals
my_number = 10
# add 10 + 11 ad store it to 'my_number' again
my_number += 11
# try it by printing it out
print(my_number)  # prints: 21

# FLOAT
print("\n---float---")
# you can also reuse the varibale name (but I do not really recommend it)
# here we will store to our original 'my_variable' a FLOAT data type
# FLOAT stores number with decimals
my_variable = 10.1
# we can also use some othe math operations like division
my_variable /= 10
# try it by printing it out
print(my_variable)  # prints: 1.01
# or multiplication
my_variable *= 100
# try it by printing it out
print(my_variable)  # prints: 101.0
# we can also use different variables together and make complex mathematical expressions
my_number = ((my_variable + 10) * 2.3) / 3
# try it by printing it out
print(my_number)  # prints: 85.1

# BOOLEAN
print("\n---boolean---")
# the last important data type for today is BOOLEAN
# BOOLEAN ('bool' in Python) stores only True or False
my_boolean = False
print(my_boolean)  # prints: False

# USER INPUT
print("\n---user input---")
# you can also tell python that the user should input something
# here we will show "Please write something: " in the terminal
# and the user needs to type something and hit enter
# the result we will store in a variable 'my_input'
my_input = input("Please write something: ")
# try it by printing it out
print("my input was: " + my_input)

# Dictionary, List, Tuple and Set

# imagine list as a stack of papers on your table
# you can add new papers to it or remove from it
# a list has an order (it is ordered) and you can access the items
# by an index (they are indexed)
print("---LIST---")
my_list = [98095, 95, 290]  # create a list with []
print(my_list)  # prints: [98095, 95, 290]
my_list.append(1029)  # add to the end of the list
print(my_list)  # prints: [98095, 95, 290, 1029]
print(my_list[0])  # return the first item, prints: 98095
print(my_list.pop())  # return and delete the last item, prints: 1029
print(my_list)  # prints: [98095, 95, 290]

# tuple is like a list that you can't change after it is created
# in programing such objects that you can't change are called "immutable" objects
# it is useful if you know that you will not append or delete items
# tuple is much more efficient in Python than list because
# it does not have all the extra stuff
print("---TUPLE---")
my_tuple = (9, 8, 11)  # create a tuple with ()
print(my_tuple)  # prints: (9, 8, 11)
print(my_tuple[0])  # return the first item, prints: 9
# my_tuple.append(89) # this line would fail. you can't append to tuple

# dictionary is like a real dictionary or an address book
# item in dictionary do not have an order (they are "unordered")
# to access them you have to specify a "key" that you used
# to index the specific "value" with. The same like you would
# find someones address by their name.
print("---DICTIONARY---")
my_dictionary = {"alex": 108, "anna": 95}  # create a dictionary with {}
print(my_dictionary)  # prints: {"alex": 108, "anna": 95}
my_dictionary["marlene"] = 890  # add a new item with a key "marlene" and a value 890
print(my_dictionary)  # prints: {"alex": 108, "marlene": 890, "anna": 95}
print(my_dictionary["marlene"])  # return the value with the key "marlene", prints: 890
print(
    my_dictionary.pop("alex")
)  # return the value and delete the item with a key "alex", prints: 108

# set is like a group of people
# each item in the set is unique and items cannot be repeated
# similarly to tuples sets are immutable and
# therefore cannot be modified
# in addition sets are also unordered (similar to dictionaries)
# and can not be indexed
# they are useful to store a collection of unique options
print("---SET---")
my_set = {"alex", "anna", "marlene", "alex"}  # create a set with {}
print(
    my_set
)  # see that "alex" is in the set only once, prints: {"alex", "marlene", "anna"}
print("alex" in my_set)  # check if "alex" is in the set, prints: True
print("christian" in my_set)  # prints: False

# DYNAMIC TYPING
# Python is a dynamically typed language
# this means that you do not need to specify the datatype of a variable
# Python will figure it out by itself
x = 10  # x is an int
print(type(x))  # <class 'int'>

x = "hello"  # now x is a str
print(type(x))  # <class 'str'>

x = 3.14  # now x is a float
print(type(x))  # <class 'float'>

# find more documentation here:
# https://docs.python.org/3.11/tutorial/index.html
# recommendation: explore it with the Debugger

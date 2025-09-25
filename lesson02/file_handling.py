# -------------------------------
# Python File Handling Basics
# -------------------------------
import os

print(os.getcwd())  # prints the current working directory

# 1. Writing to a file (creates if it doesn't exist, overwrites if it does)
with open("example.txt", "w") as f:  # "w" = write mode
    f.write("Hello, world!\n")
    f.write("Na druhém řádku zdravím všechny v češtině.\n")

# 2. Appending to a file (adds to the end without overwriting existing content)
with open("example.txt", "a") as f:  # "a" = append mode
    f.write("Tento řádek je přidán.\n")

# 3. Reading the entire file at once
with open("example.txt", "r") as f:  # "r" = read mode
    content = f.read()
    print("--- File content (read all at once) ---")
    print(content)

# 4. Reading line by line
with open("example.txt", "r") as f:
    print("--- File content (line by line) ---")
    for line in f:
        print(line.strip())  # strip() removes newline characters

# 5. Safe file deletion (optional)
if os.path.exists("example.txt"):
    os.remove("example.txt")
    print("File deleted.")
else:
    print("File does not exist.")

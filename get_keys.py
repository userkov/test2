import os

with open(".env", "r") as file:
    for line in file:
        line = line.replace("\n", "")
        try:
            os.environ[line[:line.find("=")]] = line[line.find("=") + 1:]
        except ValueError:
            print("Value Error")


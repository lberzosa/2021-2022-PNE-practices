from pathlib import Path

# -- Constant with the new the file to open
FILENAME = "RNU6_269P.txt"
filename = input("introduce a filename: ")

# -- Open and read the file
try:
    file_contents = Path(filename).read_text()
# -- Print the contents on the console
    print(file_contents)
except FileNotFoundError:
    print("file is not found, try again")
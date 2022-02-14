from pathlib import Path

# -- Constant with the new the file to open
filename = input("introduce a filename: ")

# -- Open and read the file
try:
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines() #separar en lineas
    head = lines[0] #coger solo la linea 0
    print(f"head of the: {filename} file:")
    print(head)
except FileNotFoundError:
    print("file is not found, try again")
except IndexError:
    print(f"[ERROR]: file '{filename}' is empty")
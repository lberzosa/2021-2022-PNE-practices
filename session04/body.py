from pathlib import Path

# -- Constant with the new the file to open
filename = input("introduce a filename: ")

# -- Open and read the file
try:
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines() #separar el fichero en lineas
    body = lines[1:] #imprimir desde la linea 1 hasta el final
    print(f"body of the: {filename} file:")
    for line in body: #line: lineas del cuerpo del fichero
        print(line)
except FileNotFoundError:
    print("file is not found, try again")
except IndexError:
    print(f"[ERROR]: file '{filename}' is empty")
import os


def readLasFile(path:str) -> str:
    """
    Reads a .las file and returns as one big string.
    """
    file_extension = os.path.splitext(path)[1]
    if file_extension == ".las":
        try:
            with open(path, 'r') as lf:
                return lf.read()
        except Exception as e:
            print(e, "[readLasFile]::Error reading .las file!", repr(e))
    else:
        raise Exception("File supplied is not a .las file!")


import os


def readLasFile(path: str) -> str:
    """
    :param str path: File path to a .las file

    Reads a .las file and returns as one big string.
    """
    file_extension = os.path.splitext(path)[1]
    if str(file_extension).lower() != ".las":
        raise Exception("File supplied is not a .las file!")
    else:
        try:
            try:
                lf = open(path, 'r')
                lf_data = lf.read()
            except UnicodeDecodeError:
                lf = open(path, 'r', encoding='Latin-1')
                lf_data = lf.read()
            lf.close()
            if lf_data == "":
                raise Exception("Empty .las file found!")
            else:
                return lf_data
        except Exception as e:
            err = "\n\n[readLasFile]::Error reading .las file!\n\n"
            print(e, err, repr(e))                


def saveJsonData(path: str, jsonData: dict) -> None:
    import json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)

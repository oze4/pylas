def readLasFile(path):
    try:
        with open(path, 'r') as lf:
            las = lf.read()
        return las
    except:
        return None


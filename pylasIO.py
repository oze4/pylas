def readLasFile(path):
    with open(path, 'r') as lf:
        las = lf.read()
    return las


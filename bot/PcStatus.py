

def getStatus():
    import psutil

    # gives a single float value
    #psutil.cpu_percent()
    # gives an object with many fields
    #psutil.virtual_memory()
    # you can convert that object to a dictionary
    #dict(psutil.virtual_memory()._asdict())
    # you can have the percentage of used RAM

    # you can calculate percentage of available memory
    return "<ins>CPU</ins>"\
           + "\nCPU Usage: " + str(round(psutil.cpu_percent(), 2)) + "%"\
           + "\n\n<ins>MEMORY</ins>"\
           + "\nIn Use: " + str(round(psutil.virtual_memory().percent, 2)) + "%"\
           + "\nAvaliable: " + str(round((psutil.virtual_memory().used / 1073741824), 2)) + "Gb"\
           + "\nTotal: " + str(round((psutil.virtual_memory().total / 1073741824), 2)) + "Gb"
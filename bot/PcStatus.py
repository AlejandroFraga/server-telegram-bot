import psutil

# Variables
kb = 1024
mb = kb * kb
gb = mb * kb


def get_status():

    # gives a single float value
    #psutil.cpu_percent()
    # gives an object with many fields
    #psutil.virtual_memory()
    # you can convert that object to a dictionary
    #dict(psutil.virtual_memory()._asdict())
    # you can have the percentage of used RAM

    # you can calculate percentage of available memory
    return cpu_status() + "\n\n"\
           + memory_status()


def cpu_status():
    return "<ins>CPU</ins>"\
       + "\nCPU Usage: " + format_percent(psutil.cpu_percent())


def memory_status():

    return "<ins>MEMORY</ins>"\
       + "\nIn Use: " + format_percent(psutil.virtual_memory().percent)\
       + "\nAvaliable: " + format_bytes(psutil.virtual_memory().used)\
       + "\nTotal: " + format_bytes(psutil.virtual_memory().total)


def format_percent(value):
    return str(round(value, 2)) + " %"


def format_bytes(value):
    if value <= kb:
        return to_b(value)
    elif value <= mb:
        return to_kb(value)
    elif value <= gb:
        return to_mb(value)
    else:
        return to_gb(value)


def to_b(value):
    return str(round(value, 2)) + " B"


def to_kb(value):
    return str(round(value / kb, 2)) + " KB"


def to_mb(value):
    return str(round(value / mb, 2)) + " MB"


def to_gb(value):
    return str(round(value / gb, 2)) + " GB"

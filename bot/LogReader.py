

def getMap(newMap, total):
    string = "\nTOP ACCESS TRIES\n----------------\n\n"

    i = 0
    limit = 25

    for chain in newMap:
        i +=1
        string += "TOP " + str(i) + " " + str(chain) + "\n"
        if i >= limit:
            break

    string += "\nTOTAL\n-----\n" + str(total) + "\n"
    return string
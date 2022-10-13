
def parseDictToQuery(dictionary):
    '''
    This method parses a dictionary to convert it into field queries
    '''
    query = ""

    for key in dictionary:
        # If the current value is a sub-dict, parse it recursively
        if type(dictionary[key]) == dict:
            query += f"{key}({parseDictToQuery(dictionary[key])})"

        else:
            query += key

        query += ","

    # Remove final comma
    return query[:-1]



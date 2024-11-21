from typing import Optional

def sort_transactions(sort:str, createdAt:Optional[bool]=None)->dict:
    theOrder = {}

    match (sort):
        case "Latest":
            if createdAt != None:
                theOrder = {"createdAt": "desc" }
            else:
                theOrder = {"date":'desc'}

        case "Oldest":
            if createdAt != None:
                theOrder = { "createdAt": "asc" }
            else:
                theOrder = {"date":'asc'}

        case "A-Z":
            theOrder = { "name": "asc" }

        case "Z-A":
            theOrder = { "name": "desc" }

        case "Highest":
            theOrder = { "amount": "desc" }

        case _:
            theOrder = { "amount": "asc" }
    
    return theOrder
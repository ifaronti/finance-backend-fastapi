from typing import Optional

def sort_transactions(sort:str, createdAt:Optional[bool]=None)->dict:
    theOrder = {}

    match (sort):
        case "Latest":
            if createdAt != None:
                theOrder = f'b."createdAt" DESC'
            else:
                theOrder = {"date":'desc'}

        case "Oldest":
            if createdAt != None:
                theOrder = f'b."createdAt" ASC'
            else:
                theOrder = {"date":'asc'}

        case "A-Z":
            theOrder = f'b.name ASC' if createdAt else { "name": "asc" }

        case "Z-A":
            theOrder = f'b.name DESC' if createdAt else { "name": "desc" }

        case "Highest":
            theOrder = f'b.amount DESC' if createdAt else { "amount": "desc" }

        case _:
            theOrder = f'b.amount ASC' if createdAt else { "amount": "asc" }
    
    return theOrder
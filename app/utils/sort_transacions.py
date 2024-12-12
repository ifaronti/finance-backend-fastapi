from typing import Optional

def sort_transactions(sort:str, createdAt:Optional[bool]=None)->str:
    theOrder = ''
    match (sort):
        case "Latest":
            if createdAt != None:
                theOrder = f'b."createdAt" DESC'
            else:
                theOrder = 't.date DESC'

        case "Oldest":
            if createdAt != None:
                theOrder = f'b."createdAt" ASC'
            else:
                theOrder = 't.date ASC'

        case "A-Z":
            theOrder = f'b.name ASC' if createdAt else f't.name ASC'

        case "Z-A":
            theOrder = f'b.name DESC' if createdAt else 't.name DESC'

        case "Highest":
            theOrder = f'b.amount DESC' if createdAt else 't.amount DESC'

        case "Lowest":
            theOrder = f'b.amount ASC' if createdAt else 't.amount ASC'
    
    return theOrder.strip("'")
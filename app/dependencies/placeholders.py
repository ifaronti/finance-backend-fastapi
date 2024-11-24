import json

def data_format(arr:list, userId:str|int):
    new_arr = []
    for i in arr:
        i["userId"] = userId
        for v in i:
            if i[v] == "True":
                i[v] = True
            if i[v] == "False":
                i[v] = False
        new_arr.append(i)
    return new_arr

with open('placeholders.json') as file:
    data = json.load(file)

def placeholders(userId):
    transactions = data_format(data["transactions"], userId)
    budgets = data_format(data["budgets"], userId)
    pots = data_format(data["pots"], userId)
    bills = data_format(data["bills"], userId)

    return {"bills":bills, "pots":pots, "budgets":budgets, "transactions":transactions}

def account_balance():
    income = data["balance"]["income"]
    current = data["balance"]["current"]
    expenses = data["balance"]["expenses"]
    
    return {"income":income, "current":current, "expenses":expenses}
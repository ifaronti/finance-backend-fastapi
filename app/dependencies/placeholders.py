import json

def data_format(arr:list):
    new_arr = []
    for i in arr:
        for v in i:
            if i[v] == "True":
                i[v] = True
            if i[v] == "False":
                i[v] = False
        new_arr.append(i)
    return new_arr

with open('placeholders.json') as file:
    data = json.load(file)

def placeholders():
    transactions = data_format(data["transactions"], )
    budgets = data_format(data["budgets"], )
    pots = data_format(data["pots"], )
    bills = data_format(data["bills"], )

    return {"bills":bills, "pots":pots, "budgets":budgets, "transactions":transactions}

def account_balance():
    income = data["balance"]["income"]
    balance = data["balance"]["current"]
    expenses = data["balance"]["expenses"]
    
    return {"income":income, "balance":balance, "expenses":expenses}
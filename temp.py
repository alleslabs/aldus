import json

contracts = json.load(open("./data/terra/phoenix-1/contracts.json"))

for contract in contracts:
    contract["code"] = int(contract["code"])

json.dump(contracts, open("./data/terra/phoenix-1/contracts.json", "w"), indent=2)

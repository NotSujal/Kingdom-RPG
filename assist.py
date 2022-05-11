import json, math
import difflib
from difflib import SequenceMatcher
from replit import db

# def savedata(user:str,key:str,value:str):
    
#     #load data
#     user = str(user)
#     key = str(key)
#     value = str(value)

#     # check if player exists or not
#     try:
#         data = db[user]
#     except KeyError:
#         # User doesnt exists, create a new user
#         db[user] = {}
#         data = {}

#     # Update data in database
#     try: data = json.loads(str(data.value))
#     except: data = json.loads(str(data))
    
#     data[key] = value
#     db[user] = json.dumps(data)
#     return f"{key}: {value}"
    


def clrscr():
    keys = db.keys()
    for key in keys: 
        print(db[key])
        del db[key]

def savedata(user:str,key:str,value:str):
    # load data
    user = str(user)
    key = str(key)
    with open('data/players.json','r') as f:
        data = json.load(f)
        try:
            data[user][key] = value
            
        except:
            # Either User or key doesnt exists
            try:
                data[user]
            except:
                # User doesnt exist Confirmed
                data[user] = {}

            data[user][key] = value
    
    with open('data/players.json','w') as f:
        json.dump(data,f,indent=4)

    return f"{key} : {value}"
    
# def getdata(user:str,key:str,absent):
#     user = str(user)
#     key = str(key)
#     absent = str(absent)
#     # Check of Player exists or not
#     try:
#         data = db[user]
#     except KeyError:
#         # User doesnt exists, create a new user
#         db[user] = {}
#         data = {}
#         savedata(user,key,absent)
#         return absent
        
#     data = json.loads(str(data))

#     # check if key exists or not
#     try:
#         return data[key]
#     except:
#         savedata(user,key,absent)
#         return absent

        
    
def getdata(user:str,key:str,absent):
    user = str(user)
    key = str(key)
    with open('data/players.json','r') as f:
        data = json.load(f)

        try:
            return data[user][key]
        except:
            savedata(user,key,absent)
            return absent


def addcoins(user:str,amount) -> int:
    state = True
    user = str(user)
    money = int(getdata(user, "coins","0"))
    money += amount
    if money <=0:
        money = 0
        state = False
        
    savedata(user,"coins",str(money))
    return state




def addinventory(user:str,item:str,amount:int):
    user = str(user)
    item = str(item)
    
    inv = getdata(user, "inv",{})
    
    if type(inv) is not dict:
        inv = {}
    if item in inv:
        current_count = int(inv[item])
        current_count += int(amount)
    else:
        current_count = int(amount)
        
    inv[item] = str(current_count)

    for key,val in inv.items():
        if int(val) <= 0:
            del inv[key]
            break

    savedata(user, "inv",inv)
    return inv




def auto_complete(key,filename="locations"):
    with open(f"data/{filename}.json",'r') as f:
        words = list(json.load(f).keys())
    _list = difflib.get_close_matches(key, words)
    if len(_list) >0:
        similarity = {}
        for item in _list:
            num = int(SequenceMatcher(None, item, key).ratio() * 100)
            similarity[num] = item

        return similarity[sorted(similarity,reverse=True)[0]]
    else: return False

        

def player_debug(user):
    with open("data/players.json",'r') as f:
        player =  json.load(f)[str(user)]
        return json.dumps(player,indent = 2)
    

def check_lvlup(curr_lvl,curr_xp):
    req_xp =  420/69 * curr_lvl + 100
    if curr_xp >= req_xp:
        return math.ceil(req_xp),True
    else: return math.ceil(req_xp),False





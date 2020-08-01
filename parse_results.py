import os
import json

dirname = "./results"
players = {}
round1 = {}
round2 = {}
round3 = {}
rounds = [round1, round2, round3]

for filename in os.listdir(dirname):
    with open(dirname + "/" + filename, "r") as f:
        player_id = filename[:-4]  
        for line in f.readlines():
            if line.startswith("Player Name:"):  # first line
                players[player_id] = line.split(":")[1].strip()  # parse name
            elif line.startswith("ROUND SKIPPED"):
                continue
            elif line.startswith("ROUND "):
                round_num = int(line.split(" ")[1].strip())  
                cur_round_list = rounds[round_num - 1]  # sub 1 b/c rounds = 1,2,3 but round list 0-idx 
                if player_id not in cur_round_list:  # adding first element for this player
                    cur_round_list[player_id] = []
            elif len(line) > 1:  # not just newline so should be obj line
                temp1 = line.split(".", 1)
                obj_num = int(temp1[0].strip())
                temp2 = temp1[1].strip().split("-", 1)
                cat = temp2[0].strip()
                temp3 = temp2[1].strip().split(":", 1)
                word = temp3[0].strip()
                pic = temp3[1].strip()
                element = {"obj_num": obj_num, "cat": cat, "word": word, "pic": pic}
                cur_round_list[player_id].append(element)

appdir = "./house-hunt/src/"

names_dict = json.dumps(players)
with open(appdir+"names.json", "w+") as f:
    f.write(names_dict)

rounds_data = {"round1": round1, "round2": round2, "round3": round3}
data_dict = json.dumps(rounds_data)
with open(appdir+"data.json", "w+") as f:
    f.write(data_dict)

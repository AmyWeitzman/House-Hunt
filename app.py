from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse 
from Player import Player 
import random
import json

app = Flask(__name__)

letters = 'ABCDEFGHLMNOPRSTW'
categories = {'Food/Beverage', 'Clothing Item', 'School Supply', 'Container', 'Movie', 'Color', 'Animal', 'Outdoors', 'Item in Bathroom', 'Item in Garage', 'Adjective', 'Occupation', 'Item in Kitchen', 'Music', 'Sports', 'Foreign', 'Cold', 'Hot', 'Holiday Item', 'Compound Word', 'Book', 'Long', 'Short', 'Winter', 'Summer', 'Technology', 'Game/Leisure', 'Expensive', 'Nature', 'Travel', 'Ends With Letter', 'Messy', 'Wet', 'Rectangular', 'Rounded', 'Soft', 'Hard', 'Turn Off', 'Used Daily', 'Rarely Used', 'Usually Taken on Vacation', 'High', 'Low', 'Use Up and Replace', 'In Your Room', '21st Century Item', 'Sweet', 'Noisy', 'Recyclable'}
players = {}  # dictionary of Player objects, identify players by their phone numbers

round1_letter = letters[random.randint(0, len(letters) - 1)]  # pick a random letter
round1_cats = random.sample(categories, 5)  # randomly pick 5 categories

round2_letter = letters[random.randint(0, len(letters) - 1)]  # pick a random letter
round2_cats = random.sample(categories, 5)  # randomly pick 5 categories

round3_letter = letters[random.randint(0, len(letters) - 1)]  # pick a random letter
round3_cats = random.sample(categories, 5)  # randomly pick 5 categories

round_info = {1: {"letter": round1_letter, "cats": round1_cats}, 
              2: {"letter": round2_letter, "cats": round2_cats},
              3: {"letter": round3_letter, "cats": round3_cats}}

write_round_info()

@app.route("/", methods=['GET', 'POST'])
def reply():
    number = request.values.get('From', None)  # keep track of who text is from

    if number not in players:
        # new player
        name = request.values.get('Body', None)
        players[number] = Player(name, number)   # key = num b/c mult peeps could have same name, but nums = unique
        resp = MessagingResponse()
        resp.message("\nHello, " + name + ". Welcome to HOUSE HUNT!")
    else:  # existing player
        player = players[number]
        num_pics = int(request.values.get('NumMedia', 0))

        if num_pics > 0:
            # player sent pic of object for current round
            obj = request.values.get('Body', None)
            obj_num = obj.split(".")[0].strip()
            obj_txt = obj.split(".")[1].strip()
            pic_url = request.values.get('MediaUrl0', None)  
            player.add_obj(obj_num, obj_txt, pic_url)
            if player.get_obj_cnt() == 5:  # last obj for cur round, move to next round
                msg = "Got it, " + player.get_name() + ".\n"
                if player.get_round() == 3:  # finished, cannot go to a next round
                    name = player.get_name()
                    resp = MessagingResponse()
                    msg += "\nCongrats, " + name + "! You have finished the game. Thank you for playing!"
                    del players[number]
                else:
                    player.inc_round()
                    player.reset_obj_cnt()
                    msg += get_round_info(player)
                resp = MessagingResponse()
                resp.message(msg)
            else:  # same round
                resp = MessagingResponse()
                resp.message("Got it, " + player.get_name() + ". " + str(5 - player.get_obj_cnt()) + " to go.")
        else:   # sent keyword, perform appropriate action: go, skip, quit
            keyword = request.values.get('Body', None).lower()
            if keyword == "skip":
                # skip to next round
                if player.get_round() == 3:  # finished, cannot go to a next round
                    name = player.get_name()
                    resp = MessagingResponse()
                    resp.message("\nCongrats, " + name + "! You have finished the game. Thank you for playing!")
                    del players[number]
                else:
                    player.inc_round()
                    player.reset_obj_cnt()
                    player.update_file()
                    resp = MessagingResponse()
                    resp.message(get_round_info(player))
            elif keyword == "og":
                # end game for this player
                number = request.values.get('From', None)
                name = player.get_name()
                resp = MessagingResponse()
                resp.message("\nOk, " + name + ". Thank you for playing.")
                del players[number]
            elif keyword == "go":
                # start game for this player
                resp = MessagingResponse()
                resp.message(get_round_info(player))
            else:  # PROBLEM
                resp = MessagingResponse()
                resp.message("INVALID RESPONSE")

    return str(resp) 

def get_round_info(player):
    round_num = player.get_round()
    text = ""
    letter = round_info[round_num]["letter"]
    cats = round_info[round_num]["cats"]

    text += "\nRound " + str(round_num) + "\n"
    text += "Your letter is " + letter + "\n"
    for idx, cat in enumerate(cats):
        text += str(idx + 1) + ". " + cat + "\n"

    player.set_cats(cats)

    return text

def write_round_info():
    appdir = "./house-hunt/src/"
    round_info_dict = json.dumps(round_info)
    with open(appdir+"round_info.json", "w+") as f:
        f.write(round_info_dict)

if __name__ == "__main__":
    app.run(debug=True)
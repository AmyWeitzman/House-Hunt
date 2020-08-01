class Player():
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.round = 1
        self.obj_cnt = 0
        self.cats = []
        self.file = f"./results/{number}.txt"

        with open(self.file, "a+") as f:
            f.write("Player Name: " + name + "\n\n") 
            f.write("ROUND " + str(self.round) + "\n")   

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def get_round(self):
        return self.round

    def get_obj_cnt(self):
        return self.obj_cnt

    def set_cats(self, cats):
        self.cats = cats

    def inc_round(self):
        self.round += 1

    def reset_obj_cnt(self):
        self.obj_cnt = 0

    def update_file(self):   # player skipped, set file for next round
        with open(self.file, "a+") as f:
            f.write("ROUND SKIPPED\n")
            f.write("\nROUND " + str(self.round) + "\n")

    def add_obj(self, obj_num, obj_txt, pic_url):
        with open(self.file, "a+") as f:
            self.obj_cnt += 1
            f.write(obj_num + ". " + self.cats[int(obj_num) - 1] + " - " + obj_txt + ": " + pic_url + "\n")
            if (self.obj_cnt == 5) and (self.get_round() < 3): 
                f.write("\nROUND " + str(self.round + 1) + "\n")
        
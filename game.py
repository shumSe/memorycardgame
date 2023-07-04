import time
import tkinter as tk
import leaderboard as lb
from PIL import ImageTk, Image
from random import sample

from enums import FruitsImagesType


def get_image_by_type(type):
    image = FruitsImagesType.get_image(type)
    return image


class Game:

    def __init__(self, window):

        self.game_over = False

        self.board_sizes = [(4, 3), (4, 4), (5, 4)]
        self.game_size = self.board_sizes[0]
        self.cards_count = self.game_size[0] * self.game_size[1]

        self.start_time = time.time()
        self.end_time = 60
        self.enable_timer = True

        self.player_name = ""
        self.player_score = 0
        self.player_time = 0

        self.hidden_card = ImageTk.PhotoImage(Image.open("Images/hidden.gif"))

        self.blank_card = ImageTk.PhotoImage(Image.open("Images/blank.gif"))

        self.turned_cards_visible = 0
        self.turned_cards_ids = []
        self.selected_cards = []
        self.found_cards = []
        self.cards_type = []

        self.window = window
        self.main_frame = tk.Frame(self.window)
        self.cards_frame = tk.Frame(self.window)

    def load_cards(self):
        images_count = 10

        cards_type_list = list(range(1, images_count + 1))
        chosen_cards = sample(cards_type_list, k=self.cards_count // 2)

        result = []

        for card in chosen_cards:
            imageType = FruitsImagesType(card)
            image = FruitsImagesType.get_image(imageType)
            result.append(image)

        return result

    def setup_cards(self):
        memory_cards = self.load_cards() * 2
        return sample(memory_cards, k=len(memory_cards))

    def check_game_over(self):
        if self.game_over:
            self.enable_timer = False
            self.open_game_over_window(0)

        if len(self.found_cards) == self.cards_count:
            self.game_over = True
            self.player_time = self.timer()
            self.enable_timer = False
            lb.add_player(self.player_name, self.player_score, self.player_time)
            self.open_game_over_window(1)

    def open_game_over_window(self, state):
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")
        game_over_window.geometry("300x200")
        end_text = ""
        if state == 0:
            end_text = "Game Over. Out of time"
        else:
            end_text = f"Game Over. The score is {self.player_score}. The time is {self.player_time}"
        tk.Label(
            master=game_over_window,
            text=end_text
        ).grid(row=0, column=0)

    def setup_game_frame(self):
        self.cards_frame.destroy()
        self.cards_frame = tk.Frame(self.window)
        self.cards_frame.grid(row=1, column=1)

        self.btn_cards = [tk.Button(self.cards_frame,
                                    image=self.hidden_card,
                                    command=lambda x=i: self.show(x))
                          for i in range(self.cards_count)]

        for count in range(self.cards_count):
            self.btn_cards[count].grid(row=count // self.game_size[0],
                                       column=count % self.game_size[0])

    def show_one_card(self, card_id):
        self.btn_cards[card_id].config(image=self.cards_type[card_id])
        self.turned_cards_visible += 1
        self.turned_cards_ids.append(self.cards_type[card_id])
        self.selected_cards.append(card_id)

    def show(self, item):
        if item not in self.found_cards:
            if self.turned_cards_visible == 0:
                self.show_one_card(card_id=item)
            elif self.turned_cards_visible == 1:
                if item != self.selected_cards[-1]:
                    self.show_one_card(card_id=item)
        if self.turned_cards_visible == 2:
            self.window.after(750, self.check)

    def check(self):
        if self.turned_cards_visible != 2:
            return
        if self.turned_cards_ids[-1] == self.turned_cards_ids[-2]:
            self.update_score()
            self.found_cards.append(self.selected_cards[-1])
            self.found_cards.append(self.selected_cards[-2])
            self.btn_cards[self.selected_cards[-1]].configure(
                image=self.blank_card)
            self.btn_cards[self.selected_cards[-2]].configure(
                image=self.blank_card)
            self.check_game_over()
        self.redraw()

    def redraw(self):
        for i in range(self.cards_count):
            if i not in self.found_cards:
                self.btn_cards[i].configure(image=self.hidden_card)
        self.turned_cards_visible = 0

    def start_new_game(self):
        self.display_player_score()
        self.cards_type = self.setup_cards()
        self.setup_game_frame()
        self.start_time = time.time()
        self.timer()

    def play_easy(self):
        self.game_size = self.board_sizes[0]
        self.cards_count = self.game_size[0] * self.game_size[1]
        self.end_time = 60
        self.start_new_game()

    def play_medium(self):
        self.game_size = self.board_sizes[1]
        self.cards_count = self.game_size[0] * self.game_size[1]
        self.end_time = 45
        self.start_new_game()

    def play_hard(self):
        self.game_size = self.board_sizes[2]
        self.cards_count = self.game_size[0] * self.game_size[1]
        self.end_time = 30
        self.start_new_game()

    def display_player_score(self):
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid(row=0, column=1)

        self.label_player_name = tk.Label(
            master=self.main_frame,
            text=f' {self.player_name} : ',
            font=("Roboto", 20),
        )
        self.label_player_name.grid(row=0, column=0)

        self.label_player_score = tk.Label(
            master=self.main_frame,
            text='0',
            font=("Roboto", 20)
        )
        self.label_player_score.grid(row=0, column=1)

        self.label_timer = tk.Label(
            master=self.main_frame,
            text="",
            font=("Roboto", 20),
            fg="red",
        )
        self.label_timer.grid(row=0, column=2)

    def timer(self):
        seconds = time.time() - self.start_time
        self.label_timer.config(text=str(seconds)[:5])
        if int(seconds) >= self.end_time:
            self.game_over = True
            self.check_game_over()
        if self.enable_timer:
            self.label_timer.after(100, self.timer)
        return str(seconds)[:6]

    def update_score(self):
        self.player_score += 1
        self.label_player_score.configure(text=str(self.player_score))

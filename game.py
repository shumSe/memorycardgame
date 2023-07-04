import tkinter as tk
from typing import List

from PIL import ImageTk, Image
from random import sample

from enums import FruitsImagesType


def get_image_by_type(type):
    image = FruitsImagesType.get_image(type)
    return image


class Game:

    def __init__(self, window):

        # self.player1 = None
        # self.current_player = None
        self.player_nb = 1
        self.game_mode = "Alone"
        self.game_over = False

        self.DIMENSIONS = [(5, 4), (6, 4)]
        self.game_dim = self.DIMENSIONS[0]
        self.cards_count = self.game_dim[0] * self.game_dim[1]  # Количество карт

        self.hidden_card = ImageTk.PhotoImage(Image.open("Images/hidden.gif"))

        self.blank_card = ImageTk.PhotoImage(Image.open("Images/blank.gif"))

        self.cards_list = []

        self.turned_cards_visible = 0  # Number of visible cards
        self.turned_cards_ids = []  # List of index of turned over cards
        self.selected_cards = []
        self.found_cards = []  # List of index of found pairs
        self.cards_type = []  # List of index of cards

        self.window = window
        self.radio_button_choice = tk.IntVar()
        # self.set_radio_buttons()
        self.main_frame = tk.Frame(self.window, height=500, width=500)
        self.cards_frame = tk.Frame(self.window)


    def load_cards(self):
        """
        Loads the cards images and returns a list of cards

        Returns
        -------
        List[tk.PhotoImage]
            List containing unique cards (images) chosen randomly.

        """

        images_count = 10  # TODO: вынести в константу, загрузить по 12 картинок каждого типа

        cards_type_list = list(range(1, images_count + 1))
        chosen_cards = sample(cards_type_list, k=self.cards_count // 2)

        result = []

        for card in chosen_cards:
            imageType = FruitsImagesType(card)
            image = FruitsImagesType.get_image(imageType)
            result.append(image)

        return result

    def initiate_game(self):
        """
        Returns
        -------
        List[tk.PhotoImage]
            List of pairs of cards (images object) randomly mixed.

        """
        memory_cards = self.load_cards() * 2
        return sample(memory_cards, k=len(memory_cards))


    def check_game_over(self):
        if len(self.found_cards) == self.cards_count:
            self.game_over = True
            self.open_game_over_window()

    def open_game_over_window(self):
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")
        game_over_window.geometry("300x200")
        tk.Label(
            master=game_over_window,
            # text=f"Game Over. The score is {score}"
            text=f"Game Over"
        ).grid(row=0, column=0)

    def set_up_memory_frame(self):
        self.cards_frame.destroy()
        # self.radio_buttons_frame.destroy()
        self.cards_frame = tk.Frame(self.window)
        self.cards_frame.grid(row=1, column=1)

        self.but_cards = [tk.Button(self.cards_frame,
                                    image=self.hidden_card,
                                    command=lambda x=i: self.show(x))
                          for i in range(self.cards_count)]

        for count in range(self.cards_count):
            self.but_cards[count].grid(row=count // self.game_dim[0],
                                       column=count % self.game_dim[0])

    def show_one_card(self, card_id):
        self.but_cards[card_id].config(image=self.cards_type[card_id])
        self.turned_cards_visible += 1
        self.turned_cards_ids.append(self.cards_type[card_id])
        self.selected_cards.append(card_id)

    def show(self, item):
        if item not in self.found_cards:
            # and self.current_player.can_play:
            if self.turned_cards_visible == 0:
                self.show_one_card(card_id=item)
            elif self.turned_cards_visible == 1:
                if item != self.selected_cards[-1]:
                    self.show_one_card(card_id=item)
        if self.turned_cards_visible == 2:
            self.window.after(2000, self.check)

    def check(self):
        if self.turned_cards_visible != 2:
            return
        if self.turned_cards_ids[-1] == self.turned_cards_ids[-2]:
            self.found_cards.append(self.selected_cards[-1])
            self.found_cards.append(self.selected_cards[-2])
            self.but_cards[self.selected_cards[-1]].configure(
                image=self.blank_card)
            self.but_cards[self.selected_cards[-2]].configure(
                image=self.blank_card)
            self.check_game_over()

        # elif self.player_nb == 2:
        #     self.switch_players()

        self.reinit()

    def reinit(self):
        """
        Hides all cards and resets the number of visible cards

        Returns
        -------
        None.

        """

        for i in range(self.cards_count):
            if i not in self.found_cards:
                self.but_cards[i].configure(image=self.hidden_card)
        self.turned_cards_visible = 0

    # def reset_game(self):
    #     self.reset_scores()
    #     self.current_player = self.player1
    #     self.turned_cards_nb = 0
    #     self.found_cards = []
    #     self.turned_cards_ids = []
    #     self.turned_card_played = []
    #     self.game_over = False

    def start_new_game(self):
        """
        Start a new memory game with set dimensions and players.

        Resets game parameters.
        Load a new memory to start a new game.

        Returns
        -------
        None.

        """

        # if self.player_nb == 1:
        #     self.display_stat_1player()
        # else:
        #     self.display_players_score()

        self.cards_type = self.initiate_game()
        # self.reset_game()
        self.set_up_memory_frame()

    def play_alone(self):
        self.player_nb = 1
        self.game_mode = 'Alone'
        self.start_new_game()

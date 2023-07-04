from tkinter import ttk
from tkinter.constants import NO, CENTER, END

from game import Game

import tkinter as tk
import leaderboard as lb


def main():
    window = tk.Tk()
    window.title("Memory game")

    memory_game = Game(window)
    # menus
    top = tk.Menu(window)
    window.config(menu=top)
    jeu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Game', menu=jeu)
    submenu = tk.Menu(jeu, tearoff=False)
    jeu.add_cascade(label='New Game', menu=submenu)

    player_name_input = tk.Entry(window, width=50)
    player_name_input.insert(0, "Enter your name")
    player_name_input.pack()

    def start_game(mode):
        player_name = player_name_input.get()
        if player_name == "Enter your name" or player_name == "You should input name":
            player_name_input.delete(0, END)
            player_name_input.insert(0, "You should input name")
        else:
            my_leaderboard.destroy()
            player_name_input.destroy()
            memory_game.player_name = player_name
            if mode == 0:
                memory_game.play_easy()
            elif mode == 1:
                memory_game.play_medium()
            elif mode == 2:
                memory_game.play_hard()

    submenu.add_command(
        label='Easy',
        command=lambda: start_game(0)
    )
    submenu.add_command(
        label='Medium',
        command=lambda: start_game(1)
    )
    submenu.add_command(
        label='Hard',
        command=lambda: start_game(2)
    )
    jeu.add_command(label='Close', command=window.destroy)

    help_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='Rules', )

    lb.create_table()
    my_leaderboard = ttk.Treeview(window)
    my_leaderboard['columns'] = ('id', 'name', 'score', 'time')

    my_leaderboard.column("#0", width=0, stretch=NO)
    my_leaderboard.column("id", anchor=CENTER, width=40)
    my_leaderboard.column("name", anchor=CENTER, width=200)
    my_leaderboard.column("score", anchor=CENTER, width=100)
    my_leaderboard.column("time", anchor=CENTER, width=100)

    my_leaderboard.heading("#0", text="", anchor=CENTER)
    my_leaderboard.heading("id", text="Id", anchor=CENTER)
    my_leaderboard.heading("name", text="Name", anchor=CENTER)
    my_leaderboard.heading("score", text="Score", anchor=CENTER)
    my_leaderboard.heading("time", text="Time, sec.", anchor=CENTER)

    for row in lb.show_table():
        pl_id = row[0]
        pl_name = row[1]
        pl_score = row[2]
        pl_time = row[3]
        my_leaderboard.insert(parent="", index='end', iid=row[0], text="",
                              values=(f'{pl_id}', f'{pl_name}', f'{pl_score}', f'{pl_time}'))

    my_leaderboard.pack()

    # Launch GUI
    window.mainloop()


if __name__ == '__main__':
    main()

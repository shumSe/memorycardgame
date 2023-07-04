from tkinter import ttk
from tkinter.constants import NO, CENTER, END

from game import Game

import tkinter as tk
import leaderboard as lb


def main():
    window = tk.Tk()
    window.title("Memory game")
    window.resizable(0,0)

    memory_game = Game(window)
    top = tk.Menu(window)
    window.config(menu=top)
    game_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Game', menu=game_menu)
    submenu = tk.Menu(game_menu, tearoff=False)
    game_menu.add_cascade(label='New Game', menu=submenu)

    player_name_input = tk.Entry(window, width=50)
    player_name_input.insert(0, "Enter your name")
    player_name_input.pack()

    def start_game(mode):
        player_name = player_name_input.get()
        if player_name == "Enter your name" or player_name == "You should input name":
            player_name_input.delete(0, END)
            player_name_input.insert(0, "You should input name")
        else:
            game_menu.entryconfig("New Game", state="disabled")
            my_leaderboard.destroy()
            player_name_input.destroy()
            memory_game.player_name = player_name
            if mode == 0:
                memory_game.play_easy()
            elif mode == 1:
                memory_game.play_medium()
            elif mode == 2:
                memory_game.play_hard()

    def open_rules():
        rules_window = tk.Toplevel(window)
        rules_window.title("Rules")
        rules_window.geometry("300x200")
        easy_text = "Easy - Board size: 4x3 - Time: 60 seconds"
        medium_text = "Medium - Board size: 4x4 - Time: 45 seconds"
        hard_text = "Hard - Board size: 5x4 - Time: 30 seconds"
        tk.Label(
            master=rules_window,
            text=easy_text
        ).grid(row=0, column=0)
        tk.Label(
            master=rules_window,
            text=medium_text
        ).grid(row=1, column=0)
        tk.Label(
            master=rules_window,
            text=hard_text
        ).grid(row=2, column=0)

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
    game_menu.add_command(label='Close', command=window.destroy)

    help_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='Rules', command=open_rules)

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

    window.mainloop()

if __name__ == '__main__':
    main()

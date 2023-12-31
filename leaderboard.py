import sqlite3

conn = sqlite3.connect("leaderBoard.db")
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS leaderBoard(name TEXT, score INT, time TEXT)')


def add_player(name,score,time):
    if table_full():  
        if not lowest_score(
                score): 
            c.execute('DELETE FROM leaderBoard WHERE rowid=10')
            c.execute("INSERT INTO leaderBoard (name,score,time) VALUES (?,?,?)",
                      (name, score, time))
            c.execute(
                "CREATE TABLE ordered_board(name TEXT, score INT, time TEXT)")  
            c.execute(
                "INSERT INTO ordered_board (name,score,time) SELECT name,score FROM leaderBoard ORDER BY score DESC ")
            c.execute("DROP TABLE leaderBoard")
            c.execute("ALTER TABLE ordered_board RENAME TO leaderBoard")
    else:  
        c.execute("INSERT INTO leaderBoard (name,score,time) VALUES (?,?,?)",
                  (name, score, time))
        c.execute(
            "CREATE TABLE ordered_board(name TEXT, score INT, time TEXT)")  
        c.execute(
            "INSERT INTO ordered_board (name,score,time) SELECT name,score,time FROM leaderBoard ORDER BY score DESC ")
        c.execute("DROP TABLE leaderBoard")  
        c.execute("ALTER TABLE ordered_board RENAME TO leaderBoard")
    conn.commit()
    c.close()
    conn.close()


def show_table():
    c.execute('SELECT ROWID, name, score, time FROM leaderBoard')
    res = c.fetchall()
    return res


def table_full():
    c.execute('SELECT * FROM leaderBoard')
    amount = c.fetchall()

    return len(amount) >= 10


def lowest_score(score):
    c.execute('SELECT score FROM leaderBoard WHERE score<?', (score,))
    amount = c.fetchall()
    return len(amount) == 0
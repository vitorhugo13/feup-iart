import sqlite3

inFile = open("data.csv", "r")
conn = sqlite3.connect("data.db")
db = conn.cursor()

def write_to_db(db, data):
    sql = "INSERT INTO Player (depth, heuristic, moves, decisiontime, states, cuts, pruned) VALUES (?, ?, ?, ?, ?, ?, 1)"
    db.execute(sql, data["p1"])
    p1_id = db.lastrowid
    db.execute(sql, data["p2"])
    p2_id = db.lastrowid
    winner = 0
    if data["p1won"] == 1 and data["p2won"] == 0:
        winner = 1
    elif data["p1won"] == 0 and data["p2won"] == 1:
        winner = 2
    db.execute(
        "INSERT INTO Game (p1, p2, winner) VALUES (?, ?, ?)",
        (p1_id, p2_id, winner)
        )

data = []
current = {}
counter = 0

for line in inFile:
    if counter == 0:
        fields = line.split(",")
        depth = int(fields[1])
        heuristic = fields[2]
        moves = int(fields[3])
        time = float(fields[4])
        leaves = int(fields[5])
        cuts = int(fields[6])
        p1won = int(fields[7])
        current["p1"] = (depth, heuristic, moves, time, leaves, cuts)
        current["p1won"] = p1won
    elif counter == 1:
        fields = line.split(",")
        depth = int(fields[1])
        heuristic = fields[2]
        moves = int(fields[3])
        time = float(fields[4])
        leaves = int(fields[5])
        cuts = int(fields[6])
        p2won = int(fields[7])
        current["p2"] = (depth, heuristic, moves, time, leaves, cuts)
        current["p2won"] = p2won
    else:
        write_to_db(db, current)
        current = {}
    
    counter += 1
    counter %= 3

conn.commit()
conn.close()


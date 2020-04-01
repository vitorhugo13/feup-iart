DROP TABLE IF EXISTS Player;
CREATE TABLE Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    depth INTEGER NOT NULL,
    heuristic TEXT NOT NULL,
    moves INTEGER NOT NULL,
    decisiontime REAL NOT NULL,
    states INTEGER NOT NULL,
    cuts INTEGER NOT NULL,
    pruned INTEGER NOT NULL
);

DROP TABLE IF EXISTS Game;
CREATE TABLE Game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    p1 INTEGER NOT NULL REFERENCES Player(id) ON DELETE CASCADE,
    p2 INTEGER NOT NULL REFERENCES Player(id) ON DELETE CASCADE,
    winner INTEGER NOT NULL
);

DROP VIEW IF EXISTS Outcome;
CREATE VIEW Outcome AS
SELECT player1.depth AS p1depth, player1.heuristic AS p1heuristic,
player2.depth AS p2depth, player2.heuristic AS p2heuristic,
g.winner AS winner
FROM Game g
JOIN Player player1 ON g.p1 = player1.id
JOIN Player player2 ON g.p2 = player2.id;

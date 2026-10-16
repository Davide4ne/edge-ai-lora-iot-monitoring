CREATE TABLE IF NOT EXISTS rilevazioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    egg INTEGER,
    label TEXT,
    prob REAL
);
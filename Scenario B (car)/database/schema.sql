CREATE TABLE IF NOT EXISTS parcheggio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    auto_rilevate INTEGER,
    posti_liberi INTEGER,
    stato TEXT
);
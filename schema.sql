DROP TABLE IF EXISTS gastos;
DROP TABLE IF EXISTS metas;

CREATE TABLE gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    categoria TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'Variável',
    data DATE DEFAULT (DATE('now', 'localtime'))
);

CREATE TABLE metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL, -- 'Global' ou o nome da categoria (ex: 'Lazer')
    valor_limite REAL NOT NULL,
    mes TEXT NOT NULL, -- Formato YYYY-MM
    UNIQUE(categoria, mes) -- Impede metas duplicadas no mesmo mês
);
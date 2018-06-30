DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS SecondPartyAliases;
DROP TABLE IF EXISTS SecondParties;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Accounts;

CREATE TABLE Accounts (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    balance FLOAT NOT NULL DEFAULT 0.0
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TABLE SecondParties (
    id INTEGER PRIMARY KEY,
    default_category_id INTEGER,
    name VARCHAR(40) NOT NULL
);

CREATE TABLE SecondPartyAliases (
    second_party_id INTEGER NOT NULL,
    alias VARCHAR(40) NOT NULL,
    PRIMARY KEY (second_party_id, alias)
);

CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES Accounts(id),
    category_id INTEGER REFERENCES Categories(id),
    other_party_id INTEGER REFERENCES SecondParties(id),
    amount FLOAT NOT NULL,
    description VARCHAR(100),
    time DATETIME NOT NULL DEFAULT (DATETIME('now'))
);

CREATE TRIGGER CreateDefaultSecondPartyAlias
AFTER INSERT ON SecondParties
FOR EACH ROW
BEGIN
    INSERT INTO SecondPartyAliases (second_party_id, alias)
    VALUES (NEW.id, NEW.name);
END;

CREATE TRIGGER UpdateAcccountBalance
BEFORE INSERT ON Transactions
FOR EACH ROW
BEGIN
    UPDATE Accounts
    SET Balance = Accounts.balance + NEW.amount
    WHERE id = NEW.account_id;
END;

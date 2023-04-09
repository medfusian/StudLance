CREATE TABLE Участки (
  ID_участка SERIAL PRIMARY KEY,
  Линия_номер_участка TEXT NOT NULL,
  Площадь NUMERIC(10,2) NOT NULL,
  Стоимость_постройки NUMERIC(10,2) NOT NULL,
  Взносы_в_фонд_садоводства NUMERIC(10,2) NOT NULL,
  ID_владельца INT NOT NULL REFERENCES Владельцы(ID_владельца)
);

CREATE TABLE Владельцы (
  ID_владельца SERIAL PRIMARY KEY,
  Имя TEXT NOT NULL,
  Фамилия TEXT NOT NULL
);

CREATE TABLE Постройки (
  ID_постройки SERIAL PRIMARY KEY,
  Название_постройки TEXT NOT NULL,
  Тип_постройки TEXT NOT NULL,
  Стоимость_постройки NUMERIC(10,2) NOT NULL,
  ID_участка INT NOT NULL REFERENCES Участки(ID_участка)
);

CREATE TABLE Владельцы (
  id INT(11) NOT NULL AUTO_INCREMENT,
  имя VARCHAR(50) NOT NULL,
  фамилия VARCHAR(50) NOT NULL,
  отчество VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Участки (
  id INT(11) NOT NULL AUTO_INCREMENT,
  номер_участка VARCHAR(20) NOT NULL,
  площадь FLOAT(4,2),
  взносы_в_фонд_садоводства FLOAT(8,2),
  PRIMARY KEY (id)
);

CREATE TABLE Постройки (
  id INT(11) NOT NULL AUTO_INCREMENT,
  id_участка INT,
  тип_постройки VARCHAR(50),
  стоимость_постройки FLOAT(8,2),
  PRIMARY KEY (id),
  FOREIGN KEY (id_участка) REFERENCES Участки(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Участки_Совместная_собственность (
  id INT(11) NOT NULL AUTO_INCREMENT,
  id_участка INT NOT NULL,
  id_владельца INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_участка) REFERENCES Участки(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_владельца) REFERENCES Владельцы(id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE Владельцы ADD COLUMN email VARCHAR(50) AFTER фамилия;

ALTER TABLE Участки DROP COLUMN взносы_в_фонд_садоводства;


################################################################


INSERT INTO владельцы (имя, фамилия, отчество)
VALUES
('Иван', 'Иванов', 'Иванович'),
('Петр', 'Петров', 'Петрович'),
('Анна', 'Сидорова', 'Александровна'),
('Мария', 'Петрова', 'Николаевна'),
('Сергей', 'Кузнецов', 'Андреевич'),
('Дмитрий', 'Смирнов', 'Сергеевич');

INSERT INTO Участки (номер_участка, площадь, взносы_в_фонд_садоводства)
VALUES
('Участок 1', 98, 300000),
('Участок 2', 80, 0),
('Участок 3', 90, 1200),
('Участок 4', 99, 150000),
('Участок 5', 90, 0),
('Участок 6', 70, 110000),
('Участок 7', 70, 0),
('Участок 8', 85, 1300),
('Участок 9', 95, 950),
('Участок 10', 99, 0);

INSERT INTO Постройки (id_участка, тип_постройки, стоимость_постройки)
VALUES
(1, 'Дом', 150000),
(1, 'Баня', 50000),
(1, 'Туалет', 500),
(2, 'Дачный домик', 50000),
(3, 'Дом', 100000),
(4, 'Дачный домик', 40000),
(4, 'Беседка', 10000),
(4, 'Туалет', 500),
(5, 'Дом', 90000),
(6, 'Баня', 30000),
(6, 'Беседка', 8000),
(7, 'Дачный домик', 60000),
(7, 'Туалет', 500),
(8, 'Беседка', 15000),
(9, 'Дом', 130000);

INSERT INTO Постройки (тип_постройки, стоимость_постройки)
VALUES
('Бассейн', 150000),
('Гараж', 100000),
('Сауна', 75000);

INSERT INTO участки_совместная_собственность (id_участка, id_владельца)
VALUES
(1, 1),
(1, 4),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(5, 2),
(6, 6),
(7, 2),
(8, 4),
(9, 5),
(10, 2);

# ALTER TABLE постройки AUTO_INCREMENT=1;

# INSERT INTO Владельцы (имя, фамилия, телефон) VALUES ('Иван', 'Иванов', '1234567890');
# UPDATE Участки SET стоимость_постройки = 15000 WHERE номер_участка = 'A-01';
# DELETE FROM Участки WHERE номер_участка = 'A-01';

# INSERT INTO Участки (номер_участка, площадь, взносы_в_фонд_садоводства)
# VALUES ('A1', 91.00, 500.00)
# ON DUPLICATE KEY UPDATE площадь = 80;

# MERGE INTO Владельцы AS target
# USING Владельцы_temp AS source
# ON target.фамилия = source.фамилия
# WHEN NOT MATCHED THEN
# INSERT (имя, фамилия, отчество)
# VALUES (source.имя, source.фамилия, source.отчество);

################################################################

# Номера участков владельцев с отчеством, заканчивающимся на «ич»
SELECT Участки.номер_участка, Владельцы.отчество
FROM Участки
JOIN Участки_Совместная_Собственность
ON Участки.id = Участки_Совместная_Собственность.id_участка
JOIN Владельцы
ON Участки_Совместная_Собственность.id_владельца = Владельцы.id
WHERE Владельцы.отчество LIKE '%ич';

# участки, на которых зарегистрировано более 1 типа постройки
SELECT у.номер_участка, COUNT(DISTINCT п.тип_постройки) AS количество_типов_построек
FROM Участки у
JOIN Постройки п ON у.id = п.id_участка
WHERE п.id_участка IS NOT NULL
GROUP BY у.номер_участка
HAVING COUNT(DISTINCT п.тип_постройки) > 1;

# тип построек, которые отсутствуют на участках
SELECT DISTINCT Постройки.тип_постройки
FROM Постройки
LEFT JOIN Участки
ON Постройки.id_участка = Участки.id
WHERE Участки.id IS NULL;

# Владелец (владельцы) участка максимальной площади
SELECT Владельцы.*
FROM Владельцы
JOIN Участки_Совместная_Собственность
ON Владельцы.id = Участки_Совместная_Собственность.id_владельца
JOIN Участки
ON Участки.id = Участки_Совместная_Собственность.id_участка
WHERE Участки.площадь = (SELECT MAX(площадь) FROM Участки);


# Владельцы участков с максимальным числом типов построек
SELECT DISTINCT Владельцы.*
FROM Владельцы
INNER JOIN Участки_Совместная_собственность ON Владельцы.id = Участки_Совместная_собственность.id_владельца
INNER JOIN (
  SELECT id_участка, COUNT(DISTINCT тип_постройки) AS cnt
  FROM Постройки
  GROUP BY id_участка
  HAVING cnt = (
    SELECT COUNT(DISTINCT тип_постройки)
    FROM Постройки
    GROUP BY id_участка
    ORDER BY COUNT(DISTINCT тип_постройки) DESC
    LIMIT 1
  )
) p ON Участки_Совместная_собственность.id_участка = p.id_участка;


# Владельцы, оплатившие все типы взносов
SELECT Владельцы.*
FROM Владельцы
WHERE NOT EXISTS (
  SELECT Участки.*
  FROM Участки
  WHERE NOT EXISTS (
    SELECT Участки_Совместная_собственность.*
    FROM Участки_Совместная_собственность
    WHERE Участки_Совместная_собственность.id_участка = Участки.id
      AND Участки_Совместная_собственность.id_владельца = Владельцы.id
    )
    AND (Участки.взносы_в_фонд_садоводства IS NULL OR Участки.взносы_в_фонд_садоводства <= 0)
  );

SELECT Владельцы.*
FROM Владельцы
INNER JOIN Участки_Совместная_собственность ON Владельцы.id = Участки_Совместная_собственность.id_владельца
INNER JOIN Участки ON Участки_Совместная_собственность.id_участка = Участки.id
GROUP BY Владельцы.id
HAVING COUNT(DISTINCT CASE WHEN Участки.взносы_в_фонд_садоводства <= 0 THEN Участки.id END) = COUNT(DISTINCT Участки.id);


# Участки, на которых нет бань, но есть туалеты
SELECT *
FROM Участки
WHERE id NOT IN (
  SELECT id_участка
  FROM Постройки
  WHERE тип_постройки = 'баня'
) AND id IN (
  SELECT id_участка
  FROM Постройки
  WHERE тип_постройки = 'туалет'
);

SELECT id_участка
FROM Постройки
WHERE тип_постройки = 'баня'
EXCEPT
SELECT id_участка
FROM Постройки
WHERE тип_постройки = 'туалет';


SELECT Участки.*
FROM Участки
LEFT JOIN Постройки ON Участки.id = Постройки.id_участка AND Постройки.тип_постройки = 'баня'
INNER JOIN Постройки AS p ON Участки.id = p.id_участка AND p.тип_постройки = 'туалет'
WHERE Постройки.id_участка IS NULL;

################################################################

# Вставка с пополнением справочников
DELIMITER //

CREATE PROCEDURE add_building(
  IN p_id_участка INT,
  IN p_тип_постройки VARCHAR(50),
  IN p_стоимость_постройки FLOAT(8,2)
)
BEGIN
  DECLARE v_id_участка INT;

  -- Получаем id_участка по его значению из таблицы Участки
  SELECT id INTO v_id_участка
  FROM Участки
  WHERE id = p_id_участка;

  -- Если id_участка не найден, то выбрасываем ошибку
  IF v_id_участка IS NULL THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Указанный id_участка не найден в таблице Участки';
  END IF;

  -- Вставляем новую запись в таблицу Постройки, используя v_id_участка в качестве внешнего ключа
  INSERT INTO Постройки (id_участка, тип_постройки, стоимость_постройки)
  VALUES (v_id_участка, p_тип_постройки, p_стоимость_постройки);

  -- Если вставка выполнена успешно, то выводим сообщение об этом
  SELECT CONCAT('Постройка "', p_тип_постройки, '" на участке ', v_id_участка, ' успешно добавлена') AS 'Результат';
END //

DELIMITER ;

CALL add_building(4, 'баня', 50000.00);

# Удаление с очисткой справочников
CREATE PROCEDURE delete_with_cleanup(IN parent_id INT)
BEGIN
  DECLARE child_count INT;
  SELECT COUNT(*) INTO child_count FROM Постройки WHERE id_участка = parent_id ;

  IF child_count > 0 THEN
    -- есть зависимые записи, удаляем их
    DELETE FROM Постройки WHERE id_участка = parent_id;
  END IF;

  -- удаляем родительскую запись
  DELETE FROM Участки WHERE id = parent_id;

  -- проверяем, остались ли еще дочерние записи для этого родителя
  SELECT COUNT(*) INTO child_count FROM Постройки WHERE id_участка = parent_id;

  IF child_count = 0 THEN
    -- больше нет дочерних записей, удаляем родительскую запись
    DELETE FROM Участки WHERE id = parent_id;
  END IF;
END;


CALL delete_with_cleanup(5);


# Каскадное удаление
DELIMITER $$
CREATE PROCEDURE delete_owner(IN owner_id INT)
BEGIN
    DECLARE num_rows INT;

    START TRANSACTION;

    -- Удаляем записи из таблицы Участки_Совместная_собственность, связанные с удаляемым владельцем
    DELETE FROM Участки_Совместная_собственность WHERE id_владельца = owner_id;

    -- Удаляем участки, связанные с удаляемым владельцем
    DELETE FROM Участки WHERE id IN (
        SELECT id_участка FROM Участки_Совместная_собственность WHERE id_владельца = owner_id
    );

    -- Удаляем постройки, связанные с удаляемым владельцем
    DELETE FROM Постройки WHERE id_участка IN (
        SELECT id_участка FROM Участки_Совместная_собственность WHERE id_владельца = owner_id
    );

    -- Удаляем запись в таблице Владельцы
    DELETE FROM Владельцы WHERE id = owner_id;

    -- Проверяем, остались ли у этого владельца участки
    SELECT COUNT(*) INTO num_rows FROM Участки_Совместная_собственность WHERE id_владельца = owner_id;

    -- Если удаляемый владелец стал бездетным после удаления связанных записей, то удаляем его запись из таблицы Владельцы
    IF num_rows = 0 THEN
        DELETE FROM Владельцы WHERE id = owner_id;
    END IF;

    COMMIT;
END$$
DELIMITER ;

CALL delete_owner(6);


# Вычисление и возврат значения агрегатной функции
CREATE PROCEDURE get_avg_area (OUT avg_area FLOAT)
BEGIN
  SELECT AVG(площадь) INTO avg_area FROM Участки;
END;

CALL get_avg_area(@avg);
SELECT @avg AS avg_area;

# Формирование статистики во временной таблице
DELIMITER //

CREATE PROCEDURE `формирование_статистики_участков`()
BEGIN
    DECLARE total_count INT;
    DECLARE min_area FLOAT(4,2);
    DECLARE max_area FLOAT(4,2);
    DECLARE avg_area FLOAT(4,2);
    DECLARE total_funds FLOAT(8,2);
    DECLARE min_funds FLOAT(8,2);
    DECLARE max_funds FLOAT(8,2);
    DECLARE avg_funds FLOAT(8,2);

    SELECT COUNT(*) INTO total_count FROM Участки;
    SELECT MIN(площадь) INTO min_area FROM Участки;
    SELECT MAX(площадь) INTO max_area FROM Участки;
    SELECT AVG(площадь) INTO avg_area FROM Участки;
    SELECT SUM(взносы_в_фонд_садоводства) INTO total_funds FROM Участки;
    SELECT MIN(взносы_в_фонд_садоводства) INTO min_funds FROM Участки;
    SELECT MAX(взносы_в_фонд_садоводства) INTO max_funds FROM Участки;
    SELECT AVG(взносы_в_фонд_садоводства) INTO avg_funds FROM Участки;

    DROP TABLE IF EXISTS Статистика_участков;
    CREATE TEMPORARY TABLE Статистика_участков (
        `Всего участков` INT,
        `Минимальная площадь` FLOAT(4,2),
        `Максимальная площадь` FLOAT(4,2),
        `Средняя площадь` FLOAT(4,2),
        `Общие взносы` FLOAT(8,2),
        `Минимальные взносы` FLOAT(8,2),
        `Максимальные взносы` FLOAT(8,2),
        `Средние взносы` FLOAT(8,2)
    );

    INSERT INTO Статистика_участков (
        `Всего участков`,
        `Минимальная площадь`,
        `Максимальная площадь`,
        `Средняя площадь`,
        `Общие взносы`,
        `Минимальные взносы`,
        `Максимальные взносы`,
        `Средние взносы`
    ) VALUES (
        total_count,
        min_area,
        max_area,
        avg_area,
        total_funds,
        min_funds,
        max_funds,
        avg_funds
    );

    SELECT * FROM Статистика_участков;

END//

DELIMITER ;

CALL формирование_статистики_участков();

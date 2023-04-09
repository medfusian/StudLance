import numpy as np

# Пример линейного (7,4)-кода с матрицами проверки и порождения
H = np.array([[1, 0, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 0, 1, 0],
              [0, 0, 0, 1, 1, 1, 1]])
G = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [1, 1, 0, 1],
              [1, 0, 1, 1],
              [0, 1, 1, 0]])


# Функция для вычисления синдрома
def compute_syndrome(received_codeword, H):
    syndrome = received_codeword @ H.T % 2
    return syndrome


# Функция для синдромного декодирования
def decode_syndrome(received_codeword, H):
    syndrome = compute_syndrome(received_codeword, H)
    error_column = np.argwhere(np.all(np.array_equal(H, syndrome), axis=0)).flatten()
    if len(error_column) == 0:
        return received_codeword
    else:
        corrected_codeword = np.copy(received_codeword)
        corrected_codeword[error_column[0]] = (received_codeword[error_column[0]] + 1) % 2
        return corrected_codeword


# Функция для декодирования перебором
def decode_brute_force(received_codeword):
    for i in range(2 ** len(received_codeword)):
        candidate_codeword = np.array([int(b) for b in bin(i)[2:].zfill(len(received_codeword))])
        syndrome = compute_syndrome(candidate_codeword, H)
        if np.array_equal(syndrome, np.zeros(H.shape[0], dtype=int)):
            return candidate_codeword
    return None


# Пример использования функций
info_word = np.array([0, 1, 1, 0])
codeword = (G @ info_word) % 2

print("Информационное слово:", info_word)
print("Кодовое слово:", codeword)

received_codeword = np.array([0, 1, 1, 1, 0, 1, 0])
print("Полученное кодовое слово:", received_codeword)

corrected_codeword = decode_syndrome(received_codeword, H)
print("Декодированное кодовое слово (синдромное декодирование):", corrected_codeword)

decoded_codeword = decode_brute_force(received_codeword)
print("Декодированное кодовое слово (декодирование перебором):", decoded_codeword)

print("----------------------------------------------------------------")
# Зададим параметры кода Хэмминга
r = 3
n = 2 ** r - 1
k = 2 ** r - r - 1

# Создадим матрицы проверки и порождения
H = np.zeros((r, n))
G = np.zeros((k, n))

# Заполним матрицы проверки и порождения
for i in range(r):
    H[i, 2 ** i - 1] = 1
for i in range(k):
    for j in range(n):
        if j + 1 == 2 ** i:
            G[i, j] = 1
        elif j + 1 > 2 ** i:
            G[i, j] = G[i, j - 2 ** i]

# Создадим матрицы проверки и порождения для расширенного кода Хэмминга
H_extended = np.array([[1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
                       [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
                       [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                       [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
                       [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                       [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                       [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
                       [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1]])
G_extended = np.array([[1, 0, 0, 0, 0, 1, 1, 1],
                       [0, 1, 0, 0, 1, 0, 1, 1],
                       [0, 0, 1, 0, 1, 1, 0, 1],
                       [0, 0, 0, 1, 1, 1, 1, 0],
                       [1, 1, 0, 1, 0, 0, 0, 1],
                       [1, 0, 1, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 1, 0, 0, 0],
                       [1, 1, 1, 0, 0, 1, 1, 0]])

# Сгенерируем случайное информационное слово и закодируем его кодом Хэмминга
info_word = np.random.randint(2, size=k)
codeword = (info_word @ G) % 2

# Выведем информационное слово и соответствующее ему кодовое слово
print("Информационное слово:", info_word)
print("Кодовое слово Хэмминга:", codeword)

# Для кода Хэмминга
received_codeword = np.array([0, 0, 1, 1, 1, 0, 0])
print("Полученное кодовое слово для кода Хэмминга:", received_codeword)

corrected_codeword = decode_syndrome(received_codeword, H)
print("Декодированное кодовое слово (синдромное декодирование):", corrected_codeword)

# Для расширенного кода Хэмминга
received_codeword = np.array([1, 0, 0, 1, 0, 1, 1])
print("Полученное кодовое слово для расширенного кода Хэмминга:", received_codeword)

corrected_codeword = decode_syndrome(received_codeword, H)
print("Декодированное кодовое слово (синдромное декодирование расширенного кода):", corrected_codeword)

print("Байбекова Мария Владиславовна КМА")
input("press enter for exit")

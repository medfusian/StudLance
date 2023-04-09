def syndrome(codeword, t, alpha):
    g = [alpha_to_int[alpha ** i] for i in range(2 * t)]
    s = [0] * (2 * t)  # увеличиваем длину списка s до 2 * t
    for i in range(len(codeword)):
        for j in range(2 * t):
            s[(i + j) % (2 * t)] ^= alpha_to_int[codeword[i]] * g[j]
    return s[:t]


def chien_search(locator, alpha):
    roots = []
    for i in range(len(locator)):
        if locator[i] == 0:
            roots.append(alpha ** i)
    return roots


def bch_decode(codeword, t, alpha):
    s = syndrome(codeword, t, alpha)
    if all(s[i] == 0 for i in range(t)):
        # no errors detected
        return codeword[:len(codeword) - 2 * t]
    # calculate error locator polynomial using Berlekamp-Massey algorithm
    locator = [1] + [0] * (t - 1)
    old_locator = [1] + [0] * (t - 1)
    discrepancy = [0] * (t + 1)
    discrepancy[0] = 1
    error = 0
    for i in range(t):
        delta = s[i] ^ sum(locator[j + 1] * s[i - j - 1] for j in range(i + 1))
        if delta != 0:
            temp_locator = locator[:]
            if 2 * i >= error:
                for j in range(t - error + i, i - 1, -1):
                    if j < len(old_locator) and old_locator[j] != 0:
                        locator[i - j + error] ^= delta * old_locator[j]
                error = 2 * i - error + 1
                old_locator = temp_locator[:]
            for j in range(t - error + i, i - 1, -1):
                if locator[j] != 0:
                    locator[i - j + error] ^= delta * locator[j]
    roots = chien_search(locator, alpha)
    # calculate error values using Forney algorithm
    error_values = [0] * len(codeword)
    for i in range(len(roots)):
        root = roots[i]
        error = s[0]
        for j in range(1, t):
            error ^= alpha_to_int[codeword[i]] * locator[j] * root ** (j)
        error_values[alpha_to_int[root]] = alpha_to_int[error]
    corrected_codeword = [(alpha_to_int[codeword[i]] ^ error_values[i]) for i in range(len(codeword))]
    # return original message
    return corrected_codeword


def error_locator(s, t, alpha):
    locator = [1]
    for i in range(1, t + 1):
        delta = s[i - 1]
        for j in range(1, i):
            if i - j - 1 >= 0 and j < len(locator):
                delta ^= locator[j] * s[i - j - 1]
        locator.append(0)
        for j in range(len(locator) - 1, 0, -1):
            if j - 1 >= 0:
                locator[j] = locator[j - 1]
        locator[0] = alpha ** alpha_to_int[delta] if delta != 0 else 0
    return locator


codeword = [1, 0, 1, 1, 0, 0, 1]
t = 1
alpha = 2


alpha_to_int = {alpha ** i: i for i in range(2 * t)}
alpha_to_int[0] = 0

# исходное сообщение
message = [1, 0, 1, 0, 1]

# кодирование сообщения
print("Кодовое слово:", message)

# добавление ошибки в кодовое слово
codeword[3] = (codeword[3] + 1) % 2
print("Кодовое слово с ошибкой:", codeword)

# декодирование кодового слова
decoded = bch_decode(codeword, t, alpha)
print("Декодированное сообщение:", message)


print("Байбекова Мария Владиславовна КМА")
input("press enter for exit")




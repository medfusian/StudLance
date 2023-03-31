def cyclic_codes(length):
    codes = []
    for i in range(2**length):
        code = bin(i)[2:].zfill(length) # перевод числа в двоичный вид
        is_cyclic = True
        for j in range(1, length):
            if code[j:] + code[:j] < code: # проверяем, что циклический сдвиг больше или равен исходному коду
                is_cyclic = False
                break
        if is_cyclic:
            codes.append(code)
    return codes

# выводим все циклические коды длин 3-9
for n in range(3, 10):
    print('Циклические коды длины ' + str(n))
    print(cyclic_codes(n))
    print('\n')

print('Столбовская Полина Сергеевна')
input('Нажмите Enter для выхода\n')

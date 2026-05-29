def sha48_encrypt(input_number: int) -> int:
    """Классический шифратор SHA48 (внутреннее ядро)."""
    MASK_48 = 0xFFFFFFFFFFFF
    h0 = 0x6A09E667F3BCC908 & MASK_48
    h1 = 0xBB67AE8584CAA73B & MASK_48

    state = (input_number ^ h0) + h1
    state &= MASK_48

    for round_idx in range(6):
        state = state ^ ((state << 5) | (state >> 43)) & MASK_48
        state = (state + 0x9E3779B97F4A) & MASK_48
        state = ((state >> 17) | (state << 31)) & MASK_48
        state ^= 0x517CC1B72722
        state = (state * (round_idx + 1)) & MASK_48

    return state

# Интерактивный цикл ввода
print("--- Программа-шифратор SHA48 из ДВОИЧНОГО кода ---")
print("Вводите ровно 48 бит (только 0 и 1). Для выхода напишите 'выход'.\n")

while True:
    user_input = input("Введите 48-битный исходный код (0 и 1): ").strip().replace(" ", "")

    if user_input.lower() in ['выход', 'exit', 'quit']:
        print("Программа завершена.")
        break

    # Проверка 1: Строго 48 символов
    if len(user_input) != 48:
        print(f"❌ Ошибка: Длина строки должна быть ровно 48 символов! Вы ввели {len(user_input)}.")
        print("-" * 60)
        continue

    # Проверка 2: Только нули и единицы
    if not all(char in '01' for char in user_input):
        print("❌ Ошибка: Вводить можно только нули '0' и единицы '1'!")
        print("-" * 60)
        continue

    # Конвертируем вашу 48-битную строку ввода в число
    binary_number = int(user_input, 2)

    # Расчет хэша
    hash_result = sha48_encrypt(binary_number)

    print(f"\nРезультат шифрования:")
    print(f"  • Входное число (десятичное): {binary_number}")
    print(f"  • Итоговый HEX-хэш SHA48:     0x{hash_result:012X}")

    # ДОБАВЛЕНО: Вывод получившегося хэша строго в двоичном виде (48 бит)
    print(f"  • ИТОГОВЫЙ ХЭШ В ДВОИЧНОЙ:    {hash_result:048b}")

    print("-" * 60)

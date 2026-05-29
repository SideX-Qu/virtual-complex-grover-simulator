try:
    import cupy as cp
except ImportError:
    import numpy as np
    !pip install cupy-cuda12x
    import cupy as cp
import numpy as np
import time
import sys
from IPython.display import clear_output

# Честный квантовый Оракул на чипе GPU (6 раундов SHA48)
# ИСПРАВЛЕНО: Синтаксис работы с complex128 приведен к стандартам C++/CUDA
sha48_complex_oracle_kernel = cp.ElementwiseKernel(
    'uint64 target_hash, uint64 base_x', 'uint64 out_indices, complex128 state_vec',
    '''
    unsigned long long y = i; // Индекс младших 24 бит (номер потока CUDA)
    unsigned long long state = (base_x | y);

    // Математика 6 раундов нашего SHA48 внутри видеокарты
    unsigned long long MASK_48 = 0xFFFFFFFFFFFFULL;
    unsigned long long h0 = 0x6A09E667F3BCC908ULL & MASK_48;
    unsigned long long h1 = 0xBB67AE8584CAA73BULL & MASK_48;

    state = (state ^ h0) + h1;
    state &= MASK_48;

    for(int r = 0; r < 6; r++) {
        state = state ^ ((state << 5) | (state >> 43)) & MASK_48;
        state = (state + 0x9E3779B97F4AULL) & MASK_48;
        state = ((state >> 17) | (state << 31)) & MASK_48;
        state ^= 0x517CC1B72722ULL;
        state = (state * (r + 1)) & MASK_48;
    }

    // НАСТОЯЩАЯ КВАНТОВАЯ ИНВЕРСИЯ ФАЗЫ:
    // ИСПРАВЛЕНО: Инвертируем весь комплексный объект целиком через оператор умножения
    if (state == target_hash) {
        state_vec = state_vec * -1.0;
        out_indices = 1; // Сигнал диспетчеру, что цель в этом секторе
    } else {
        out_indices = 0;
    }
    ''',
    'sha48_complex_oracle_kernel'
)

def run_complex_grover_gpu(target_hash: int, node_id: int):
    N_sub = 24
    num_states = 1 << N_sub # 16,777,216 квантовых состояний

    # 1. Честная квантовая инициализация суперпозиции комплексных амплитуд
    start_amplitude = 1.0 / np.sqrt(num_states)

    # Создаем массив complex128 в VRAM видеокарты (требует ровно 268 МБ)
    state_vector = cp.full(num_states, start_amplitude + 0j, dtype=cp.complex128)
    out_flags = cp.zeros(num_states, dtype=cp.uint64)

    base_x = int(node_id << 24)

    # --- КВАНТОВЫЙ ЭКСПРЕСС-ТЕСТ СРЕДНИХ КОМПЛЕКСНЫХ АМПЛИТУД ---
    EXPRESS_STEPS = 8  # Делаем всего 8 шагов вместо 3217!
    for step in range(EXPRESS_STEPS):
        # Вызов комплексного Оракула на CUDA
        sha48_complex_oracle_kernel(target_hash, base_x, out_flags, state_vector)

        # Комплексный диффузор: отражение волнового вектора относительно среднего значения
        mean_amp = cp.mean(state_vector)
        state_vector = 2.0 * mean_amp - state_vector

    # Квантовый фильтр аномалий: вычисляем действительную часть средней комплексной амплитуды
    current_mean_real = float(cp.mean(state_vector.real).get())

    # Если геометрия комплексного вектора осталась идеально плоской - узел пустой
    if abs(current_mean_real - start_amplitude) < 1e-15:
        return None  # Мгновенно сбрасываем сектор

    # --- ПОЛНАЯ ДОКРУТКА ЦЕЛИ ПРИ ОБНАРУЖЕНИИ АНОМАЛИИ ФАЗЫ ---
    print(f"\n🎯 [КОМПЛЕКСНЫЙ РАДАР]: Обнаружен сдвиг фазы на Узле №0x{node_id:06X}! Докрутка волнового вектора...")

    total_iterations = int(np.floor((np.pi / 4) * np.sqrt(num_states)))
    remaining_steps = total_iterations - EXPRESS_STEPS

    for step in range(remaining_steps):
        sha48_complex_oracle_kernel(target_hash, base_x, out_flags, state_vector)
        mean_amp = cp.mean(state_vector)
        state_vector = 2.0 * mean_amp - state_vector

    # Финальное квантовое измерение: вероятность равна квадрату модуля комплексной амплитуды
    probabilities = cp.absolute(state_vector) ** 2
    found_y = int(cp.argmax(probabilities).get())
    return base_x | found_y

# --- Интерфейс управления комплексной сетью ---
print("--- НАСТОЯЩИЙ КОМПЛЕКСНЫЙ КВАНТОВЫЙ CUDA-ВЗЛОМЩИК SHA48 ---")
user_bin_input = input("Введите 48-битный двоичный хэш: ").strip().replace(" ", "")

if len(user_bin_input) != 48 or not all(char in '01' for char in user_bin_input):
    print("❌ Ошибка: Введите строго 48 бит (только 0 и 1)!")
else:
    target_hash = int(user_bin_input, 2)
    start_time = time.time()
    solution = None

    # Сканируем 16777216 макро-узлов
    for node_id in range(16777216):

        if node_id % 50 == 0:
            clear_output(wait=True)
            current_time = time.time()
            elapsed = current_time - start_time
            variants_checked = node_id * 16777216
            virtual_speed = (variants_checked / elapsed) / 1_000_000 if elapsed > 0 else 0

            print("=======================================================")
            print("🔮 СИМУЛЯЦИЯ КОМПЛЕКСНОГО ВОЛНОВОГО ВЕКТОРА (COMPLEX128)")
            print("=======================================================")
            print(f"  • Целевой хэш:        0x{target_hash:012X}")
            print(f"  • Выделено памяти:    268 Мегабайт (uint64 + complex128)")
            print(f"  • Проверено вариантов: {variants_checked:,}")
            print(f"  • Прошло времени:     {elapsed:.1f} сек.")
            print(f"  • Скорость квантовой сетки: {virtual_speed:.2f} млн вар/сек.")
            print("=======================================================")
            sys.stdout.flush()

        # Запуск честной комплексной симуляции
        result = run_complex_grover_gpu(target_hash, node_id)
        if result is not None:
            solution = result
            break

    end_time = time.time()

    if solution is not None:
        print(f"\n📢 [КВАНТОВЫЙ КОЛЛАПС]: Комплексная волна успешно схлопнулась!")
        print(f"  • Истинный ответ (ДЕСЯТИЧНАЯ): {solution}")
        print(f"  • Истинный ответ (ДВОИЧНАЯ):   {solution:048b}")
        print(f"  • Время реального поиска: {end_time - start_time:.4f} сек.")
    else:
        print(f"\n❌ Сканирование завершено за {end_time - start_time:.1f} сек. Совпадений нет.")
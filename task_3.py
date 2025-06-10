import timeit
from pprint import pprint

# === Алгоритм Кнута-Морріса-Пратта ===


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

# === Алгоритм Рабіна-Карпа ===


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1, modulus)
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(
        main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1, modulus)
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash -
                                  ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            current_slice_hash = (current_slice_hash + modulus) % modulus
    return -1

# === Алгоритм Боєра-Мура ===


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


# === Зчитування текстів ===
with open('article1.txt', 'r', encoding='utf-8') as f1:
    text1 = f1.read()

with open('article2.txt', 'r', encoding='utf-8') as f2:
    text2 = f2.read()

# === Підрядки для тесту ===
existing_substring1 = text1[len(text1) // 2:len(text1) // 2 + 20]
existing_substring2 = text2[len(text2) // 3:len(text2) // 3 + 20]
fake_substring = 'qwertyuiopzxcvbnmlkj'

# === Алгоритми ===
algorithms = {
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
    "Boyer-Moore": boyer_moore_search
}

# === Функція бенчмарку ===


def benchmark(algorithm_name, func, text, pattern, number=5):
    def stmt(): return func(text, pattern)
    exec_time = timeit.timeit(stmt, number=number)
    return exec_time / number


# === Запуск тестів ===
results = {}

for i, (text, substr) in enumerate([(text1, existing_substring1), (text1, fake_substring),
                                    (text2, existing_substring2), (text2, fake_substring)]):
    case = f"text{i//2 + 1}_{'real' if i % 2 == 0 else 'fake'}"
    results[case] = {}
    for name, func in algorithms.items():
        time_taken = benchmark(name, func, text, substr)
        results[case][name] = time_taken

# === Вивід результатів ===
print("=== Benchmark Results (in seconds) ===")
pprint(results)
print("\n=== Найшвидші алгоритми ===")
for case, times in results.items():
    fastest = min(times, key=times.get)
    print(f"{case}: {fastest} ({times[fastest]:.6f} секунд)")

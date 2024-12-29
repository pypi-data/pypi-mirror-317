import random
import string

def nashCore(words, length):
    asci = []
    for char in words:
        asci.append(ord(char))

    for i in range(len(asci)):
        newVal = asci[i]
        newVal = 3 * newVal + 1
        asci[i] = newVal

    for i in range(len(asci)):
        newVal = asci[i]
        newVal = newVal / 2.45
        asci[i] = newVal

    def normalize_to_range(numbers, target_min, target_max):
        min_val = min(numbers)
        max_val = max(numbers)

        normalized_numbers = [
            int(((num - min_val) / (max_val - min_val)) * (target_max - target_min) + target_min)
            for num in numbers
        ]

        return normalized_numbers

    final_asci = normalize_to_range(asci, 33, 126)

    final_asci1 = []

    for i in range(length):
        new_element = (final_asci[i % len(final_asci)] + i) % 94 + 33
        final_asci1.append(new_element)

    array_sum = sum(final_asci1)
    digit_sum = sum(int(digit) for digit in str(array_sum))

    final_asci2 = []
    if digit_sum % 7 == 0:
        for i in range(length):
            new_element = (final_asci[i % len(final_asci)] * (i + 1)) % 94 + 33
            final_asci2.append(new_element)
    elif digit_sum % 7 == 1 or digit_sum % 7 == 3 or digit_sum % 7 == 5:
        for i in range(length):
            new_element = (final_asci[i % len(final_asci)] ** (i + 2)) % 94 + 33
            final_asci2.append(new_element)
    else:
        for i in range(length):
            new_element = (abs(final_asci[i % len(final_asci)] - i)) % 94 + 33
            final_asci2.append(new_element)

    hashedWord = []

    for i in range(len(final_asci2)):
        character = chr(final_asci2[i])
        hashedWord.append(character)

    finalHash = ''.join(hashedWord)

    return finalHash




def nashGuard(data, length, salt=None):

    if salt is None:
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))  
        return_hash_and_salt = True
    else:
        return_hash_and_salt = False

    combined = data + salt

    asci = [ord(char) for char in combined]

    salt_asci = [ord(char) for char in salt]
    for i in range(len(asci)):
        salt_value = salt_asci[i % len(salt_asci)]
        asci[i] = ((asci[i] * (i + 1) + salt_value) ** 1.3 + salt_value % 29) % 256

    for i in range(len(asci)):
        salt_value = salt_asci[i % len(salt_asci)]
        asci[i] = (asci[i] * 3.1415 / (salt_value + i + 1)) % 256  

    def normalize_to_range(numbers, target_min, target_max):
        min_val = min(numbers)
        max_val = max(numbers)
        return [
            int(((num - min_val) / (max_val - min_val)) * (target_max - target_min) + target_min)
            for num in numbers
        ]

    normalized = normalize_to_range(asci, 33, 126)

    final_asci = []
    for i in range(length):
        salt_value = salt_asci[i % len(salt_asci)]
        new_element = (normalized[i % len(normalized)] + salt_value * (i + 1)) % 94 + 33
        final_asci.append(new_element)

    hashed_word = ''.join(chr(val) for val in final_asci)

    if return_hash_and_salt:
        return hashed_word, salt

    return hashed_word





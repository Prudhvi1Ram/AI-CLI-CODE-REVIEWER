def find_duplicates(numbers):
    duplicates = []

    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] == numbers[j]:
                if numbers[i] not in duplicates:
                    duplicates.append(numbers[i])

    return duplicates

print(find_duplicates([1, 2, 3, 2, 4, 1]))
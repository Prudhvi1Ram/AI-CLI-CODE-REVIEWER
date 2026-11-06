def calculate_total(price, quantity):
    total = price * quantity
    return total + tax

print(calculate_total(100, 5))
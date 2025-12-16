import random

def generate_card():
    return {
        "card_number": str(random.randint(10**15, 10**16 - 1)),
        "cvv": str(random.randint(100, 999)),
        "expiry": "12/30",
        "balance":500000
    }

# Ramiro Flores Villarreal
# A01710879
# 23 / 05 / 2024
# Implementation of Computational methods Project: Card Game - Paradigm E4

import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Define the context-free grammar for the card game
grammar = CFG.fromstring("""
S -> ROUNDS
ROUNDS -> ROUND ROUNDS | ROUND
ROUND -> CARD BEATS
BEATS -> CARD
CARD -> RANK SUIT
RANK -> '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
SUIT -> 'C' | 'D' | 'H' | 'S'
""")

def can_beat(card1, card2, trump_suit):
    ranks = "23456789"
    rank1, suit1 = card1[0], card1[1]
    rank2, suit2 = card2[0], card2[1]
    if suit1 == suit2 and ranks.index(rank2) > ranks.index(rank1):
        return True
    if suit2 == trump_suit and suit1 != trump_suit:
        return True
    return False

def solve_card_game(t, test_cases):
    results = []
    for case in test_cases:
        n, trump_suit, cards = case
        pairs = form_pairs(cards, n, trump_suit)
        if pairs is None:
            results.append("IMPOSSIBLE")
        else:
            results.extend([f"{pair[0]} {pair[1]}" for pair in pairs])
    return results

def form_pairs(cards, n, trump_suit):
    if n == 0:
        return []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            card1 = cards[i]
            card2 = cards[j]
            if can_beat(card1, card2, trump_suit):
                remaining_cards = cards[:i] + cards[i+1:j] + cards[j+1:]
                result = form_pairs(remaining_cards, n - 1, trump_suit)
                if result is not None:
                    return [(card1, card2)] + result
            elif can_beat(card2, card1, trump_suit):
                remaining_cards = cards[:i] + cards[i+1:j] + cards[j+1:]
                result = form_pairs(remaining_cards, n - 1, trump_suit)
                if result is not None:
                    return [(card2, card1)] + result
    return None

def validate_and_parse_input(input_text, grammar):
    parser = nltk.ChartParser(grammar)
    tokens = word_tokenize(input_text)
    try:
        for tree in parser.parse(tokens):
            return True
    except ValueError:
        return False
    return False

# Input handling
def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    idx = 0
    t = int(data[idx])
    idx += 1
    test_cases = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        trump_suit = data[idx]
        idx += 1
        cards = data[idx:idx + 2*n]
        idx += 2*n

        # Validate using the defined grammar
        # input_text = ' '.join([str(n), trump_suit] + cards)
        # if not validate_and_parse_input(input_text, grammar):
        #    print("INVALID INPUT FORMAT")
        #    return

        test_cases.append((n, trump_suit, cards))

    results = solve_card_game(t, test_cases)
    for result in results:
        print(result)

# Example usage for testing
if __name__ == "__main__":
    import sys
    from io import StringIO

    test_input = """8
    3
    S
    3C 9S 4C 6D 3S 7S
    2
    C
    3S 5D 9S 6H
    1
    H
    6C 5D
    1
    S
    7S 3S
    1
    H
    9S 9H
    1
    S
    9S 9H
    1
    C
    9D 8H
    2
    C
    9C 9S 6H 8C
    """
    sys.stdin = StringIO(test_input)
    main()
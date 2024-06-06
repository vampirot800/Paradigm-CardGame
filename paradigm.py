# Ramiro Flores Villarreal
# A01710879
# 23 / 05 / 2024
# Implementation of Computational methods Project: Card Game - Paradigm E4

# Libraries
import nltk
from nltk import CFG
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from itertools import permutations

# Lambda functions for comparison
rank_order = "23456789"
rank_index = lambda rank: rank_order.index(rank)
can_beat = lambda card1, card2, trump: (
    (card1[1] == card2[1] and rank_index(card2[0]) > rank_index(card1[0])) or
    (card2[1] == trump and card1[1] != trump)
)

# Function to solve the game for multiple test cases
def solve_card_game(test_cases):
    def find_rounds(cards, trump):
        if not cards:
            return []
        for i, j in permutations(range(len(cards)), 2):
            card1, card2 = cards[i], cards[j]
            if can_beat(card1, card2, trump):
                remaining_cards = [card for k, card in enumerate(cards) if k not in {i, j}]
                result = find_rounds(remaining_cards, trump)
                if result is not None:
                    return [(card1, card2)] + result
        return None

    results = []
    for n, trump_suit, cards in test_cases:
        pairs = find_rounds(cards, trump_suit)
        if pairs is None:
            results.append("IMPOSSIBLE")
        else:
            results.extend([f"{pair[0]} {pair[1]}" for pair in pairs])
    return results

# Function to validate and parse the input text based on CFG
def validate_and_parse_input(input_text):
    cards = input_text.split()[2:]  
    tokens = [char for card in cards for char in card]

# CFG implementation
    grammar = CFG.fromstring("""
    S -> ROUNDS
    ROUNDS -> ROUND ROUNDS | ROUND
    ROUND -> CARD LOST_TO
    LOST_TO -> CARD
    CARD -> RANK SUIT
    RANK -> '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    SUIT -> 'C' | 'D' | 'H' | 'S'
    """)

    parser = nltk.RecursiveDescentParser(grammar)
    try:
        for tree in parser.parse(tokens):
            return True
    except ValueError as e:
        print("Parsing error:", e)
        return False
    return False

# Main function (Input handling)
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
        cards = data[idx:idx + 2 * n]
        idx += 2 * n

        input_text = ' '.join([str(n), trump_suit] + cards)
        if not validate_and_parse_input(input_text):
            print("INVALID INPUT FORMAT")
            return

        test_cases.append((n, trump_suit, cards))

    results = solve_card_game(test_cases)
    for result in results:
        print(result)

# Test case from code forces
if __name__ == "__main__":
    import sys
    from io import StringIO

# Test case input Format
#
# 1 - total number of game sets
# 1 - total number of pairs to play
# S - Trump suit (instant win)
# 3C 9S - Pair 

    test_input = """
    8
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

    # Test cases implemented additionally
    test_input2 = """
    2
    12 
    D
    6C 9D 7D 2D 4S 5D 8H 9D 2D 6S 4C 3C 2D 5D 3H 2H 5S 5S 6D 8S 3S 4D 2H 3D
    1
    H
    2H 2H
    """

    sys.stdin = StringIO(test_input2)
    main()

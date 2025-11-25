# PokerHandFunction.py
def findPokerHand(hand):
    ranks = []
    suits = []
    possibleRanks = []
 
    for card in hand:
        # Handling '10C', '10D', etc.
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
            
        # Assign numeric rank values
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11
        elif rank == "10": # Handle the '10' rank
            rank = 10
        
        try:
            ranks.append(int(rank))
        except ValueError:
            print(f"Error converting rank: {rank}")
            continue

        suits.append(suit)
 
    # Must have 5 cards for evaluation
    if len(ranks) < 5:
        return "Not Enough Cards"
        
    sortedRanks = sorted(ranks)
 
    # Check for Flush (all suits the same)
    is_flush = suits.count(suits[0]) == 5

    # Check for Straight
    # Handles 5, 4, 3, 2, A (wheel straight)
    is_regular_straight = all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks)))
    is_wheel_straight = sortedRanks == [2, 3, 4, 5, 14]
    is_straight = is_regular_straight or is_wheel_straight

    if is_wheel_straight:
        # A, 2, 3, 4, 5 - Treat the A as low for straight ranking
        current_straight_ranks = [1, 2, 3, 4, 5]
    else:
        current_straight_ranks = sortedRanks
        
    # Royal Flush, Straight Flush, and Flush
    if is_flush: 
        if is_straight and 14 in sortedRanks: # Royal Flush (A, K, Q, J, 10, all same suit)
            possibleRanks.append(10)
        elif is_straight: # Straight Flush
            possibleRanks.append(9)
        else:
            possibleRanks.append(6) # Flush
 
    # Straight
    if is_straight and not is_flush:
        possibleRanks.append(5)
 
    handUniqueVals = list(set(sortedRanks))
 
    # Count occurrences of each rank
    rank_counts = {}
    for rank in sortedRanks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
    counts = list(rank_counts.values())
    
    # Four of a Kind, Full House, Three of a Kind, Two Pair, Pair
    if 4 in counts:
        possibleRanks.append(8) # Four of a Kind
    elif 3 in counts and 2 in counts:
        possibleRanks.append(7) # Full House
    elif 3 in counts:
        possibleRanks.append(4) # Three of a Kind
    elif counts.count(2) == 2:
        possibleRanks.append(3) # Two Pair
    elif 2 in counts:
        possibleRanks.append(2) # Pair
 
    if not possibleRanks:
        possibleRanks.append(1) # High Card
        
    pokerHandRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                      5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}
    
    # Return the highest ranking hand
    output = pokerHandRanks[max(possibleRanks)]
    return output
import sys

def maxmin(board, depth):
    # Base case: if we've reached a leaf node, evaluate statically
    if depth == 0:
        estimate = improved_static_estimation_game(board)
        return board, 1, estimate  # One position evaluated

    # Recursive case: generate possible moves for White (MAX player)
    possible_moves = generate_moves_game(board)

    best_board = None
    best_estimate = float('-inf')
    total_evaluated = 0

    # For each move, call MIN node (Black's turn)
    for move in possible_moves:
        child_board, child_evaluated, child_estimate = minmax(move, depth - 1)

        total_evaluated += child_evaluated

        # White (MAX) wants to maximize the estimate
        if child_estimate > best_estimate:
            best_estimate = child_estimate
            best_board = move

    return best_board, total_evaluated, best_estimate

def minmax(board, depth):
    # Base case: if we've reached a leaf node, evaluate statically
    if depth == 0:
        estimate = improved_static_estimation_game(board)
        return board, 1, estimate  # One position evaluated

    # Recursive case: generate possible moves for Black (MIN player)
    possible_moves = generate_moves_game_black(board)

    best_board = None
    best_estimate = float('inf')
    total_evaluated = 0

    # For each move, call MAX node (White's turn)
    for move in possible_moves:
        child_board, child_evaluated, child_estimate = maxmin(move, depth - 1)

        total_evaluated += child_evaluated

        # Black (MIN) wants to minimize the estimate
        if child_estimate < best_estimate:
            best_estimate = child_estimate
            best_board = move

    return best_board, total_evaluated, best_estimate

def generate_moves_game(board):
    """
    Generate all possible board positions for White in the midgame/endgame.

    Rules from the handout:
    - If White has 3 pieces left, White can 'hop' (move any white piece to any empty point).
    - Otherwise, White can only move a piece to an adjacent empty neighbor.

    This function just chooses which rule applies and delegates.
    """

    # Count how many white pieces are currently on the board
    num_white_pieces = sum(1 for c in board if c == 'W')

    if num_white_pieces == 3:
        # Endgame: White is allowed to hop anywhere
        return generate_hopping(board)
    else:
        # Midgame: White can only move to adjacent empty spots
        return generate_move(board)

def generate_moves_game_black(board):
    """
    Generates all possible positions for Black in the midgame/endgame phase.
    Uses color-swapping logic described in the Morris Variant handout:
      1. Swap colors on the board (W <-> B).
      2. Generate all White moves on the swapped board using generate_moves_game().
      3. Swap colors back in each generated position.
    """
    # Step 1: Swap colors on the board
    swapped_board = []
    for c in board:
        if c == 'W':
            swapped_board.append('B')
        elif c == 'B':
            swapped_board.append('W')
        else:
            swapped_board.append('x')
    swapped_board = ''.join(swapped_board)

    # Step 2: Generate moves for "White" on the swapped board
    temp_positions = generate_moves_game(swapped_board)

    # Step 3: Swap colors back in all generated positions
    result_positions = []
    for pos in temp_positions:
        reverted = []
        for c in pos:
            if c == 'W':
                reverted.append('B')
            elif c == 'B':
                reverted.append('W')
            else:
                reverted.append('x')
        result_positions.append(''.join(reverted))

    return result_positions

def generate_move(board):
    """
    Generate all possible moves for White in the midgame phase (sliding pieces).
    White can move a piece to any adjacent empty position (given by neighbors()).
    """
    moves_list = []

    for i in range(len(board)):
        if board[i] == 'W':  # Find a white piece
            for j in neighbors(i):  # Check all neighbors
                if board[j] == 'x':  # Empty spot available
                    new_board = list(board)
                    new_board[i] = 'x'  # Move from i
                    new_board[j] = 'W'  # to j

                    if close_mill(j, new_board):
                        generate_remove(new_board, moves_list)
                    else:
                        moves_list.append(''.join(new_board))

    return moves_list

def generate_hopping(board):
    """
    Generate all possible board positions for White in the endgame (hopping phase).
    When White has exactly 3 pieces left, she can move a piece to any empty location.
    """
    moves_list = []

    for i in range(len(board)):
        if board[i] == 'W':  # find a white piece
            for j in range(len(board)):
                if board[j] == 'x':  # find any empty spot
                    new_board = list(board)
                    new_board[i] = 'x'
                    new_board[j] = 'W'

                    if close_mill(j, new_board):
                        generate_remove(new_board, moves_list)
                    else:
                        moves_list.append(''.join(new_board))

    return moves_list

def generate_remove(board, L):
    """
    Removes a black piece from the board if possible.
    Appends resulting board positions to L.
    If all black pieces are in mills, appends the board unchanged.
    """
    found = False

    for i in range(len(board)):
        if board[i] == 'B':
            if not close_mill(i, board):
                board_copy = list(board)
                board_copy[i] = 'x'
                L.append(''.join(board_copy))
                found = True

    # If no black pieces were removable (all in mills)
    if not found:
        L.append(''.join(board))


def close_mill(j, board):
    """
    Return True if placing a piece of color C at position j forms a mill.
    board is a list of length 21 with 'W', 'B', or 'x'.
    """
    C = board[j]
    if C == 'x':  # empty can't close a mill
        return False

    match j:
        case 0:
            return (board[2] == C and board[4] == C) or (board[6] == C and board[18] == C)
        case 1:
            return (board[3] == C and board[5] == C) or (board[11] == C and board[20] == C)
        case 2:
            return (board[0] == C and board[4] == C) or (board[7] == C and board[15] == C)
        case 3:
            return (board[1] == C and board[5] == C) or (board[10] == C and board[17] == C)
        case 4:
            return (board[0] == C and board[2] == C) or (board[8] == C and board[12] == C)
        case 5:
            return (board[1] == C and board[3] == C) or (board[9] == C and board[14] == C)
        case 6:
            return (board[0] == C and board[18] == C) or (board[7] == C and board[8] == C)
        case 7:
            return (board[6] == C and board[8] == C) or (board[2] == C and board[15] == C)
        case 8:
            return (board[6] == C and board[7] == C) or (board[4] == C and board[12] == C)
        case 9:
            return (board[5] == C and board[14] == C) or (board[10] == C and board[11] == C)
        case 10:
            return (board[3] == C and board[17] == C) or (board[9] == C and board[11] == C)
        case 11:
            return (board[9] == C and board[10] == C) or (board[1] == C and board[20] == C)
        case 12:
            # extra OR: (15,18)
            return ((board[4] == C and board[8] == C) or
                    (board[13] == C and board[14] == C) or
                    (board[15] == C and board[18] == C))
        case 13:
            return (board[12] == C and board[14] == C) or (board[16] == C and board[19] == C)
        case 14:
            # extra OR: (17,20)
            return ((board[5] == C and board[9] == C) or
                    (board[12] == C and board[13] == C) or
                    (board[17] == C and board[20] == C))
        case 15:
            # extra OR: (12,18)
            return ((board[2] == C and board[7] == C) or
                    (board[16] == C and board[17] == C) or
                    (board[12] == C and board[18] == C))
        case 16:
            return (board[15] == C and board[17] == C) or (board[13] == C and board[19] == C)
        case 17:
            # extra OR: (14,20)
            return ((board[15] == C and board[16] == C) or
                    (board[3] == C and board[10] == C) or
                    (board[14] == C and board[20] == C))
        case 18:
            # extra OR: (15,12)
            return ((board[0] == C and board[6] == C) or
                    (board[19] == C and board[20] == C) or
                    (board[15] == C and board[12] == C))
        case 19:
            return (board[16] == C and board[13] == C) or (board[18] == C and board[20] == C)
        case 20:
            # extra OR: (14,17)
            return ((board[1] == C and board[11] == C) or
                    (board[18] == C and board[19] == C) or
                    (board[14] == C and board[17] == C))
        case _:
            return False

def neighbors(position):
    """
    Given a board index (0–20), return a list of indices that are adjacent
    to that position according to the Variant Morris board graph.
    """
    mapping = {
        0:  [1, 2, 6],
        1:  [0, 3, 11],
        2:  [0, 3, 7, 4],
        3:  [1, 2, 5, 10],
        4:  [2, 5, 8],          # ✅ corrected neighbor list
        5:  [3, 4, 9],
        6:  [0, 7, 18],
        7:  [2, 6, 8, 15],
        8:  [4, 7, 12],
        9:  [5, 10, 14],
        10: [3, 9, 11, 17],
        11: [1, 10, 20],
        12: [8, 13, 15],
        13: [12, 14, 16],
        14: [9, 13, 17],
        15: [7, 12, 16, 18],
        16: [13, 15, 17, 19],
        17: [10, 14, 16, 20],
        18: [6, 15, 19],
        19: [16, 18, 20],
        20: [11, 17, 19],
    }

    return mapping[position]



def improved_static_estimation_game(board):
    """
    Improved static estimation function for the midgame/endgame phase.
    Incorporates material balance, mobility, mill counts, and potential mills.
    """
    num_white = board.count('W')
    num_black = board.count('B')

    # Generate moves for both sides
    white_moves = len(generate_moves_game(board))
    black_moves = len(generate_moves_game_black(board))

    # --- Terminal conditions ---
    if num_black <= 2:
        return 10000  # White wins
    elif num_white <= 2:
        return -10000  # Black wins
    elif black_moves == 0:
        return 10000  # Black is trapped (no legal moves)

    # --- Strategic feature calculations ---
    white_potentials = count_potential_mills(board, 'W')
    black_potentials = count_potential_mills(board, 'B')
    white_mills = count_mills(board, 'W')
    black_mills = count_mills(board, 'B')

    # Combine weighted factors into a single score
    score = (
        1000 * (num_white - num_black) +          # Material balance
        200  * (white_potentials - black_potentials) +  # Future mill potential
        100  * (white_mills - black_mills) +      # Existing mills
        5    * (white_moves - black_moves)        # Mobility advantage
    )

    return score


def count_potential_mills(board, color):
    """
    Counts the number of two-in-a-row configurations (potential mills)
    where the third position is empty.
    """
    count = 0
    mill_patterns = [
        (0, 2, 4), (6, 7, 8), (18, 19, 20),
        (1, 3, 5), (9, 10, 11),
        (2, 7, 15), (4, 8, 12),
        (3, 10, 17), (5, 9, 14),
        (12, 13, 14), (15, 16, 17),
        (13, 16, 19),
        (0, 6, 18), (1, 11, 20)
    ]

    for a, b, c in mill_patterns:
        trio = [board[a], board[b], board[c]]
        if trio.count(color) == 2 and trio.count('x') == 1:
            count += 1

    return count


def count_mills(board, color):
    """
    Counts the number of complete mills (three in a row)
    currently on the board for the given color.
    """
    mill_patterns = [
        (0, 2, 4), (6, 7, 8), (18, 19, 20),
        (1, 3, 5), (9, 10, 11),
        (2, 7, 15), (4, 8, 12),
        (3, 10, 17), (5, 9, 14),
        (12, 13, 14), (15, 16, 17),
        (13, 16, 19),
        (0, 6, 18), (1, 11, 20)
    ]

    count = 0
    for mill in mill_patterns:
        if all(board[i] == color for i in mill):
            count += 1

    return count



def main():
    # Ensure correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python3 MiniMaxOpening.py <input_file> <output_file> <depth>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        depth = int(sys.argv[3])
    except ValueError:
        print("Depth must be an integer.")
        sys.exit(1)

    # Read the input board position
    with open(input_file, "r") as f:
        board = f.readline().strip()

    # Simple validation
    if len(board) != 21:
        print("Error: Board position must be exactly 21 characters long.")
        sys.exit(1)

    # Call minimax for the opening phase (White’s turn)
    best_board, nodes_evaluated, estimate = maxmin(board, depth)

    # Write result to output file
    with open(output_file, "w") as f:
        f.write(best_board)

    # Print output as per project format
    print(f"Board Position: {best_board}")
    print(f"Positions evaluated by static estimation: {nodes_evaluated}.")
    print(f"MINIMAX estimate: {estimate}.")

if __name__ == "__main__":
    main()

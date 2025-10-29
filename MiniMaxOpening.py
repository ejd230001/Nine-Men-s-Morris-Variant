import sys

def maxmin(board, depth):
    # Base case: if we've reached a leaf node, evaluate statically
    if depth == 0:
        estimate = static_estimation_opening(board)
        return board, 1, estimate  # One position evaluated

    # Recursive case: generate possible moves for White (MAX player)
    possible_moves = generate_moves_opening(board)

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
        estimate = static_estimation_opening(board)
        return board, 1, estimate  # One position evaluated

    # Recursive case: generate possible moves for Black (MIN player)
    possible_moves = generate_moves_opening_black(board)

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

def generate_moves_opening(board):
    """
    Wrapper function defined in the Morris Variant handout.
    Returns all possible opening moves for White.
    """
    return generate_add(board)

def generate_moves_opening_black(board):
    """
    Wrapper function defined in the Morris Variant handout.
    Returns all possible opening moves for Black.
    """
    return generate_add_black(board)


def generate_add(board):
    L = []

    for i in range(len(board)):
        if board[i] == 'x':  # empty location
            board_copy = list(board)  # create mutable copy
            board_copy[i] = 'W'

            if close_mill(i, board_copy):
                generate_remove(board_copy, L)
            else:
                L.append(''.join(board_copy))

    return L


def generate_add_black(board):
    """
    Generates all possible positions for Black in the opening phase.
    Uses color-swapping logic described in the Morris-Variant handout:
      1. Swap colors on the board (W <-> B).
      2. Generate all White moves on the swapped board using generate_add().
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
    temp_positions = generate_add(swapped_board)

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


def static_estimation_opening(board):
    """
    Static estimation for the opening phase.
    Returns (numWhitePieces - numBlackPieces) as defined in the handout.
    """
    num_white = board.count('W')
    num_black = board.count('B')
    return num_white - num_black


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

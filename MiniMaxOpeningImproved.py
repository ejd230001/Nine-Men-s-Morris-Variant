import sys

def maxmin(board, depth):
    """
    White’s turn (MAX). Applies Minimax recursion for the opening phase,
    using the improved static estimation function.
    """
    if depth == 0:
        estimate = improved_static_estimation_opening(board)
        return board, 1, estimate  # One position evaluated

    possible_moves = generate_moves_opening(board)

    best_board = None
    best_estimate = float('-inf')
    total_evaluated = 0

    for move in possible_moves:
        child_board, child_evaluated, child_estimate = minmax(move, depth - 1)
        total_evaluated += child_evaluated

        if child_estimate > best_estimate:
            best_estimate = child_estimate
            best_board = move

    return best_board, total_evaluated, best_estimate


def minmax(board, depth):
    """
    Black’s turn (MIN). Mirrors White’s Minimax behavior, minimizing the estimate.
    """
    if depth == 0:
        estimate = improved_static_estimation_opening(board)
        return board, 1, estimate

    possible_moves = generate_moves_opening_black(board)

    best_board = None
    best_estimate = float('inf')
    total_evaluated = 0

    for move in possible_moves:
        child_board, child_evaluated, child_estimate = maxmin(move, depth - 1)
        total_evaluated += child_evaluated

        if child_estimate < best_estimate:
            best_estimate = child_estimate
            best_board = move

    return best_board, total_evaluated, best_estimate


# ---------- Move Generation ----------

def generate_moves_opening(board):
    """Returns all possible opening moves for White."""
    return generate_add(board)


def generate_moves_opening_black(board):
    """Generates all possible opening moves for Black using color swapping."""
    return generate_add_black(board)


def generate_add(board):
    """Generates all positions by placing a White piece on any empty spot."""
    L = []
    for i in range(len(board)):
        if board[i] == 'x':
            board_copy = list(board)
            board_copy[i] = 'W'

            if close_mill(i, board_copy):
                generate_remove(board_copy, L)
            else:
                L.append(''.join(board_copy))
    return L


def generate_add_black(board):
    """Generates all possible positions for Black by swapping colors."""
    swapped_board = []
    for c in board:
        if c == 'W':
            swapped_board.append('B')
        elif c == 'B':
            swapped_board.append('W')
        else:
            swapped_board.append('x')
    swapped_board = ''.join(swapped_board)

    temp_positions = generate_add(swapped_board)

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
    """Removes a Black piece if possible; otherwise keeps board unchanged."""
    found = False
    for i in range(len(board)):
        if board[i] == 'B' and not close_mill(i, board):
            board_copy = list(board)
            board_copy[i] = 'x'
            L.append(''.join(board_copy))
            found = True
    if not found:
        L.append(''.join(board))


# ---------- Mill Checking ----------

def close_mill(j, board):
    """Checks if placing a piece at index j forms a mill."""
    C = board[j]
    if C == 'x':
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
            return ((board[4] == C and board[8] == C)
                    or (board[13] == C and board[14] == C)
                    or (board[15] == C and board[18] == C))
        case 13:
            return (board[12] == C and board[14] == C) or (board[16] == C and board[19] == C)
        case 14:
            return ((board[5] == C and board[9] == C)
                    or (board[12] == C and board[13] == C)
                    or (board[17] == C and board[20] == C))
        case 15:
            return ((board[2] == C and board[7] == C)
                    or (board[16] == C and board[17] == C)
                    or (board[12] == C and board[18] == C))
        case 16:
            return (board[15] == C and board[17] == C) or (board[13] == C and board[19] == C)
        case 17:
            return ((board[15] == C and board[16] == C)
                    or (board[3] == C and board[10] == C)
                    or (board[14] == C and board[20] == C))
        case 18:
            return ((board[0] == C and board[6] == C)
                    or (board[19] == C and board[20] == C)
                    or (board[15] == C and board[12] == C))
        case 19:
            return (board[16] == C and board[13] == C) or (board[18] == C and board[20] == C)
        case 20:
            return ((board[1] == C and board[11] == C)
                    or (board[18] == C and board[19] == C)
                    or (board[14] == C and board[17] == C))
        case _:
            return False


# ---------- Improved Static Estimation ----------

def improved_static_estimation_opening(board):
    """
    Improved evaluation function for the opening phase.
    Considers:
      - Piece difference
      - Potential mills (two-in-a-row + empty)
      - Completed mills
    """
    num_white = board.count('W')
    num_black = board.count('B')

    white_potentials = count_potential_mills(board, 'W')
    black_potentials = count_potential_mills(board, 'B')
    white_mills = count_mills(board, 'W')
    black_mills = count_mills(board, 'B')

    score = (
        1000 * (num_white - num_black)
        + 200 * (white_potentials - black_potentials)
        + 100 * (white_mills - black_mills)
    )

    return score


def count_potential_mills(board, color):
    """Counts the number of two-in-a-row patterns with one empty."""
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
    """Counts the number of completed mills on the board."""
    mill_patterns = [
        (0, 2, 4), (6, 7, 8), (18, 19, 20),
        (1, 3, 5), (9, 10, 11),
        (2, 7, 15), (4, 8, 12),
        (3, 10, 17), (5, 9, 14),
        (12, 13, 14), (15, 16, 17),
        (13, 16, 19),
        (0, 6, 18), (1, 11, 20)
    ]
    return sum(all(board[i] == color for i in mill) for mill in mill_patterns)


# ---------- Main ----------

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 MiniMaxOpeningImproved.py <input_file> <output_file> <depth>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        depth = int(sys.argv[3])
    except ValueError:
        print("Depth must be an integer.")
        sys.exit(1)

    with open(input_file, "r") as f:
        board = f.readline().strip()

    if len(board) != 21:
        print("Error: Board position must be exactly 21 characters long.")
        sys.exit(1)

    best_board, nodes_evaluated, estimate = maxmin(board, depth)

    with open(output_file, "w") as f:
        f.write(best_board)

    print(f"Board Position: {best_board}")
    print(f"Positions evaluated by static estimation: {nodes_evaluated}.")
    print(f"MINIMAX estimate: {estimate}.")


if __name__ == "__main__":
    main()

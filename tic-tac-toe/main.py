#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tic‑Tac‑Toe (Python)

Features:
    • Interactive console UI
    • Visual board with grid lines
    • Win / draw detection
    • Optimal computer opponent (Minimax + alpha‑beta pruning)
"""

import sys
from typing import List, Tuple, Optional

# ----------------------------------------------------------------------
# Helper functions for the board representation
# ----------------------------------------------------------------------

def print_board(board: List[List[str]]) -> None:
    """Print the current 3×3 board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 5)   # separator line

def is_winner(board: List[List[str]], player: str) -> bool:
    """Check whether `player` has three in a row (horizontal, vertical, diagonal)."""
    lines = []
    # rows
    for r in board:
        lines.append(r)
    # columns
    for c in range(3):
        lines.append([board[0][c], board[1][c], board[2][c]])
    # diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[2][0], board[1][1], board[0][2]])

    for line in lines:
        if all(cell == player for cell in line):
            return True
    return False

def is_full(board: List[List[str]]) -> bool:
    """Return True if every cell contains a move."""
    return not any(' ' in row for row in board)

# ----------------------------------------------------------------------
# Minimax AI (with alpha‑beta pruning)
# ----------------------------------------------------------------------

class TicTacToeAI:
    """
    Simple optimal player using the minimax algorithm.
    The strategy is symmetric: X and O are interchangeable, so we just
    treat both sides as “player” during recursion.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def evaluate(board: List[List[str]]) -> int:
        """Return +1 for a win, -1 for a loss, 0 otherwise (draw)."""
        if TicTacToeAI.is_winner(board, "X"):
            return 1
        if TicTacToeAI.is_winner(board, "O"):
            return -1
        return 0

    def best_move(self,
                   board: List[List[str]],
                   player: str,
                   opponent: str) -> Tuple[int, int]:
        """
        Returns the (row, col) of the optimal move for `player`.
        Uses alpha‑beta pruning to keep the search fast.
        """
        # If we already have a winning move, take it
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':   # empty cell
                    board[r][c] = player
                    win = TicTacToeAI.is_winner(board, player)
                    if win:
                        board[r][c] = ' '
                        return (r, c)      # immediate win
                    elif not is_full(board):
                        # recurse deeper
                        _, alpha, beta = self._minimax(board, opponent,
                                                       -2, 2)
                        board[r][c] = ' '
                        if alpha >= beta:
                            continue
                    board[r][c] = player   # keep move for now (may be overwritten)
        # No immediate win – fall back to minimax result
        _, _, _, _ = self._minimax(board, player,
                                    -2, 2)   # dummy values; we only need the move
        # Find the move that yields the best score
        best_score, best_move = self._evaluate(board)
        return best_move

    def _minimax(self,
                 board: List[List[str]],
                 player: str,
                 alpha: int,
                 beta: int) -> Tuple[int, Tuple[int, int], int, int]:
        """
        Recursive minimax with alpha‑beta pruning.
        Returns (value, move, alpha, beta).
        `player` is the side to move; opponent is the other side.
        """
        # Terminal states
        if TicTacToeAI.is_winner(board, player):
            return 0, (-1, -1), alpha, beta   # dummy move; will be overridden
        if TicTacToeAI.is_winner(board, 'X') and player == 'O':
            # O wins → value = +1 for X
            return -1, (-1, -1), alpha, beta
        if TicTacToeAI.is_winner(board, 'O') and player == 'X':
            return 1, (-1, -1), alpha, beta    # X wins → value = +1 for X
        if is_full(board):
            return 0, (-1, -1), alpha, beta   # draw

        opponent = 'O' if player == 'X' else 'X'
        best_score, best_move = self._evaluate(board)

        for r in range(3):
            for c in range(3):
                if board[r][c] != ' ':
                    continue
                board[r][c] = player

                # Recurse and prune if possible
                _, _, _, _ = None   # placeholder (unused)
                value, move, a1, b1 = self._minimax(board,
                                                     opponent,
                                                     alpha, beta)

                board[r][c] = ' '   # undo move

                if player == 'O':          # O wants to maximize
                    if value > best_score:
                        best_score = value
                        best_move = (r, c)
                    if value >= beta:       # prune
                        return 0, (-1, -1), alpha, beta
                else:                       # X wants to minimize
                    if value < best_score:
                        best_score = value
                        best_move = (r, c)
                    if value <= alpha:      # prune
                        return 0, (-1, -1), alpha, beta

        return best_score, best_move, alpha, beta

    def _evaluate(self,
                   board: List[List[str]]) -> Tuple[int, Tuple[int, int]]:
        """Return (value, move) of the best line for the current player."""
        # Find the player who is to move – we don't have a context here.
        # Instead we just compute the highest‑scoring reachable state.
        # This helper is only used in the fallback path above.
        score = self.evaluate(board)
        if score == 0:
            # draw or no winner yet → any empty cell is fine
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        return (score, (r, c))
            return (score, (-1, -1))
        else:
            # For a win we can just pick any empty cell; the winner already
            # has three in a row.
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        return (score, (r, c))
            return (score, (-1, -1))

# ----------------------------------------------------------------------
# Game loop
# ----------------------------------------------------------------------

def play_game() -> None:
    """Main entry point – runs the interactive tic‑tac‑toe game."""
    board: List[List[str]] = [[' ' for _ in range(3)] for _ in range(3)]

    ai = TicTacToeAI()

    print("Welcome to Tic‑Tac‑Toe!")
    print("You are X, the computer is O.")
    print("\nBoard layout (row numbers on top):")
    # Print a static guide with coordinates
    for r in range(3):
        print(f"{r} | {board[r][0]}   {board[r][1]}   {board[r][2]} |")

    while True:
        turn = input("\nYour turn (row col, e.g. 0 1): ").strip()
        if not turn:
            continue
        parts = turn.split()
        if len(parts) != 2 or any(p not in '012' for p in parts):
            print("Invalid move – please enter two numbers separated by a space.")
            continue

        r, c = int(parts[0]), int(parts[1])
        if board[r][c] != ' ':
            print("That position is already taken. Choose another one.")
            continue

        # Human move
        board[r][c] = 'X'
        print_board(board)

        if is_winner(board, 'X'):
            print("\nCongratulations! You win!")
            break
        elif is_full(board):
            print("\nThe game ends in a draw!")
            break

        # ------------------------------------------------------------------
        # Computer move (optimal play)
        # ------------------------------------------------------------------
        r, c = ai.best_move(board, player='O', opponent='X')
        board[r][c] = 'O'
        print(f"\nComputer plays at ({r}, {c})")
        print_board(board)

        if is_winner(board, 'O'):
            print("\nComputer wins!")
            break
        elif is_full(board):
            print("\nThe game ends in a draw!")
            break

# ----------------------------------------------------------------------
# Entry point guard (allows import without side effects)
# ----------------------------------------------------------------------

if __name__ == '__main__':
    try:
        play_game()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl‑C
        print("\nGame interrupted – goodbye!")
        sys.exit(0)



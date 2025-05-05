
from typing import List, Optional

class TicTacToe:
    def __init__(self, starting_player: str = 'X'):
        # board: lista de 9 celdas (‘X’, ‘O’ o None)
        self.board: List[Optional[str]] = [None] * 9
        self.current_player: str = starting_player

    def legal_moves(self) -> List[int]:
        return [i for i, v in enumerate(self.board) if v is None]

    def make_move(self, pos: int) -> None:
        self.board[pos] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def undo_move(self, pos: int) -> None:
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.board[pos] = None

    def is_terminal(self) -> bool:
        # Comprueba victoria o empate
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for (i,j,k) in lines:
            if self.board[i] and self.board[i] == self.board[j] == self.board[k]:
                return True
        return all(cell is not None for cell in self.board)

    def utility(self) -> int:
        # +1 si gana X, -1 si O, 0 empate
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for (i,j,k) in lines:
            if self.board[i] and self.board[i] == self.board[j] == self.board[k]:
                return +1 if self.board[i] == 'X' else -1
        return 0

    def heuristic(self) -> float:
        # Heurística sencilla: (# líneas con 2X y ningún O) - (# líneas con 2O y ningún X)
        score = 0
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for (i,j,k) in lines:
            vals = [self.board[x] for x in (i,j,k)]
            if vals.count('X') == 2 and vals.count(None) == 1:
                score += 1
            if vals.count('O') == 2 and vals.count(None) == 1:
                score -= 1
        return float(score)

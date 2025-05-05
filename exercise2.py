# lab06_ej2.py
# Ejercicio 2 – Minimax con α–β Pruning 

import time
import random
from typing import List, Tuple, Optional
from tictactoe import TicTacToe


class MinimaxABPlayer:
    def __init__(self, k: int):
        self.k = k
        self.nodes_explored = 0

    def next_move(self, game: TicTacToe) -> int:
        _, move = self._alphabeta(game, depth=self.k,
                                  α=float('-inf'),
                                  β=float('inf'),
                                  maximizing=(game.current_player == 'X'))
        return move  # nunca debería ser None si hay movimientos legales

    def _alphabeta(self, game: TicTacToe, depth: int,
                   α: float, β: float, maximizing: bool
                  ) -> Tuple[float, Optional[int]]:
        self.nodes_explored += 1

        if game.is_terminal():
            return game.utility(), None
        if depth == 0:
            return game.heuristic(), None

        best_move: Optional[int] = None
        if maximizing:
            value = float('-inf')
            for m in game.legal_moves():
                game.make_move(m)
                score, _ = self._alphabeta(game, depth-1, α, β, False)
                game.undo_move(m)
                if score > value:
                    value, best_move = score, m
                α = max(α, value)
                if α >= β:
                    break  # poda β
            return value, best_move
        else:
            value = float('inf')
            for m in game.legal_moves():
                game.make_move(m)
                score, _ = self._alphabeta(game, depth-1, α, β, True)
                game.undo_move(m)
                if score < value:
                    value, best_move = score, m
                β = min(β, value)
                if β <= α:
                    break  # poda α
            return value, best_move

if __name__ == "__main__":
    random.seed(42)
    depths = [1, 2, 3, 4]
    N = 1000

    for k in depths:
        for start in ['X', 'O']:
            stats = {'wins':0, 'draws':0, 'losses':0, 'nodes':0}
            start_time = time.perf_counter()

            for i in range(N):
                game = TicTacToe(starting_player = start)
                player = MinimaxABPlayer(k)
                # Juega hasta terminal
                while not game.is_terminal():
                    m = player.next_move(game)
                    game.make_move(m)
                u = game.utility()
                stats['wins'   ] += (u == +1)
                stats['draws'  ] += (u ==  0)
                stats['losses' ] += (u == -1)
                stats['nodes'  ] += player.nodes_explored

            elapsed = time.perf_counter() - start_time
            print(f"k={k}  start={start}  |  X gana {(stats['wins']/N)*100:5.1f}%  "
                  f"empates {(stats['draws']/N)*100:5.1f}%  O gana {(stats['losses']/N)*100:5.1f}%  "
                  f"nodos_medios {stats['nodes']/N:8.1f}  tiempo {elapsed:.1f}s")

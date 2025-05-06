# Minimax puro de k niveles (sin poda α-β)

import time, random
from typing import List, Tuple, Optional
from tictactoe import TicTacToe

class MinimaxPlayer:
    """
    Jugador que decide su jugada usando Minimax puro (sin poda).
    """
    def __init__(self, k: int):
        self.k = k                      # profundidad máxima
        self.nodes_explored = 0         # para métricas

    # -------- interfaz pública --------
    def next_move(self, game: TicTacToe) -> int:
        """
        Devuelve la mejor jugada legal para el estado actual.
        """
        _, move = self._minimax(game,
                                depth=self.k,
                                maximizing=(game.current_player == 'X'))
        return move                    # no debe ser None

    # -------- implementación privada --------
    def _minimax(self, game: TicTacToe,
                 depth: int,
                 maximizing: bool
                 ) -> Tuple[float, Optional[int]]:
        """
        Retorna (score, move) para el jugador actual.
        """
        self.nodes_explored += 1

        # Caso base: nodo terminal o profundidad límite
        if game.is_terminal():
            return game.utility(), None
        if depth == 0:
            return game.heuristic(), None

        best_move: Optional[int] = None
        if maximizing:
            value = float('-inf')
            for m in game.legal_moves():
                game.make_move(m)
                score, _ = self._minimax(game, depth-1, False)
                game.undo_move(m)
                if score > value:
                    value, best_move = score, m
            return value, best_move
        else:
            value = float('inf')
            for m in game.legal_moves():
                game.make_move(m)
                score, _ = self._minimax(game, depth-1, True)
                game.undo_move(m)
                if score < value:
                    value, best_move = score, m
            return value, best_move

# ---------------------- rutina de medición ----------------------
if __name__ == "__main__":
    random.seed(42)
    depths: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    N = 1000            

    for k in depths:
        for start in ['X', 'O']:
            stats = {'wins': 0, 'draws': 0, 'losses': 0, 'nodes': 0}
            t0 = time.perf_counter()

            for _ in range(N):
                game = TicTacToe(starting_player=start)
                player = MinimaxPlayer(k)

                while not game.is_terminal():
                    move = player.next_move(game)
                    game.make_move(move)

                # registrar resultado y nodos
                u = game.utility()
                stats['wins']   += (u == +1)
                stats['draws']  += (u ==  0)
                stats['losses'] += (u == -1)
                stats['nodes']  += player.nodes_explored

            elapsed = time.perf_counter() - t0
            print(f"k={k}  start={start}  |  "
                  f"X gana {(stats['wins']/N)*100:5.1f}%  "
                  f"empates {(stats['draws']/N)*100:5.1f}%  "
                  f"O gana {(stats['losses']/N)*100:5.1f}%  "
                  f"nodos_medios {stats['nodes']/N:8.1f}  "
                  f"tiempo {elapsed:.1f}s")

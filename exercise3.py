import random
import matplotlib.pyplot as plt
from typing import List    
from tictactoe import TicTacToe  
def minimax(game, depth: int, maximizing: bool, k: int, explored_nodes: List[int]) -> float:
    if game.is_terminal() or depth == k:
        explored_nodes[0] += 1
        if game.is_terminal():
            return game.utility()
        return game.heuristic()

    if maximizing:
        max_eval = float('-inf')
        for move in game.legal_moves():
            game.make_move(move)
            eval = minimax(game, depth + 1, False, k, explored_nodes)
            game.undo_move(move)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.legal_moves():
            game.make_move(move)
            eval = minimax(game, depth + 1, True, k, explored_nodes)
            game.undo_move(move)
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(game, k: int) -> int:
    best_score = float('-inf')
    move_chosen = -1
    explored_nodes = [0]

    for move in game.legal_moves():
        game.make_move(move)
        score = minimax(game, 1, False, k, explored_nodes)
        game.undo_move(move)
        if score > best_score:
            best_score = score
            move_chosen = move

    return move_chosen, explored_nodes[0]

def simulate_multiple_depths(TicTacToeClass, ks: List[int], N: int = 200):
    resultados = {
        "k": [],
        "Victorias": [],
        "Derrotas": [],
        "Empates": [],
        "Promedio de nodos explorados": []
    }

    for k in ks:
        wins = 0
        losses = 0
        draws = 0
        total_nodes = 0

        for _ in range(N):
            game = TicTacToeClass(starting_player=random.choice(['X', 'O']))
            while not game.is_terminal():
                if game.current_player == 'X':
                    move, nodes = best_move(game, k)
                    total_nodes += nodes
                else:
                    move = random.choice(game.legal_moves())
                game.make_move(move)

            result = game.utility()
            if result == 1:
                wins += 1
            elif result == -1:
                losses += 1
            else:
                draws += 1

        resultados["k"].append(k)
        resultados["Victorias"].append(wins)
        resultados["Derrotas"].append(losses)
        resultados["Empates"].append(draws)
        resultados["Promedio de nodos explorados"].append(total_nodes / N)

    print("\nResultados promedio por profundidad:")
    for i in range(len(ks)):
        print(f"  k = {ks[i]}:")
        print(f"    - Victorias esperadas: {resultados['Victorias'][i]}/{N}")
        print(f"    - Empates esperados: {resultados['Empates'][i]}/{N}")
        print(f"    - Derrotas esperadas: {resultados['Derrotas'][i]}/{N}")
        print(f"    - Nodos promedio por subárbol: {resultados['Promedio de nodos explorados'][i]:.2f}\n")

    plt.figure(figsize=(10, 6))
    plt.plot(resultados["k"], resultados["Victorias"], label="Victorias", marker='o')
    plt.plot(resultados["k"], resultados["Empates"], label="Empates", marker='o')
    plt.plot(resultados["k"], resultados["Derrotas"], label="Derrotas", marker='o')
    plt.xlabel("Profundidad k")
    plt.ylabel("Número de partidas")
    plt.title(f"Resultados promedio en {N} partidas")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(resultados["k"], resultados["Promedio de nodos explorados"], label="Nodos Explorados", marker='s')
    plt.xlabel("Profundidad k")
    plt.ylabel("Promedio de nodos explorados por partida")
    plt.title(f"Complejidad computacional vs. Profundidad")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return resultados

if __name__ == "__main__":
    simulate_multiple_depths(TicTacToeClass=TicTacToe, ks=[1, 2, 3, 4, 5], N=20)

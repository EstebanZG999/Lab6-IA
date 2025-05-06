import math
import random
from typing import List, Optional, Tuple
from tictactoe import *

class MCTSNode:
    def __init__(self, state: TicTacToe, parent: Optional['MCTSNode'] = None, move: Optional[int] = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: List[MCTSNode] = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = state.legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.41):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        move = self.untried_moves.pop()
        new_state = TicTacToe(self.state.current_player)
        new_state.board = self.state.board[:]
        new_state.make_move(move)
        child_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def rollout(self):
        rollout_state = TicTacToe(self.state.current_player)
        rollout_state.board = self.state.board[:]
        while not rollout_state.is_terminal():
            move = random.choice(rollout_state.legal_moves())
            rollout_state.make_move(move)
        return rollout_state.utility()

    def backpropagate(self, result: int):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(-result)

def mcts(root: TicTacToe, iterations: int = 100) -> int:
    root_node = MCTSNode(root)
    for _ in range(iterations):
        node = root_node
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
        if not node.is_fully_expanded():
            node = node.expand()
        result = node.rollout()
        node.backpropagate(result)

    best_move = max(root_node.children, key=lambda c: c.visits).move
    return best_move


def run_single_simulation(iterations: int, games: int = 100) -> Tuple[int, int, int, float]:
    wins, draws, losses, total_nodes = 0, 0, 0, 0

    for _ in range(games):
        game = TicTacToe(starting_player='X')
        node_count = 0

        while not game.is_terminal():
            move = mcts(game, iterations=iterations)
            game.make_move(move)
            node_count += 1

        total_nodes += node_count
        result = game.utility()
        if result == 1:
            wins += 1
        elif result == 0:
            draws += 1
        else:
            losses += 1

    avg_nodes = total_nodes / games
    return wins, draws, losses, avg_nodes


def run_multiple_variants():
    variants = [25, 50, 100, 200, 400, 800]
    total_games = 1000

    print(f"{'Iteraciones':>12} | {'Victorias':>9} | {'Empates':>7} | {'Derrotas':>9} | {'Nodos/juego':>12}")
    print("-" * 60)

    for iters in variants:
        wins, draws, losses, avg_nodes = run_single_simulation(iters, games=total_games)
        print(f"{iters:>12} | {wins:>9} | {draws:>7} | {losses:>9} | {avg_nodes:>12.2f}")

if __name__ == "__main__":
    run_multiple_variants()

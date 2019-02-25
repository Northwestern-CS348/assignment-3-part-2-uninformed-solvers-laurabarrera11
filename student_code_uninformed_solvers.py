
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True

        current_move = False
        current_depth = self.currentState.depth + 1
        list_movables = self.gm.getMovables()

        while not current_move:
            count = self.currentState.nextChildToVisit
            if len(list_movables) <= count:
                if not self.currentState.parent:
                    return False
                else:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    list_movables = self.gm.getMovables()
                    self.currentState = self.currentState.parent
                    current_depth = self.currentState.depth + 1
                    continue

            next_move = list_movables[count]
            self.gm.makeMove(next_move)
            new_game_state = GameState(self.gm.getGameState(), current_depth, next_move)
            if new_game_state in self.visited:
                self.currentState.nextChildToVisit += 1
                self.gm.reverseMove(next_move)
            else:
                self.currentState.nextChildToVisit += 1
                new_game_state.parent = self.currentState
                self.currentState.children.append(new_game_state)
                self.currentState = new_game_state
                current_move = next_move

        if self.currentState.state != self.victoryCondition:
            self.visited[self.currentState] = True
            return False
        else:
            return True

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True

        current_depth = self.currentState.depth
        found_move = False
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            count = self.currentState.nextChildToVisit
            if len(self.currentState.children) > count:
                found_move = True
                break
        if not found_move:
            for all_visited in self.visited.keys():
                all_visited.nextChildToVisit = 0
            current_depth += 1
            if len(self.visited) == 1:
                all_possible_moves = self.gm.getMovables()
                for every_move in all_possible_moves:
                    self.gm.makeMove(every_move)
                    new_game_state = GameState(self.gm.getGameState(), current_depth, every_move)
                    new_game_state.parent = self.currentState
                    self.visited[new_game_state] = False
                    self.currentState.children.append(new_game_state)
                    self.gm.reverseMove(every_move)
        while current_depth != self.currentState.depth:
            count = self.currentState.nextChildToVisit
            self.currentState.nextChildToVisit += 1
            if len(self.currentState.children) > count:
                self.currentState = self.currentState.children[count]
                next_move = self.currentState.requiredMovable
                self.gm.makeMove(next_move)
            else:
                found_move = False
                while self.currentState.parent:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    if len(self.currentState.children) > self.currentState.nextChildToVisit:
                        found_move = True
                        break
                if not found_move:
                    return False

        if self.currentState.state != self.victoryCondition:
            self.visited[self.currentState] = True
            all_possible_moves = self.gm.getMovables()
            next_depth = current_depth + 1
            for every_move in all_possible_moves:
                self.gm.makeMove(every_move)
                new_game_state = GameState(self.gm.getGameState(), next_depth, every_move)
                if new_game_state not in self.visited:
                    self.visited[new_game_state] = False
                    new_game_state.parent = self.currentState
                    self.currentState.children.append(new_game_state)
                self.gm.reverseMove(every_move)
            return False
        else:
           return True
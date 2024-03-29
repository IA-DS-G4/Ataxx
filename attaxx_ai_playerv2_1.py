import random
import copy
import math

class AttaxxAIPlayer:
    def __init__(self, game, player_number):
        self.game = game
        self.player_number = player_number

    def rand_choose(self):
        x=random.randint(0,self.game.board_size-1)
        y=random.randint(0,self.game.board_size-1)
        return x,y

    def get_blank_cells(self,game_in_use):
        blank_cells = []
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if game_in_use.board[row][col] == ' ':
                    blank_cells.append((row, col))
        return blank_cells
    
    def get_possible_moves_for_blank_cell(self, row, col,game_in_use):
        possible_moves = []
        exist_dist_1=False
        #exist_dist_2=False        
        for i in range(-2, 3):
            for j in range(-2, 3):
                new_row, new_col = row + i, col + j

                if 0 <= new_row < self.game.board_size and 0 <= new_col < self.game.board_size and game_in_use.players[1-self.player_number]==game_in_use.board[new_row][new_col]:
                    distance = max(abs(i), abs(j))
                    if (distance == 1 and exist_dist_1==False):
                        possible_moves.append((new_row, new_col))
                        exist_dist_1=True
                    if(distance==2):
                    #if (distance == 2 and exist_dist_2==False):
                        #exist_dist_2=True
                        possible_moves.append((new_row, new_col))
        return possible_moves

    def get_possible_moves_for_all_blank_cells(self,game_in_use):
        all_possible_moves = []
        blank_cells = self.get_blank_cells(game_in_use)

        for cell in blank_cells:
            possible_moves = self.get_possible_moves_for_blank_cell(cell[0],cell[1],game_in_use)
            for starts in possible_moves:
                all_possible_moves.append((starts[0], starts[1], cell[0], cell[1]))
            
        #print(all_possible_moves)
        return all_possible_moves

    #simulate a game played from a state until the end

    def select_best_move(self, game, possible_moves):
        best_score = -float('inf')
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            # Assumindo que make_move_ai modifica o estado do jogo e retorna o vencedor
            game_copy.make_move_ai(*move)  
            score = self.evaluate_game_state(game_copy)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move if best_move else random.choice(possible_moves)


    def evaluate_game_state(self, game):
        score = 0
        for row in range(game.board_size):
            for col in range(game.board_size):
                if game.board[row][col] == game.players[self.player_number]:
                    score += 1  # Pontos por ter uma peça
                    if self.is_vulnerable(game, row, col):
                        score -= 0.5
        return score  

    def is_vulnerable(self, game, row, col):
        opponent = 'X' if self.player_number == 1 else 'O'
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue  # Ignora a própria posição
                new_row, new_col = row + i, col + j
                if 0 <= new_row < game.board_size and 0 <= new_col < game.board_size:
                    if game.board[new_row][new_col] == opponent:
                        return True  # Peça vulnerável se um oponente estiver por perto
        return False  # Não vulnerável se nenhum oponente estiver por perto
    
    def simulate_random(self, game_in_use):
        game_copy = copy.deepcopy(game_in_use)
        winner = None

        while game_copy.is_move_possible():
            possible_moves = self.get_possible_moves_for_all_blank_cells(game_copy)
            if not possible_moves:
                break

            best_move = self.select_best_move(game_copy, possible_moves)
            start_row, start_col, end_row, end_col = best_move
            winner = game_copy.make_move_ai(start_row, start_col, end_row, end_col)

        return winner if winner is not None else -1
        

    def mcts(self, iterations=2000):
        root_node = Node(self.game, None, None)

        for _ in range(iterations):
            node = root_node
            game_copy = copy.deepcopy(self.game)

            # Selection
            while node.untried_moves == [] and node.children != []:
                node = node.best_child()

            # Expansion
            if node.untried_moves != []:
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)
                game_copy.make_move_ai(*move)
                node = node.add_child(game_copy, move)

            # Simulation
            winner=self.simulate_random(game_copy)
            if self.player_number== winner:
                result_sim=1
            elif winner==-1:
                result_sim=0
            else:
                result_sim=-1
            print(result_sim)


            # Backpropagation
            while node is not None:
                node.update(result_sim)
                node = node.parent

        # Choose the best move based on visits
        best_move = root_node.best_child(c=1.0).move
        print(best_move)
        return best_move
        # Return information about the simulated move and the resulting board
        
class Node:
    def __init__(self, game, move, parent):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.get_untried_moves(game)

    def get_untried_moves(self, game):
        return AttaxxAIPlayer(game, 0).get_possible_moves_for_all_blank_cells(game)

    def add_child(self, game, move):
        child = Node(game, move, self)
        self.children.append(child)
        return child

    def best_child(self, c=2.0):
        return max(self.children, key=lambda child: child.wins / child.visits + c * math.sqrt(2 * math.log(self.visits) / child.visits))

    def update(self, result):
        self.visits = self.visits+1
        self.wins = self.wins+result
        
   

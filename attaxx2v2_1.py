import tkinter as tk
import random
from attaxx_ai_playerv2_1 import AttaxxAIPlayer  

class AttaxxGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = ['X', 'O']
        self.current_player = 0  # Primeiro jogador//Red
        self.start_position = None  # Armazenar a posição de início para o movimento
        self.winner=-1
        # Posições iniciais
        self.board[0][0] = 'O' #Red
        self.board[self.board_size-1][self.board_size-1] = 'O' 
        self.board[0][self.board_size-1] = 'X' #Blue
        self.board[self.board_size-1][0] = 'X'
        
    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def reset(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = ['X', 'O']
        self.current_player = 0  # Primeiro jogador
        self.winner = -1
        # Redefine as posições iniciais
        self.board[0][0] = 'O' #Red
        self.board[self.board_size-1][self.board_size-1] = 'O' 
        self.board[0][self.board_size-1] = 'X' #Blue
        self.board[self.board_size-1][0] = 'X'

        #Verificar se existem movimentos possíveis
    def is_move_possible(self):
        for line in range(self.board_size):
            for column in range(self.board_size):
                if self.players[self.current_player] == self.board[line][column]:
                    if self.get_valid_moves_from_position((line, column)):
                        return True
        return False

    def get_valid_moves_from_position(self, position):
        line, column = position
        valid_moves = []
        for i in range(-2, 3):  # Varia de -2 a 2
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue  # Pula a própria posição
                new_position = (line + i, column + j)
                if self.is_valid_move(position, new_position):
                    valid_moves.append(new_position)
        return valid_moves

    def is_valid_move(self, start, end):
        # Verificar se o movimento está dentro dos limites do tabuleiro
        if not (0 <= start[0] < self.board_size and 0 <= start[1] < self.board_size and
                0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size):
            return False

        # Verificar se o destino está vazio
        if self.board[end[0]][end[1]] != ' ':
            return False

        # Verificar se o movimento é um salto válido (uma ou duas células de distância)
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        return (1 <= row_diff <= 2 and col_diff == 0) or (1 <= col_diff <= 2 and row_diff == 0) or \
               (1 <= row_diff <= 2 and 1 <= col_diff <= 2)

    def make_move(self, end):
        finished=False
        if self.start_position and self.is_valid_move(self.start_position, end):
            # Se o destino é adjacente ao ponto de partida, cria uma nova peça
            if abs(self.start_position[0] - end[0]) <= 1 and abs(self.start_position[1] - end[1]) <= 1:
                self.board[end[0]][end[1]] = self.players[self.current_player]
                
            else:
                # Move a peça no ponto de partida para o destino
                self.board[end[0]][end[1]] = self.board[self.start_position[0]][self.start_position[1]]
                self.board[self.start_position[0]][self.start_position[1]] = ' '
                

            # Conquiste as células adjacentes
            self.conquer_adjacent(end)

            self.start_position = None  # Limpar a posição de início
            self.switch_player()
            #print(self.players[self.current_player])
            #print(self.is_move_possible());
            if(self.is_move_possible()==False):
                finished=True
                self.winner=self.check_winner()
            if finished:
                return self.winner
            return -1

    def make_move_ai(self,xi,yi,xf,yf):
        finished=False
        # Se o destino é adjacente ao ponto de partida, cria uma nova peça
        if abs(xi - xf) <= 1 and abs(yi - yf) <= 1:
            self.board[xf][yf] = self.players[self.current_player]
                
        else:
            # Move a peça no ponto de partida para o destino
            self.board[xf][yf] = self.board[xi][yi]
            self.board[xi][yi] = ' '
                
        # Conquiste as células adjacentes
        self.conquer_adjacent((xf,yf))
        self.print_board()

        self.switch_player()
        if(self.is_move_possible()==False):
            finished=True
            winner=self.check_winner()
        if finished:
            return winner
        return -1
        
    def switch_player(self):
        self.current_player = 1 - self.current_player  # Alternar entre jogadores

        #count pieces of the current player. The other has the rest of the board.
    def count_pieces(self):
        total=0;
        for line in range(self.board_size):
            for column in range(self.board_size):
                if(self.players[self.current_player]==self.board[line][column]):
                    total+=1;
        return total;

    def check_winner(self):
        if self.winner!=-1:
            return self.winner
        #print('ver vencedor')
        #self.print_board()
        if(self.count_pieces()<self.board_size*self.board_size/2):
            print('Ganhou o jogador ', 1-self.current_player, ' com ' , self.board_size*self.board_size-self.count_pieces(), ' peças.');
            return 1-self.current_player
        elif(self.count_pieces()==self.board_size*self.board_size/2):
            print('Houve empate')
            return 0
        else:
            print('Ganhou o jogador ', self.current_player, ' com ', self.count_pieces(), ' peças.');
        return self.current_player
    
    def check_winner(self):
        player_pieces = [cell for row in self.board for cell in row if cell == self.players[self.current_player]]
        opponent_pieces = [cell for row in self.board for cell in row if cell == self.players[1 - self.current_player]]

        if not player_pieces:
            return self.players[1 - self.current_player]
        elif not opponent_pieces:
            return self.players[self.current_player]

        if not self.available_moves():
            if len(player_pieces) > len(opponent_pieces):
                return self.players[self.current_player]
            elif len(player_pieces) < len(opponent_pieces):
                return self.players[1 - self.current_player]
            else:
                return 'Tie'
        return None
    
    def available_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == self.players[self.current_player]:
                    moves.extend(self.get_moves_for_piece(row, col))
        return moves
    
    def get_moves_for_piece(self, row, col):
        moves = []
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                new_row, new_col = row + dr, col + dc
                if self.is_valid_move((row, col), (new_row, new_col)):
                    moves.append(((row, col), (new_row, new_col)))
        return moves

    def conquer_adjacent(self, position):
        row, col = position

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                new_row, new_col = row + dr, col + dc
                new_position = (new_row, new_col)

                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size \
                        and self.board[new_row][new_col] == self.players[1 - self.current_player]:
                    # Conquista a célula adjacente
                    self.board[new_row][new_col] = self.players[self.current_player]

class AttaxxGUIPVP:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.SQUARE_SIZE = 50  # Tamanho da célula

        # Configurar o tabuleiro
        self.canvas = tk.Canvas(master, width=self.game.board_size * self.SQUARE_SIZE,
                                height=self.game.board_size * self.SQUARE_SIZE)
        self.canvas.pack()

        # Desenhar o tabuleiro inicial
        self.draw_board()

        # Reconhecer as jogadas através do clique do rato
        self.canvas.bind("<Button-1>", self.handle_click)

        self.add_control_buttons()

        # Adicionar rótulo de turno
        self.turn_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.turn_label.pack()

        self.update_turn_label()

    def update_turn_label(self):
        # Atualiza o rótulo com o jogador atual
        if self.game.current_player == 0:  # Supondo que 0 seja o jogador X (vermelho)
            self.turn_label.config(text="Player X turn", fg="red")
        else:
            self.turn_label.config(text="Player O turn", fg="blue")

    def add_control_buttons(self):
        tk.Button(self.master, text="Restart", command=self.restart_game).pack()
        tk.Button(self.master, text="Menu", command=self.back_to_menu).pack()
        tk.Button(self.master, text="Exit", command=self.exit_game).pack()

    def restart_game(self):
        # Reiniciar o jogo
        self.game.reset()  # Implementar a função reset em AttaxxGame
        self.draw_board()  # Atualizar o tabuleiro

    def back_to_menu(self):
        # Voltar para o menu de configuração
        self.master.destroy()
        main()  # Chamar a função main para mostrar a tela de configuração

    def exit_game(self):
        # Sair do jogo
        self.master.destroy()

    def draw_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                player = self.game.board[row][col]
                color = "white" if player == ' ' else "red" if player == 'X' else "blue"  # Definir cores
                self.canvas.create_rectangle(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                             (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                                             fill=color, outline="black")

    def handle_click(self, event):
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        piece = self.game.board[row][col]

        if piece != ' ' and piece == self.game.players[self.game.current_player]:
            self.game.start_position = (row, col)
        else:
            end_position = (row, col)
            self.game.make_move(end_position)

        self.draw_board()
        self.update_turn_label()
        self.update_game_state()

    def update_game_state(self):
        winner = self.game.check_winner()
        if winner == 'X':
            self.turn_label.config(text="Player X wins", fg="red")
        elif winner == 'O':
            self.turn_label.config(text="Player O wins", fg="blue")
        elif winner == 'Tie':
            self.turn_label.config(text="It's a tie", fg="green")

class AttaxxGUIPVC:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.SQUARE_SIZE = 50  # Tamanho da célula

        # Configurar o tabuleiro
        self.canvas = tk.Canvas(master, width=self.game.board_size * self.SQUARE_SIZE,
                                height=self.game.board_size * self.SQUARE_SIZE)
        self.canvas.pack()

        # Desenhar o tabuleiro inicial
        self.draw_board()

        # Reconhecer as jogadas através do clique do rato
        self.canvas.bind("<Button-1>", self.handle_click)

        self.add_control_buttons()

        # Adicionar rótulo de turno
        self.turn_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.turn_label.pack()

        self.update_turn_label()

    def update_turn_label(self):
        # Atualiza o rótulo com o jogador atual
        if self.game.current_player == 0:  # Supondo que 0 seja o jogador X (vermelho)
            self.turn_label.config(text="Player X turn", fg="red")
        else:
            self.turn_label.config(text="Player O turn", fg="blue")    

    def add_control_buttons(self):
        tk.Button(self.master, text="Restart", command=self.restart_game).pack()
        tk.Button(self.master, text="Menu", command=self.back_to_menu).pack()
        tk.Button(self.master, text="Exit", command=self.exit_game).pack()

    def restart_game(self):
        # Reiniciar o jogo
        self.game.reset()  # Implementar a função reset em AttaxxGame
        self.draw_board()  # Atualizar o tabuleiro

    def back_to_menu(self):
        # Voltar para o menu de configuração
        self.master.destroy()
        main()  # Chamar a função main para mostrar a tela de configuração

    def exit_game(self):
        # Sair do jogo
        self.master.destroy()

    def draw_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                player = self.game.board[row][col]
                color = "white" if player == ' ' else "red" if player == 'X' else "blue"  # Definir cores
                self.canvas.create_rectangle(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                             (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                                             fill=color, outline="black")

    def handle_click(self, event):
        if self.game.current_player == self.game.players.index('X'):
            col = event.x // self.SQUARE_SIZE
            row = event.y // self.SQUARE_SIZE
            piece = self.game.board[row][col]

            if piece != ' ' and piece == self.game.players[self.game.current_player]:
                self.game.start_position = (row, col)
            else:
                end_position = (row, col)
                self.game.make_move(end_position)

            self.draw_board()
            self.update_turn_label()

            if self.game.is_move_possible():
                self.handle_ai_move()

            self.update_turn_label()
            self.update_game_state()

    def handle_ai_move(self):
        # Example: Assume AI player is player 'O'
        if self.game.current_player == self.game.players.index('O'):

            ai_player = AttaxxAIPlayer(self.game, player_number=self.game.players.index('O'))
            #xi, yi = ai_player.rand_choose()
            #xf, yf = ai_player.rand_choose()
            xi, yi, xf, yf =ai_player.mcts()
            #while((self.game.board[xi][yi]!='O') or (self.game.is_valid_move((xi,yi),(xf,yf))==False)):
                #xi, yi = ai_player.rand_choose()
                #xf, yf = ai_player.rand_choose()
                
            print('melhor jogada', xi,yi,xf,yf)
            self.game.make_move_ai(xi,yi,xf,yf)
            self.draw_board()

    def update_game_state(self):
        winner = self.game.check_winner()
        if winner == 'X':
            self.turn_label.config(text="Player X wins", fg="red")
        elif winner == 'O':
            self.turn_label.config(text="Player O wins", fg="blue")
        elif winner == 'Tie':
            self.turn_label.config(text="It's a tie", fg="green")
           
class AttaxxGUICVC:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.SQUARE_SIZE = 50  # Tamanho da célula

        self.game_running = True

        # Configurar o tabuleiro
        self.canvas = tk.Canvas(master, width=self.game.board_size * self.SQUARE_SIZE,
                                height=self.game.board_size * self.SQUARE_SIZE)
        self.canvas.pack()

        self.add_control_buttons()

        # Desenhar o tabuleiro inicial
        self.draw_board()

        # Cria instâncias independentes da IA para cada jogador
        self.ai_player_0 = AttaxxAIPlayer(self.game, 0)  # IA para o jogador 'X'
        self.ai_player_1 = AttaxxAIPlayer(self.game, 1)  # IA para o jogador 'O'

        # Iniciar o jogo AI vs AI
        self.master.after(1000, self.play_ai_game)

        # Adicionar rótulo de turno
        self.turn_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.turn_label.pack()

        self.update_turn_label()

    def update_turn_label(self):
        # Atualiza o rótulo com o jogador atual
        if self.game.current_player == 0:
            self.turn_label.config(text="Player X turn", fg="red")
        else:
            self.turn_label.config(text="Player O turn", fg="blue")

    def add_control_buttons(self):
        tk.Button(self.master, text="Restart", command=self.restart_game).pack()
        tk.Button(self.master, text="Menu", command=self.back_to_menu).pack()
        tk.Button(self.master, text="Exit", command=self.exit_game).pack()

    def restart_game(self):
        self.game_running = False  # Parar o loop do jogo atual
        self.game.reset()
        self.draw_board()
        self.update_turn_label()
        self.game_running = True  # Indicar que um novo jogo deve começar
        self.master.after(1000, self.play_ai_game)

    def back_to_menu(self):
        self.game_running = False  # Parar o loop do jogo atual
        self.master.destroy()
        main()

    def exit_game(self):
        self.game_running = False  # Parar o loop do jogo atual
        self.master.destroy()

    def draw_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                player = self.game.board[row][col]
                color = "white" if player == ' ' else "red" if player == 'X' else "blue"
                self.canvas.create_rectangle(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                             (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                                             fill=color, outline="black")

    def play_ai_game(self):
        if not self.game_running or self.game.check_winner():
            self.update_game_state()
            return

        self.handle_ai_move()
        self.master.after(1000, self.play_ai_game)

    def handle_ai_move(self):
        # Escolhe a IA baseada no jogador atual
        current_ai = self.ai_player_0 if self.game.current_player == 0 else self.ai_player_1
        move = current_ai.mcts()
        self.game.make_move_ai(*move)
        self.draw_board()
        self.update_turn_label()
        self.game.switch_player()  # Alterna para o outro jogador

    def update_game_state(self):
        winner = self.game.check_winner()
        if winner == 'X':
            self.turn_label.config(text="Player X wins", fg="red")
        elif winner == 'O':
            self.turn_label.config(text="Player O wins", fg="blue")
        elif winner == 'Tie':
            self.turn_label.config(text="It's a tie", fg="green")

def start_game(mode, board_size):
    root = tk.Tk()
    root.title("Attaxx Game")
    game = AttaxxGame(board_size)

    if mode == 'PVP':
        gui = AttaxxGUIPVP(root, game)
    elif mode == 'PVC':
        gui = AttaxxGUIPVC(root, game)
    elif mode == 'CVC':
        gui = AttaxxGUICVC(root, game)

    root.mainloop()

def main():
    setup_window = tk.Tk()
    setup_window.title("Setup")

    def start_selected_game():
        mode = game_mode_var.get()
        size = board_size_var.get()
        if size == 'Random':
            size = random.choice([4, 5, 6, 7])
        else:
            size = int(size)

        setup_window.destroy()
        start_game(mode, size)

    game_mode_var = tk.StringVar(value='PVP')
    board_size_var = tk.StringVar(value='4')

    tk.Radiobutton(setup_window, text="Human vs Human", variable=game_mode_var, value='PVP').pack()
    tk.Radiobutton(setup_window, text="Human vs AI", variable=game_mode_var, value='PVC').pack()
    tk.Radiobutton(setup_window, text="AI vs AI", variable=game_mode_var, value='CVC').pack()

    tk.Radiobutton(setup_window, text="4x4 Board", variable=board_size_var, value='4').pack()
    tk.Radiobutton(setup_window, text="7x7 Board", variable=board_size_var, value='7').pack()
    tk.Radiobutton(setup_window, text="Random Size", variable=board_size_var, value='Random').pack()

    tk.Button(setup_window, text="Start Game", command=start_selected_game).pack()

    setup_window.mainloop()

if __name__ == "__main__":
    main()
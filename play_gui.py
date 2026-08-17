import json
import tkinter as tk
from tkinter import ttk
import agent
import game


class Game2048GUI:
    """GUI para visualizar jogos de 2048 em tempo real."""
    
    # Cores para os tiles do 2048
    COLORS = {
        0: "#cdc1b4",
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e",
    }
    
    # Cores de texto (claro para tiles escuros, escuro para tiles claros)
    TEXT_COLORS = {
        0: "#776e65",
        2: "#776e65",
        4: "#776e65",
        8: "#f9f6f2",
        16: "#f9f6f2",
        32: "#f9f6f2",
        64: "#f9f6f2",
        128: "#f9f6f2",
        256: "#f9f6f2",
        512: "#f9f6f2",
        1024: "#f9f6f2",
        2048: "#f9f6f2",
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("2048 AI - Live Visualization")
        self.root.geometry("600x700")
        self.root.configure(bg="#faf8ef")
        
        self.genome = self.load_genome()
        self.games_total = 500
        self.win_target = 1024
        
        self.scores = []
        self.max_tiles = []
        self.wins = 0
        self.current_game = 0
        self.current_score = 0
        self.current_board = None
        self.game_over = False
        
        self.setup_ui()
        self.start_next_game()
    
    def load_genome(self):
        with open("models/best_genome.json", "r") as file:
            return json.load(file)
    
    def setup_ui(self):
        """Configura a interface da GUI."""
        
        # Título
        title_label = tk.Label(
            self.root,
            text="2048 AI - Live Visualization",
            font=("Arial", 24, "bold"),
            bg="#faf8ef",
            fg="#776e65"
        )
        title_label.pack(pady=10)
        
        # Frame de estatísticas
        stats_frame = tk.Frame(self.root, bg="#faf8ef")
        stats_frame.pack(pady=10)
        
        # Progresso dos jogos
        self.game_label = tk.Label(
            stats_frame,
            text="Game: 0/500",
            font=("Arial", 14),
            bg="#faf8ef",
            fg="#776e65"
        )
        self.game_label.grid(row=0, column=0, padx=20)
        
        # Score atual
        self.score_label = tk.Label(
            stats_frame,
            text="Score: 0",
            font=("Arial", 14),
            bg="#faf8ef",
            fg="#776e65"
        )
        self.score_label.grid(row=0, column=1, padx=20)
        
        # Estatísticas acumuladas
        self.avg_score_label = tk.Label(
            stats_frame,
            text="Avg Score: 0",
            font=("Arial", 12),
            bg="#faf8ef",
            fg="#776e65"
        )
        self.avg_score_label.grid(row=1, column=0, padx=20)
        
        self.best_score_label = tk.Label(
            stats_frame,
            text="Best Score: 0",
            font=("Arial", 12),
            bg="#faf8ef",
            fg="#776e65"
        )
        self.best_score_label.grid(row=1, column=1, padx=20)
        
        self.wins_label = tk.Label(
            stats_frame,
            text="Wins: 0/500 (0.0%)",
            font=("Arial", 12),
            bg="#faf8ef",
            fg="#776e65"
        )
        self.wins_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Frame do tabuleiro
        board_frame = tk.Frame(
            self.root,
            bg="#bbada0",
            padx=10,
            pady=10
        )
        board_frame.pack(pady=20)
        
        # Criar grid 4x4 para o tabuleiro
        self.tile_labels = []
        for i in range(4):
            row_labels = []
            for j in range(4):
                tile_label = tk.Label(
                    board_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=6,
                    height=3,
                    bg="#cdc1b4",
                    fg="#776e65"
                )
                tile_label.grid(row=i, column=j, padx=3, pady=3)
                row_labels.append(tile_label)
            self.tile_labels.append(row_labels)
        
        # Barra de progresso
        style = ttk.Style()
        style.configure("Horizontal.TProgressbar", background="#8f7a66", troughcolor="#faf8ef")
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Horizontal.TProgressbar"
        )
        self.progress.pack(pady=20)
        
        # Botão para pausar/continuar
        self.paused = False
        self.pause_button = tk.Button(
            self.root,
            text="Pause",
            font=("Arial", 12),
            command=self.toggle_pause,
            bg="#faf8ef",
            fg="#8f7a66",
            width=10,
            relief="flat"
        )
        self.pause_button.pack(pady=5)
    
    def toggle_pause(self):
        """Alterna entre pausado e rodando."""
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.root.after(100, self.game_step)
    
    def update_board_display(self):
        """Atualiza a visualização do tabuleiro."""
        if self.current_board is None:
            return
        
        for i in range(4):
            for j in range(4):
                value = self.current_board[i][j]
                label = self.tile_labels[i][j]
                
                # Definir cor baseada no valor
                bg_color = self.COLORS.get(value, "#3c3a32")
                text_color = self.TEXT_COLORS.get(value, "#f9f6f2")
                
                label.config(
                    text=str(value) if value != 0 else "",
                    bg=bg_color,
                    fg=text_color
                )
    
    def update_stats(self):
        """Atualiza as estatísticas na GUI."""
        self.game_label.config(text=f"Game: {self.current_game}/{self.games_total}")
        self.score_label.config(text=f"Score: {self.current_score}")
        
        if self.scores:
            avg_score = sum(self.scores) / len(self.scores)
            self.avg_score_label.config(text=f"Avg Score: {avg_score:.0f}")
            self.best_score_label.config(text=f"Best Score: {max(self.scores)}")
        
        win_rate = (self.wins / self.current_game * 100) if self.current_game > 0 else 0
        self.wins_label.config(
            text=f"Wins: {self.wins}/{self.current_game} ({win_rate:.1f}%)"
        )
        
        # Atualizar barra de progresso
        progress_value = (self.current_game / self.games_total) * 100
        self.progress["value"] = progress_value
    
    def start_next_game(self):
        """Inicia o próximo jogo."""
        if self.current_game >= self.games_total:
            self.show_final_results()
            return
        
        self.current_game += 1
        self.current_board = game.reset_game()
        self.current_score = 0
        self.game_over = False
        
        self.update_board_display()
        self.update_stats()
        
        # Iniciar o jogo
        self.root.after(100, self.game_step)
    
    def game_step(self):
        """Executa um passo do jogo."""
        if self.paused:
            return
        
        if self.game_over or self.current_game > self.games_total:
            return
        
        if game.is_game_over(self.current_board):
            self.end_current_game()
            return
        
        # Obter ação do agente
        action = agent.genetic_agent(self.current_board, self.genome)
        
        if action is None:
            self.end_current_game()
            return
        
        # Executar movimento
        self.current_board, reward, moved = game.move(
            self.current_board,
            action
        )
        
        if moved:
            self.current_score += reward
            self.current_board = game.add_new_tile(self.current_board)
        
        # Atualizar display
        self.update_board_display()
        self.update_stats()
        
        # Continuar jogo
        self.root.after(50, self.game_step)
    
    def end_current_game(self):
        """Finaliza o jogo atual e inicia o próximo."""
        self.game_over = True
        
        # Registrar estatísticas
        self.scores.append(self.current_score)
        max_tile = max(max(row) for row in self.current_board)
        self.max_tiles.append(max_tile)
        
        # Verificar vitória
        if max_tile >= self.win_target:
            self.wins += 1
        
        # Pequena pausa antes do próximo jogo
        self.root.after(500, self.start_next_game)
    
    def show_final_results(self):
        """Mostra os resultados finais."""
        self.progress["value"] = 100
        
        result_text = f"""
        ==============================
        FINAL RESULTS
        ==============================
        Games: {self.games_total}
        Average Score: {sum(self.scores) / len(self.scores):.0f}
        Best Score: {max(self.scores)}
        Best Tile: {max(self.max_tiles)}
        Wins (target {self.win_target}): {self.wins}/{self.games_total} ({self.wins/self.games_total*100:.1f}%)
        """
        
        result_label = tk.Label(
            self.root,
            text=result_text,
            font=("Arial", 12),
            bg="#faf8ef",
            fg="#776e65",
            justify="left"
        )
        result_label.pack(pady=20)
        
        self.pause_button.config(state="disabled")


def main():
    root = tk.Tk()
    app = Game2048GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for X, 2 for O
        self.game_over = False
        self.winner = None
        self.winning_combination = None  # Store winning cells

    def reset_game(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.winning_combination = None
        return self.get_board_image()

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != 0:
            return self.get_board_image()

        self.board[row][col] = self.current_player
        self.check_winner()
        
        if not self.game_over:
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
        
        return self.get_board_image()

    def check_winner(self):
        # Check rows
        for i in range(3):
            if all(self.board[i, :] == self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.winning_combination = [(i, j) for j in range(3)]
                return

        # Check columns
        for i in range(3):
            if all(self.board[:, i] == self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.winning_combination = [(j, i) for j in range(3)]
                return

        # Check main diagonal
        if all(np.diag(self.board) == self.current_player):
            self.game_over = True
            self.winner = self.current_player
            self.winning_combination = [(i, i) for i in range(3)]
            return

        # Check anti-diagonal
        if all(np.diag(np.fliplr(self.board)) == self.current_player):
            self.game_over = True
            self.winner = self.current_player
            self.winning_combination = [(i, 2-i) for i in range(3)]
            return

        # Check for draw
        if np.all(self.board != 0):
            self.game_over = True
            self.winner = 0  # Draw

    def get_board_image(self):
        # Create an image of the board
        cell_size = 100
        board_size = cell_size * 3
        img = Image.new("RGB", (board_size, board_size), color="white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        # Draw grid
        for i in range(1, 3):
            draw.line([(0, i*cell_size), (board_size, i*cell_size)], fill="black", width=3)
            draw.line([(i*cell_size, 0), (i*cell_size, board_size)], fill="black", width=3)

        # Draw X, O, and highlight winning cells
        for i in range(3):
            for j in range(3):
                x0, y0 = j*cell_size, i*cell_size
                x1, y1 = x0+cell_size, y0+cell_size
                cell = self.board[i][j]
                highlight = self.winning_combination and (i, j) in self.winning_combination
                if highlight:
                    draw.rectangle((x0, y0, x1, y1), fill=(144, 238, 144))  # light green
                if cell == 1:
                    bbox = draw.textbbox((0, 0), "X", font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text((x0 + (cell_size-w)//2, y0 + (cell_size-h)//2), "X", fill="blue", font=font)
                elif cell == 2:
                    bbox = draw.textbbox((0, 0), "O", font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text((x0 + (cell_size-w)//2, y0 + (cell_size-h)//2), "O", fill="red", font=font)

        return img

def create_game_interface():
    game = TicTacToe()
    
    with gr.Blocks(title="Tic Tac Toe") as interface:
        gr.Markdown("# Tic Tac Toe")
        gr.Markdown("Player 1: X (blue), Player 2: O (red)")
        
        board = gr.Image(
            value=game.get_board_image(),
            interactive=True,
            label="Click a cell to make a move",
            elem_id="board"
        )
        reset_btn = gr.Button("Reset Game")

        def on_cell_click(evt: gr.SelectData):
            # evt.index gives (x, y) in pixels, so convert to cell
            if evt is None or evt.index is None:
                return game.get_board_image()
            x, y = evt.index
            cell_size = 100
            col = x // cell_size
            row = y // cell_size
            if 0 <= row < 3 and 0 <= col < 3:
                return game.make_move(row, col)
            return game.get_board_image()

        def on_reset():
            return game.reset_game()

        board.select(on_cell_click, None, board)
        reset_btn.click(on_reset, None, board)
    
    return interface

if __name__ == "__main__":
    interface = create_game_interface()
    interface.launch() 
import pygame
import sys

# --- Configuration ---
DIM = 4  # Dimension size (4x4x4x4)
CELL_SIZE = 30  # Initial cell size
MARGIN = 10
GRID_SPACING = 20

# --- Colors ---
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (230, 50, 50)
BLUE = (50, 50, 230)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
WIN_BG = (220, 255, 220)

# --- Init ---
pygame.init()
clock = pygame.time.Clock()

def create_font(cell_size):
    return pygame.font.SysFont(None, max(14, cell_size))

def calc_window_size(cell_size):
    width = (cell_size * DIM + GRID_SPACING) * DIM + MARGIN
    height = (cell_size * DIM + GRID_SPACING) * DIM + MARGIN + 50
    return width, height

CELL_SIZE_CURRENT = CELL_SIZE
WIDTH, HEIGHT = calc_window_size(CELL_SIZE_CURRENT)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FourTic - 4D Tic-Tac-Toe")
font = create_font(CELL_SIZE_CURRENT)

game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
current_player = "X"
winner_line = []
winner_player = None

def reset_game():
    global game_board, current_player, winner_line, winner_player
    game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    current_player = "X"
    winner_line = []
    winner_player = None

def draw_board(cell_size):
    global font
    screen.fill(WIN_BG if winner_player else WHITE)
    font = create_font(cell_size)
    for w in range(DIM):
        for z in range(DIM):
            offset_x = MARGIN + w * (cell_size * DIM + GRID_SPACING)
            offset_y = MARGIN + z * (cell_size * DIM + GRID_SPACING)

            pygame.draw.rect(screen, GRAY, (offset_x - 2, offset_y - 2, cell_size * DIM + 4, cell_size * DIM + 4), 2)

            for y in range(DIM):
                for x in range(DIM):
                    rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)

                    # Highlight winning cells strongly
                    if (w, z, y, x) in winner_line:
                        pygame.draw.rect(screen, GREEN, rect)
                    else:
                        pygame.draw.rect(screen, WHITE if not winner_player else WIN_BG, rect)

                    pygame.draw.rect(screen, BLACK, rect, 1)

                    mark = game_board[w][z][y][x]
                    if mark:
                        text_color = RED if mark == "X" else BLUE
                        text = font.render(mark, True, text_color)
                        screen.blit(text, text.get_rect(center=rect.center))

    # Winner banner
    if winner_player:
        msg_font = pygame.font.SysFont(None, max(24, cell_size + 6))
        msg = msg_font.render(f"Spieler {winner_player} hat gewonnen! Drücke R für neues Spiel", True, BLACK)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 25)))

    pygame.display.flip()

def check_winner():
    global winner_line
    directions = [
        (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
        (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0),
        (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 1, 0), (1, 1, 0, 1),
        (1, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1)
    ]

    for w in range(DIM):
        for z in range(DIM):
            for y in range(DIM):
                for x in range(DIM):
                    player = game_board[w][z][y][x]
                    if player == "":
                        continue
                    for dw, dz, dy, dx in directions:
                        line = []
                        try:
                            for i in range(4):
                                if game_board[w + i*dw][z + i*dz][y + i*dy][x + i*dx] == player:
                                    line.append((w + i*dw, z + i*dz, y + i*dy, x + i*dx))
                                else:
                                    break
                            if len(line) == 4:
                                winner_line = line
                                return player
                        except IndexError:
                            continue
    if all(game_board[w][z][y][x] != "" for w in range(DIM) for z in range(DIM) for y in range(DIM) for x in range(DIM)):
        return "Tie"
    return None

def handle_click(pos, cell_size):
    global current_player, winner_player
    if winner_player:
        return

    x, y = pos
    for w in range(DIM):
        for z in range(DIM):
            offset_x = MARGIN + w * (cell_size * DIM + GRID_SPACING)
            offset_y = MARGIN + z * (cell_size * DIM + GRID_SPACING)
            if offset_x <= x < offset_x + cell_size * DIM and offset_y <= y < offset_y + cell_size * DIM:
                grid_x = (x - offset_x) // cell_size
                grid_y = (y - offset_y) // cell_size
                if game_board[w][z][grid_y][grid_x] == "":
                    game_board[w][z][grid_y][grid_x] = current_player
                    winner = check_winner()
                    if winner:
                        draw_board(cell_size)
                        pygame.display.flip()
                        pygame.time.wait(400)
                        announce_winner(winner, cell_size)
                        return
                    current_player = "O" if current_player == "X" else "X"
                    return

def announce_winner(winner, cell_size):
    global winner_player
    winner_player = winner
    draw_board(cell_size)

def main():
    global WIDTH, HEIGHT, CELL_SIZE_CURRENT, screen
    running = True
    while running:
        draw_board(CELL_SIZE_CURRENT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                CELL_SIZE_CURRENT = max(10, min(WIDTH, HEIGHT) // (DIM * (DIM + 1)))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos, CELL_SIZE_CURRENT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
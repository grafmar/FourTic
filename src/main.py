import pygame
import asyncio

# --- Configuration ---
DIM = 4
CELL_SIZE = 30
MARGIN = 10
GRID_SPACING = 20

# --- Colors ---
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (230, 50, 50)
BLUE = (50, 50, 230)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
WIN_BG_X = (255, 220, 220)  # light red for X
WIN_BG_O = (220, 230, 255)  # light blue for O
BTN_COLOR = (100, 180, 255)
BTN_HOVER = (130, 200, 255)

pygame.init()
clock = pygame.time.Clock()

def create_font(size): return pygame.font.SysFont(None, max(14, size))
def calc_window_size(size):
    return (size * DIM + GRID_SPACING) * DIM + MARGIN, (size * DIM + GRID_SPACING) * DIM + MARGIN + 80

CELL_SIZE_CURRENT = CELL_SIZE
WIDTH, HEIGHT = calc_window_size(CELL_SIZE_CURRENT)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FourTic - 4D Tic-Tac-Toe")
font = create_font(CELL_SIZE_CURRENT)

game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
current_player = "X"
winner_line = []
winner_player = None
game_started = False  # <--- NEU

def reset_game():
    global game_board, current_player, winner_line, winner_player
    game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    current_player = "X"
    winner_line.clear()
    winner_player = None

def draw_button(label, y_offset):
    btn_width, btn_height = 160, 40
    rect = pygame.Rect(WIDTH // 2 - btn_width // 2, y_offset, btn_width, btn_height)
    mouse_pos = pygame.mouse.get_pos()
    color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    text = pygame.font.SysFont(None, 26).render(label, True, BLACK)
    screen.blit(text, text.get_rect(center=rect.center))
    return rect

def draw_board(size):
    global font
    if winner_player == "X":
        screen.fill(WIN_BG_X)
    elif winner_player == "O":
        screen.fill(WIN_BG_O)
    else:
        screen.fill(WHITE)

    font = create_font(size)
    for w in range(DIM):
        for z in range(DIM):
            ox = MARGIN + w * (size * DIM + GRID_SPACING)
            oy = MARGIN + z * (size * DIM + GRID_SPACING)
            pygame.draw.rect(screen, GRAY, (ox - 2, oy - 2, size * DIM + 4, size * DIM + 4), 2)
            for y in range(DIM):
                for x in range(DIM):
                    rect = pygame.Rect(ox + x * size, oy + y * size, size, size)
                    if (w, z, y, x) in winner_line:
                        if winner_player == "X":
                            pygame.draw.rect(screen, (255, 180, 180), rect)  # stronger red for X win
                        elif winner_player == "O":
                            pygame.draw.rect(screen, (180, 200, 255), rect)  # stronger blue for O win
                        else:
                            pygame.draw.rect(screen, GRAY, rect)
                    else:
                        base_color = WHITE if not winner_player else (WIN_BG_X if winner_player=="X" else WIN_BG_O)
                        pygame.draw.rect(screen, base_color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    mark = game_board[w][z][y][x]
                    if mark:
                        color = RED if mark == "X" else BLUE
                        text = font.render(mark, True, color)
                        screen.blit(text, text.get_rect(center=rect.center))

    msg_font = pygame.font.SysFont(None, max(24, size + 6))
    if winner_player:
        msg = msg_font.render(f"Player {winner_player} has won!", True, RED if current_player == "X" else BLUE)
    else:
        msg = msg_font.render(f"Next move: {current_player}", True, RED if current_player == "X" else BLUE)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 75)))

    return draw_button("Restart Game", HEIGHT - 50)

def check_winner():
    global winner_line
    winner_line = []
    dirs = []
    # alle 4D-Richtungen generieren (jede Kombination aus -1,0,1)
    for dw in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dw, dz, dy, dx) == (0, 0, 0, 0):
                        continue
                    # nur eine Richtung pro Linie (nicht doppelt)
                    if (dw, dz, dy, dx) > (0, 0, 0, 0):
                        dirs.append((dw, dz, dy, dx))

    for w in range(DIM):
        for z in range(DIM):
            for y in range(DIM):
                for x in range(DIM):
                    p = game_board[w][z][y][x]
                    if not p:
                        continue
                    for dw, dz, dy, dx in dirs:
                        line = []
                        try:
                            for i in range(4):
                                ww = w + i * dw
                                zz = z + i * dz
                                yy = y + i * dy
                                xx = x + i * dx
                                if ww < 0 or zz < 0 or yy < 0 or xx < 0:
                                    raise IndexError
                                if game_board[ww][zz][yy][xx] == p:
                                    line.append((ww, zz, yy, xx))
                                else:
                                    break
                            if len(line) == 4:
                                winner_line = line
                                return p
                        except IndexError:
                            continue

    if all(game_board[w][z][y][x]
           for w in range(DIM)
           for z in range(DIM)
           for y in range(DIM)
           for x in range(DIM)):
        return "Tie"
    return None

def handle_click(pos, size):
    global current_player, winner_player
    if winner_player: return
    x, y = pos
    for w in range(DIM):
        for z in range(DIM):
            ox = MARGIN + w * (size * DIM + GRID_SPACING)
            oy = MARGIN + z * (size * DIM + GRID_SPACING)
            if ox <= x < ox + size * DIM and oy <= y < oy + size * DIM:
                gx, gy = (x - ox)//size, (y - oy)//size
                if game_board[w][z][gy][gx] == "":
                    game_board[w][z][gy][gx] = current_player
                    wnr = check_winner()
                    if wnr:
                        winner_player = wnr
                    else:
                        current_player = "O" if current_player=="X" else "X"
                return

async def main():
    global WIDTH, HEIGHT, CELL_SIZE_CURRENT, screen, game_started
    await asyncio.sleep(0)
    running = True
    while running:
        screen.fill(WHITE)
        if not game_started:
            # --- Startbildschirm ---
            title = pygame.font.SysFont(None, 48).render("FourTic 4D", True, BLACK)
            msg = pygame.font.SysFont(None, 28).render("Tippe oder klicke zum Starten", True, GRAY)
            screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))
        else:
            btn_rect = draw_board(CELL_SIZE_CURRENT)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                CELL_SIZE_CURRENT = max(10, min(WIDTH, HEIGHT)//(DIM*(DIM+1)))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    game_started = True   # erster Klick startet nur das Spiel
                else:
                    if btn_rect.collidepoint(event.pos):
                        reset_game()
                    else:
                        handle_click(event.pos, CELL_SIZE_CURRENT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: reset_game()
                elif event.key == pygame.K_f: pygame.display.toggle_fullscreen()

        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())

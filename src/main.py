import pygame
import asyncio
import random

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
GRAY = (150, 150, 150)
WIN_BG_X = (255, 220, 220)  # light red for X
WIN_BG_O = (220, 230, 255)  # light blue for O
BTN_COLOR = (100, 180, 255)
BTN_HOVER = (130, 200, 255)

pygame.init()
clock = pygame.time.Clock()

def create_font(size):
    return pygame.font.SysFont(None, max(14, size))

def calc_window_size(size):
    return (size * DIM + GRID_SPACING) * DIM + MARGIN, (size * DIM + GRID_SPACING) * DIM + MARGIN + 80

CELL_SIZE_CURRENT = CELL_SIZE
WIDTH, HEIGHT = calc_window_size(CELL_SIZE_CURRENT)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FourTic - 4D Tic-Tac-Toe")
font = create_font(CELL_SIZE_CURRENT)

# --- Game State ---
game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
current_player = "X"
winner_line = []
winner_player = None
game_started = False
vs_computer = False

# Button placeholders (werden in main / draw_board gesetzt)
btn1 = None
btn2 = None
btn_restart = None
btn_mode = None

def reset_game():
    global game_board, current_player, winner_line, winner_player
    game_board = [[[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    current_player = "X"
    winner_line.clear()
    winner_player = None

def draw_button(label, y_offset, width=160):
    btn_height = 40
    rect = pygame.Rect(WIDTH // 2 - width // 2, y_offset, width, btn_height)
    mouse_pos = pygame.mouse.get_pos()
    color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    text = pygame.font.SysFont(None, 26).render(label, True, BLACK)
    screen.blit(text, text.get_rect(center=rect.center))
    return rect

def draw_board(size):
    global font, btn_restart, btn_mode
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
                    if (w, z, y, x) in winner_line and winner_player:
                        # stronger highlight for winner line
                        pygame.draw.rect(screen, (255, 180, 180) if winner_player == "X" else (180, 200, 255), rect)
                    else:
                        base_color = WHITE if not winner_player else (WIN_BG_X if winner_player == "X" else WIN_BG_O)
                        pygame.draw.rect(screen, base_color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    mark = game_board[w][z][y][x]
                    if mark:
                        color = RED if mark == "X" else BLUE
                        text = font.render(mark, True, color)
                        screen.blit(text, text.get_rect(center=rect.center))

    # status / message line
    msg_font = pygame.font.SysFont(None, max(24, size + 6))
    if winner_player:
        msg = msg_font.render(f"Player {winner_player} has won!", True,
                              RED if winner_player == "X" else BLUE)
    else:
        mode = "vs Computer" if vs_computer else "2 Player"
        msg = msg_font.render(f"Next move: {current_player}", True,
                              RED if current_player == "X" else BLUE)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 75)))

    # --- Buttons unten nebeneinander ---
    btn_y = HEIGHT - 55
    btn_restart_rect = pygame.Rect(WIDTH // 2 - 200, btn_y, 180, 40)
    btn_mode_rect = pygame.Rect(WIDTH // 2 + 20, btn_y, 180, 40)

    mouse_pos = pygame.mouse.get_pos()

    # Restart-Button
    color1 = BTN_HOVER if btn_restart_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color1, btn_restart_rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, btn_restart_rect, 2, border_radius=8)
    txt1 = pygame.font.SysFont(None, 26).render("Restart Game", True, BLACK)
    screen.blit(txt1, txt1.get_rect(center=btn_restart_rect.center))

    # Mode-Button
    color2 = BTN_HOVER if btn_mode_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color2, btn_mode_rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, btn_mode_rect, 2, border_radius=8)
    txt2 = pygame.font.SysFont(None, 26).render(
        "Mode: vs Computer" if vs_computer else "Mode: 2 Players", True, BLACK
    )
    screen.blit(txt2, txt2.get_rect(center=btn_mode_rect.center))

    return btn_restart_rect, btn_mode_rect



# --- Helper for directions (including diagonals in all signs) ---
def get_directions():
    dirs = []
    for dw in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dw, dz, dy, dx) != (0, 0, 0, 0):
                        dirs.append((dw, dz, dy, dx))
    return dirs

DIRECTIONS = get_directions()

def check_winner():
    global winner_line
    winner_line = []
    for w in range(DIM):
        for z in range(DIM):
            for y in range(DIM):
                for x in range(DIM):
                    p = game_board[w][z][y][x]
                    if not p:
                        continue
                    for dw, dz, dy, dx in DIRECTIONS:
                        line = []
                        valid = True
                        for i in range(4):
                            nw, nz, ny, nx = w + i * dw, z + i * dz, y + i * dy, x + i * dx
                            if 0 <= nw < DIM and 0 <= nz < DIM and 0 <= ny < DIM and 0 <= nx < DIM:
                                if game_board[nw][nz][ny][nx] == p:
                                    line.append((nw, nz, ny, nx))
                                else:
                                    valid = False
                                    break
                            else:
                                valid = False
                                break
                        if valid and len(line) == 4:
                            winner_line = line
                            return p
    if all(game_board[w][z][y][x] for w in range(DIM)
           for z in range(DIM)
           for y in range(DIM)
           for x in range(DIM)):
        return "Tie"
    return None

def available_moves():
    return [(w, z, y, x)
            for w in range(DIM)
            for z in range(DIM)
            for y in range(DIM)
            for x in range(DIM)
            if game_board[w][z][y][x] == ""]

def simulate_move(w, z, y, x, player):
    game_board[w][z][y][x] = player
    res = check_winner()
    game_board[w][z][y][x] = ""
    return res

def ai_move():
    moves = available_moves()
    if not moves:
        return
    # 1) try to win
    for move in moves:
        if simulate_move(*move, "O") == "O":
            game_board[move[0]][move[1]][move[2]][move[3]] = "O"
            return
    # 2) block opponent
    for move in moves:
        if simulate_move(*move, "X") == "X":
            game_board[move[0]][move[1]][move[2]][move[3]] = "O"
            return
    # 3) pick central-ish
    moves.sort(key=lambda m: abs(m[0] - (DIM-1)/2) + abs(m[1] - (DIM-1)/2) + abs(m[2] - (DIM-1)/2) + abs(m[3] - (DIM-1)/2))
    move = moves[0]
    game_board[move[0]][move[1]][move[2]][move[3]] = "O"

def handle_click(pos, size):
    global current_player, winner_player
    if winner_player:
        return
    x, y = pos
    for w in range(DIM):
        for z in range(DIM):
            ox = MARGIN + w * (size * DIM + GRID_SPACING)
            oy = MARGIN + z * (size * DIM + GRID_SPACING)
            if ox <= x < ox + size * DIM and oy <= y < oy + size * DIM:
                gx, gy = (x - ox) // size, (y - oy) // size
                if game_board[w][z][gy][gx] == "":
                    game_board[w][z][gy][gx] = current_player
                    wnr = check_winner()
                    if wnr:
                        winner_player = wnr
                    else:
                        # switch player
                        current_player = "O" if current_player == "X" else "X"
                        # if new current is O and mode is vs_computer, let AI play immediately
                        if vs_computer and current_player == "O" and not winner_player:
                            ai_move()
                            wnr2 = check_winner()
                            if wnr2:
                                winner_player = wnr2
                            else:
                                current_player = "X"
                return

async def main():
    global WIDTH, HEIGHT, CELL_SIZE_CURRENT, screen, game_started, vs_computer, btn1, btn2, btn_restart, btn_mode
    await asyncio.sleep(0)  # allow web init
    running = True
    while running:
        screen.fill(WHITE)
        if not game_started:
            title = pygame.font.SysFont(None, 48).render("FourTic 4D", True, BLACK)
            msg = pygame.font.SysFont(None, 28).render("Choose game mode:", True, GRAY)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            btn1 = draw_button("2 Players", HEIGHT // 2)
            btn2 = draw_button("Play vs Computer", HEIGHT // 2 + 60, width=220)
        else:
            btn_restart, btn_mode = draw_board(CELL_SIZE_CURRENT)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                CELL_SIZE_CURRENT = max(10, min(WIDTH, HEIGHT) // (DIM * (DIM + 1)))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    if btn1 and btn1.collidepoint(event.pos):
                        game_started = True
                        vs_computer = False
                    elif btn2 and btn2.collidepoint(event.pos):
                        game_started = True
                        vs_computer = True
                else:
                    # in-game buttons
                    if btn_restart and btn_restart.collidepoint(event.pos):
                        reset_game()
                    elif btn_mode and btn_mode.collidepoint(event.pos):
                        vs_computer = not vs_computer
                        reset_game()
                    else:
                        handle_click(event.pos, CELL_SIZE_CURRENT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())

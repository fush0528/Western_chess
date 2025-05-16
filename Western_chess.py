import pygame
import sys

# 初始化 Pygame 遊戲引擎
pygame.init()

# 遊戲常數設定
DEFAULT_WINDOW_SIZE = 800  # 預設視窗大小
MIN_WINDOW_SIZE = 400     # 最小視窗大小
MAX_WINDOW_SIZE = 1200    # 最大視窗大小
BOARD_SIZE = 8           # 棋盤大小 8x8
BUTTON_SIZE = 30         # 按鈕大小
BUTTON_MARGIN = 5        # 按鈕間距
BEIGE = (200, 220, 220)  # 米黃色 - 用於棋盤淺色格
DARK_BROWN = (139, 69, 19)  # 深棕色 - 用於棋盤深色格
BLACK = (0, 0, 0)        # 黑色 - 用於文字
HIGHLIGHT = (255, 255, 0, 100)  # 黃色半透明 - 用於高亮
VALID_MOVE_COLOR = (128, 128, 128, 128)  # 半透明灰色 - 用於顯示可移動位置

# 初始化遊戲視窗
screen = pygame.display.set_mode((DEFAULT_WINDOW_SIZE, DEFAULT_WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("西洋棋")

class ChessPiece:
    """棋子類別 - 定義每個棋子的屬性和行為"""
    
    def get_valid_moves(self, board):
        """計算棋子的合法移動位置"""
        valid_moves = []
        row, col = self.position
        
        if self.piece_type == 'pawn':
            # 白方兵向上移動
            if self.color == 'white':
                # 前進一格
                if row > 0 and board.board[row-1][col] is None:
                    valid_moves.append((row-1, col))
                    # 初始位置可前進兩格
                    if row == 6 and board.board[row-2][col] is None:
                        valid_moves.append((row-2, col))
                # 斜向吃子
                if row > 0 and col > 0 and board.board[row-1][col-1] and board.board[row-1][col-1].color != self.color:
                    valid_moves.append((row-1, col-1))
                if row > 0 and col < 7 and board.board[row-1][col+1] and board.board[row-1][col+1].color != self.color:
                    valid_moves.append((row-1, col+1))
            
            # 黑方兵向下移動
            else:
                # 前進一格
                if row < 7 and board.board[row+1][col] is None:
                    valid_moves.append((row+1, col))
                    # 初始位置可前進兩格
                    if row == 1 and board.board[row+2][col] is None:
                        valid_moves.append((row+2, col))
                # 斜向吃子
                if row < 7 and col > 0 and board.board[row+1][col-1] and board.board[row+1][col-1].color != self.color:
                    valid_moves.append((row+1, col-1))
                if row < 7 and col < 7 and board.board[row+1][col+1] and board.board[row+1][col+1].color != self.color:
                    valid_moves.append((row+1, col+1))
        
        elif self.piece_type == 'rook':
            # 城堡可以直線移動
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                current_row, current_col = row + dx, col + dy
                while 0 <= current_row < 8 and 0 <= current_col < 8:
                    target = board.board[current_row][current_col]
                    if target is None:
                        valid_moves.append((current_row, current_col))
                    elif target.color != self.color:
                        valid_moves.append((current_row, current_col))
                        break
                    else:
                        break
                    current_row += dx
                    current_col += dy
        
        elif self.piece_type == 'knight':
            # 騎士走L形
            moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
            for dx, dy in moves:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board.board[new_row][new_col]
                    if target is None or target.color != self.color:
                        valid_moves.append((new_row, new_col))
        
        elif self.piece_type == 'bishop':
            # 主教可以斜線移動
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                current_row, current_col = row + dx, col + dy
                while 0 <= current_row < 8 and 0 <= current_col < 8:
                    target = board.board[current_row][current_col]
                    if target is None:
                        valid_moves.append((current_row, current_col))
                    elif target.color != self.color:
                        valid_moves.append((current_row, current_col))
                        break
                    else:
                        break
                    current_row += dx
                    current_col += dy
        
        elif self.piece_type == 'queen':
            # 皇后可以直線和斜線移動
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                current_row, current_col = row + dx, col + dy
                while 0 <= current_row < 8 and 0 <= current_col < 8:
                    target = board.board[current_row][current_col]
                    if target is None:
                        valid_moves.append((current_row, current_col))
                    elif target.color != self.color:
                        valid_moves.append((current_row, current_col))
                        break
                    else:
                        break
                    current_row += dx
                    current_col += dy
        
        elif self.piece_type == 'king':
            # 國王可以向任意方向移動一格
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board.board[new_row][new_col]
                    if target is None or target.color != self.color:
                        valid_moves.append((new_row, new_col))
        
        return valid_moves
    def __init__(self, color, piece_type, position):
        self.color = color          # 棋子顏色
        self.piece_type = piece_type  # 棋子類型
        self.position = position    # 棋子位置
        self.image = None          # 棋子圖像
        self.chinese_name = self.get_chinese_name()  # 取得中文名稱
        self.load_image()          # 載入棋子圖像
    
    def get_chinese_name(self):
        """取得棋子的中文名稱"""
        names = {
            'pawn': '兵',
            'rook': '城堡',
            'knight': '騎士',
            'bishop': '主教',
            'queen': '皇后',
            'king': '國王'
        }
        return names.get(self.piece_type, '')
    
    def load_image(self):
        """使用基本圖形繪製棋子"""
        size = DEFAULT_WINDOW_SIZE // BOARD_SIZE
        # 建立透明背景的表面
        self.surface = pygame.Surface((size - 10, size - 10), pygame.SRCALPHA)
        color = (255, 255, 255) if self.color == 'white' else (0, 0, 0)
        
        # 根據不同棋子類型繪製不同形狀
        if self.piece_type == 'pawn':  # 兵 - 圓形
            pygame.draw.circle(self.surface, color, (size//2 - 5, size//2 - 5), size//4)
        elif self.piece_type == 'rook':  # 城堡 - 方形
            pygame.draw.rect(self.surface, color, (size//4 - 5, size//4 - 5, size//2, size//2))
        elif self.piece_type == 'knight':  # 騎士 - 三角形
            points = [(size//4 - 5, size//2 - 5), 
                     (size//2 - 5, size//4 - 5),
                     (3*size//4 - 5, size//2 - 5)]
            pygame.draw.polygon(self.surface, color, points)
        elif self.piece_type == 'bishop':  # 主教 - 尖頂三角形
            pygame.draw.polygon(self.surface, color, 
                              [(size//2 - 5, size//4 - 5),
                               (size//4 - 5, 3*size//4 - 5),
                               (3*size//4 - 5, 3*size//4 - 5)])
        elif self.piece_type == 'queen':  # 皇后 - 雙圓形
            pygame.draw.circle(self.surface, color, (size//2 - 5, size//2 - 5), size//3)
            pygame.draw.circle(self.surface, (128, 128, 128), (size//2 - 5, size//2 - 5), size//6)
        elif self.piece_type == 'king':  # 國王 - 圓形加十字
            pygame.draw.circle(self.surface, color, (size//2 - 5, size//2 - 5), size//3)
            pygame.draw.line(self.surface, (128, 128, 128), 
                           (size//2 - 5, size//4 - 5),
                           (size//2 - 5, 3*size//4 - 5), 3)
            pygame.draw.line(self.surface, (128, 128, 128),
                           (size//4 - 5, size//2 - 5),
                           (3*size//4 - 5, size//2 - 5), 3)

class Button:
    """按鈕類別 - 用於創建視窗控制按鈕"""
    def __init__(self, x, y, size, color, text, action):
        self.rect = pygame.Rect(x, y, size, size)  # 按鈕區域
        self.color = color      # 按鈕顏色
        self.text = text        # 按鈕文字
        self.action = action    # 按鈕動作
        self.hover = False      # 滑鼠懸停狀態

    def draw(self, screen):
        """繪製按鈕"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        try:
            font = pygame.font.SysFont("Microsoft JhengHei", 16, bold=True)
        except:
            font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        """處理按鈕事件"""
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            return self.action
        return None

class ChessBoard:
    """棋盤類別 - 管理棋盤和棋子"""
    def __init__(self, window_size):
        self.window_size = window_size
        self.square_size = window_size // BOARD_SIZE
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.scale = 1.0
        self.selected_piece = None
        self.valid_moves = []
        self.setup_board()
        
    def setup_board(self):
        """初始化棋盤佈局"""
        # 設置棋子初始排列順序
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        # 設置黑方棋子
        for i in range(BOARD_SIZE):
            self.board[1][i] = ChessPiece('black', 'pawn', (1, i))
            self.board[0][i] = ChessPiece('black', piece_order[i], (0, i))
            
        # 設置白方棋子
        for i in range(BOARD_SIZE):
            self.board[6][i] = ChessPiece('white', 'pawn', (6, i))
            self.board[7][i] = ChessPiece('white', piece_order[i], (7, i))
    
    def resize(self, window_size):
        """調整棋盤大小"""
        self.window_size = window_size
        self.square_size = int(window_size // BOARD_SIZE * self.scale)

    def draw(self, screen):
        """繪製棋盤和棋子"""
        board_surface = pygame.Surface((self.window_size, self.window_size), pygame.SRCALPHA)
        # 繪製棋盤格子
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = BEIGE if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(board_surface, color, 
                               (col * self.square_size, row * self.square_size, 
                                self.square_size, self.square_size))
                
                # 繪製棋子
                # 如果是有效移動位置，畫出半透明圓形
                if (row, col) in self.valid_moves:
                    circle_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, VALID_MOVE_COLOR,
                                     (self.square_size // 2, self.square_size // 2),
                                     self.square_size // 4)
                    board_surface.blit(circle_surface,
                                     (col * self.square_size, row * self.square_size))
                
                piece = self.board[row][col]
                if piece:
                    piece_surface = pygame.transform.scale(piece.surface, 
                        (int(self.square_size - 10), int(self.square_size - 10)))
                    board_surface.blit(piece_surface, 
                                   (col * self.square_size + 5, row * self.square_size + 5))
                    
                    # 如果是選中的棋子，畫出高亮效果
                    if piece == self.selected_piece:
                        highlight_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                        pygame.draw.rect(highlight_surface, HIGHLIGHT,
                                       (0, 0, self.square_size, self.square_size))
                        board_surface.blit(highlight_surface,
                                         (col * self.square_size, row * self.square_size))
        
        # 計算棋盤居中位置
        x_offset = (screen.get_width() - self.window_size * self.scale) // 2
        y_offset = (screen.get_height() - self.window_size * self.scale) // 2
        
        # 縮放並繪製棋盤
        scaled_surface = pygame.transform.scale(board_surface, 
            (int(self.window_size * self.scale), int(self.window_size * self.scale)))
        screen.blit(scaled_surface, (x_offset, y_offset))
    
    def get_piece_at_position(self, pos):
        """根據滑鼠位置獲取棋子的位置"""
        x, y = pos
        board_size = int(self.window_size * self.scale)
        x_offset = (pygame.display.get_surface().get_width() - board_size) // 2
        y_offset = (pygame.display.get_surface().get_height() - board_size) // 2
        
        # 根據縮放和偏移計算棋子位置
        x = (x - x_offset) / self.scale
        y = (y - y_offset) / self.scale
        
        row = int(y // (self.window_size / BOARD_SIZE))
        col = int(x // (self.window_size / BOARD_SIZE))
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col], (row, col)
        return None, None

    def handle_click(self, pos):
        """處理滑鼠點擊事件"""
        x, y = pos
        board_size = int(self.window_size * self.scale)
        x_offset = (pygame.display.get_surface().get_width() - board_size) // 2
        y_offset = (pygame.display.get_surface().get_height() - board_size) // 2
        
        # 根據縮放和偏移計算棋子位置
        x = (x - x_offset) / self.scale
        y = (y - y_offset) / self.scale
        
        row = int(y // (self.window_size / BOARD_SIZE))
        col = int(x // (self.window_size / BOARD_SIZE))
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            piece = self.board[row][col]
            if self.selected_piece is None:
                # 選擇棋子
                if piece:
                    self.selected_piece = piece
                    self.valid_moves = piece.get_valid_moves(self)
            else:
                # 移動棋子或選擇新的棋子
                if (row, col) in self.valid_moves:
                    # 移動棋子
                    old_row, old_col = self.selected_piece.position
                    self.board[old_row][old_col] = None
                    self.board[row][col] = self.selected_piece
                    self.selected_piece.position = (row, col)
                    self.selected_piece = None
                    self.valid_moves = []
                elif piece and piece.color == self.selected_piece.color:
                    # 選擇新的同色棋子
                    self.selected_piece = piece
                    self.valid_moves = piece.get_valid_moves(self)
                else:
                    # 取消選擇
                    self.selected_piece = None
                    self.valid_moves = []
            return piece, (row, col)
        return None, None

def draw_tooltip(screen, text, pos):
    """繪製提示框"""
    try:
        font = pygame.font.SysFont("Microsoft JhengHei", 24, bold=True)
    except:
        font = pygame.font.Font(None, 36)  # 如果無法加載微軟正黑體，使用默認字體
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos[0] + 10, pos[1] - 30)
    
    # 繪製背景
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10, 10)
    pygame.draw.rect(screen, BEIGE, bg_rect)
    pygame.draw.rect(screen, BLACK, bg_rect, 1)
    
    # 繪製文字
    screen.blit(text_surface, text_rect)

def main():
    """主程式循環"""
    global screen
    clock = pygame.time.Clock()
    current_size = DEFAULT_WINDOW_SIZE
    board = ChessBoard(current_size)
    
    # 建立視窗右上角的控制按鈕
    def update_button_positions():
        """更新按鈕位置"""
        window_width = screen.get_width()
        return [
            Button(window_width - (BUTTON_SIZE + BUTTON_MARGIN) * 3, BUTTON_MARGIN, BUTTON_SIZE, BEIGE, "➖", lambda: "minimize"),
            Button(window_width - (BUTTON_SIZE + BUTTON_MARGIN) * 2, BUTTON_MARGIN, BUTTON_SIZE, BEIGE, "🔲", lambda: "maximize"),
            Button(window_width - (BUTTON_SIZE + BUTTON_MARGIN), BUTTON_MARGIN, BUTTON_SIZE, (255, 128, 128), "❌", lambda: "quit")
        ]
    
    buttons = update_button_positions()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # 處理視窗大小調整
                new_size = min(max(min(event.w, event.h), MIN_WINDOW_SIZE), MAX_WINDOW_SIZE)
                screen = pygame.display.set_mode((new_size, new_size), pygame.RESIZABLE)
                current_size = new_size
                board.resize(current_size)
                buttons = update_button_positions()
            
            # 處理按鈕事件
            for button in buttons:
                action = button.handle_event(event)
                if action == "minimize":
                    pygame.display.iconify()  # 最小化視窗
                elif action == "maximize":
                    if screen.get_flags() & pygame.FULLSCREEN:
                        screen = pygame.display.set_mode((current_size, current_size), pygame.RESIZABLE)
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    buttons = update_button_positions()
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
        
        # 繪製遊戲畫面
        screen.fill(BEIGE)
        board.draw(screen)
        
        # 繪製按鈕
        for button in buttons:
            button.draw(screen)
        
        # 處理滑鼠點擊和懸停
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            piece, position = board.handle_click(mouse_pos)
        else:
            piece, position = board.get_piece_at_position(mouse_pos)
            if piece:
                tooltip_text = f"{piece.chinese_name} 在位置 {position}"
                draw_tooltip(screen, tooltip_text, mouse_pos)
        
        pygame.display.flip()  # 更新畫面
        clock.tick(60)  # 限制幀率為60fps

if __name__ == "__main__":
    main()

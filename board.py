"""
棋盤管理模組 - 這個檔案負責：
1. 管理西洋棋的棋盤狀態和佈局
2. 處理棋子的選擇和移動邏輯
3. 繪製棋盤、棋子和移動提示
4. 處理滑鼠互動和位置計算
"""

import pygame
from constants import (
    BOARD_SIZE, BEIGE, DARK_BROWN, HIGHLIGHT, 
    VALID_MOVE_COLOR
)
from pieces import ChessPiece

class ChessBoard:
    """
    棋盤類別：負責管理棋盤狀態和遊戲邏輯
    屬性：
        window_size: 視窗大小
        square_size: 每個棋格的大小
        board: 8x8的二維陣列，儲存棋盤上的棋子
        scale: 棋盤縮放比例
        selected_piece: 當前選中的棋子
        valid_moves: 當前選中棋子的有效移動位置列表
    """
    def __init__(self, window_size):
        """初始化棋盤屬性和狀態"""
        self.window_size = window_size
        self.square_size = window_size // BOARD_SIZE
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.scale = 1.0
        self.selected_piece = None
        self.valid_moves = []
        self.setup_board()
        
    def setup_board(self):
        """
        初始化棋盤佈局：
        - 設置黑白雙方的起始棋子位置
        - 按照西洋棋規則擺放各種棋子
        """
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
        """
        調整棋盤大小：
        根據新的視窗大小重新計算棋格大小
        """
        self.window_size = window_size
        self.square_size = int(window_size // BOARD_SIZE * self.scale)

    def draw(self, screen):
        """
        繪製棋盤和棋子：
        1. 繪製棋盤格子（交替的淺色和深色）
        2. 繪製有效移動位置的提示標記
        3. 繪製棋子
        4. 繪製選中棋子的高亮效果
        5. 處理棋盤的縮放和居中顯示
        """
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
        """
        根據滑鼠位置獲取棋子：
        - 將滑鼠座標轉換為棋盤格子位置
        - 考慮棋盤的縮放和偏移
        - 返回該位置的棋子和位置座標
        """
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
        """
        處理滑鼠點擊事件：
        1. 選擇棋子
           - 如果點擊空位，取消選擇
           - 如果點擊己方棋子，選中該棋子
        2. 移動棋子
           - 如果點擊有效移動位置，移動棋子
           - 如果點擊其他位置，取消選擇
        """
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

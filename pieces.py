"""
棋子管理模組 - 這個檔案負責：
1. 定義西洋棋的所有棋子類型和行為
2. 處理棋子的圖形繪製
3. 實現各種棋子的移動規則
4. 提供棋子的中文名稱轉換
"""

import pygame
from constants import DEFAULT_WINDOW_SIZE, BOARD_SIZE

class ChessPiece:
    """
    棋子類別：定義每個棋子的屬性和行為
    屬性：
        color: 棋子顏色（black/white）
        piece_type: 棋子類型（pawn/rook/knight/bishop/queen/king）
        position: 棋子在棋盤上的位置 (row, col)
        surface: 棋子的圖形表面
        chinese_name: 棋子的中文名稱
    """
    def __init__(self, color, piece_type, position):
        """初始化棋子的基本屬性"""
        self.color = color          # 棋子顏色
        self.piece_type = piece_type  # 棋子類型
        self.position = position    # 棋子位置
        self.image = None          # 棋子圖像
        self.chinese_name = self.get_chinese_name()  # 取得中文名稱
        self.load_image()          # 載入棋子圖像
    
    def get_chinese_name(self):
        """
        取得棋子的中文名稱
        返回：對應的中文名稱字串
        """
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
        """
        使用基本圖形繪製棋子：
        - 使用 Pygame 繪製簡單的幾何圖形來表示不同類型的棋子
        - 兵：圓形
        - 城堡：方形
        - 騎士：三角形
        - 主教：尖頂三角形
        - 皇后：雙圓形
        - 國王：圓形加十字
        """
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

    def get_valid_moves(self, board):
        """
        計算棋子的合法移動位置：
        根據不同棋子類型實現其特定的移動規則
        
        參數：
            board: 棋盤物件，用於檢查其他棋子位置
            
        返回：
            valid_moves: 包含所有合法移動位置的列表，每個位置為 (row, col) 座標
        """
        valid_moves = []
        row, col = self.position
        
        if self.piece_type == 'pawn':
            # 兵的移動規則：
            # 1. 通常只能向前移動一格
            # 2. 第一次移動可以選擇走一格或兩格
            # 3. 吃子時可以斜向前進一格
            if self.color == 'white':
                # 白方兵向上移動
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
            
            else:
                # 黑方兵向下移動
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
            # 城堡移動規則：可以直線移動任意格數（直到被擋住或吃子）
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
            # 騎士移動規則：走L形（兩格直走一格橫移）
            moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
            for dx, dy in moves:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board.board[new_row][new_col]
                    if target is None or target.color != self.color:
                        valid_moves.append((new_row, new_col))
        
        elif self.piece_type == 'bishop':
            # 主教移動規則：可以斜線移動任意格數
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
            # 皇后移動規則：結合城堡和主教的移動方式（直線+斜線）
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
            # 國王移動規則：可以向任意方向移動一格
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board.board[new_row][new_col]
                    if target is None or target.color != self.color:
                        valid_moves.append((new_row, new_col))
        
        return valid_moves

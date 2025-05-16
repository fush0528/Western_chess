"""
使用者介面模組 - 這個檔案負責：
1. 定義和管理視窗控制按鈕（最小化、最大化、關閉）
2. 實現滑鼠懸停提示框功能
3. 處理按鈕的互動事件和視覺效果
4. 管理按鈕在視窗調整大小時的位置更新
"""

import pygame
from constants import BEIGE, BLACK, BUTTON_SIZE, BUTTON_MARGIN

class Button:
    """
    按鈕類別：用於創建視窗控制按鈕
    屬性：
        rect: 按鈕的矩形區域
        color: 按鈕的背景顏色
        text: 按鈕上顯示的文字
        action: 按鈕點擊時執行的動作
        hover: 滑鼠是否懸停在按鈕上
    """
    def __init__(self, x, y, size, color, text, action):
        """
        初始化按鈕
        參數：
            x, y: 按鈕左上角的座標
            size: 按鈕的邊長（正方形）
            color: 按鈕的背景顏色
            text: 按鈕上顯示的文字
            action: 按鈕點擊時返回的動作字串
        """
        self.rect = pygame.Rect(x, y, size, size)  # 按鈕區域
        self.color = color      # 按鈕顏色
        self.text = text        # 按鈕文字
        self.action = action    # 按鈕動作
        self.hover = False      # 滑鼠懸停狀態

    def draw(self, screen):
        """
        繪製按鈕：
        1. 繪製按鈕背景
        2. 繪製按鈕邊框
        3. 載入並繪製按鈕文字
        """
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
        """
        處理按鈕事件：
        - 處理滑鼠移動（更新懸停狀態）
        - 處理滑鼠點擊（觸發按鈕動作）
        
        返回：
            若按鈕被點擊，返回對應的動作；否則返回 None
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            return self.action
        return None

def draw_tooltip(screen, text, pos):
    """
    繪製提示框：在滑鼠位置附近顯示文字提示
    
    參數：
        screen: Pygame 畫面物件
        text: 要顯示的提示文字
        pos: 滑鼠位置座標
    """
    try:
        font = pygame.font.SysFont("Microsoft JhengHei", 24, bold=True)
    except:
        font = pygame.font.Font(None, 36)  # 如果無法加載微軟正黑體，使用默認字體
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos[0] + 10, pos[1] - 30)
    
    # 繪製提示框背景
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10, 10)
    pygame.draw.rect(screen, BEIGE, bg_rect)
    pygame.draw.rect(screen, BLACK, bg_rect, 1)
    
    # 繪製提示文字
    screen.blit(text_surface, text_rect)

def update_button_positions(screen_width):
    """
    更新按鈕位置：根據視窗寬度重新計算並返回按鈕列表
    
    參數：
        screen_width: 視窗寬度
    
    返回：
        包含三個視窗控制按鈕的列表（最小化、最大化、關閉）
    """
    return [
        Button(screen_width - (BUTTON_SIZE + BUTTON_MARGIN) * 3, BUTTON_MARGIN, 
               BUTTON_SIZE, BEIGE, "➖", lambda: "minimize"),
        Button(screen_width - (BUTTON_SIZE + BUTTON_MARGIN) * 2, BUTTON_MARGIN, 
               BUTTON_SIZE, BEIGE, "🔲", lambda: "maximize"),
        Button(screen_width - (BUTTON_SIZE + BUTTON_MARGIN), BUTTON_MARGIN, 
               BUTTON_SIZE, (255, 128, 128), "❌", lambda: "quit")
    ]

"""
主程式檔案 - 這個檔案是西洋棋遊戲的入口點，負責：
1. 初始化遊戲視窗和基本設置
2. 處理主要遊戲循環
3. 處理視窗調整大小事件
4. 管理視窗控制按鈕（最小化、最大化、關閉）
5. 處理滑鼠事件和遊戲狀態更新
"""

import pygame
import sys
from constants import (
    DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE, MAX_WINDOW_SIZE,
    BEIGE, BUTTON_SIZE, BUTTON_MARGIN
)
from board import ChessBoard
from ui import update_button_positions, draw_tooltip

# 初始化 Pygame 遊戲引擎
pygame.init()

# 初始化遊戲視窗
screen = pygame.display.set_mode((DEFAULT_WINDOW_SIZE, DEFAULT_WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("西洋棋")

def main():
    """
    主程式循環函數：
    - 初始化遊戲時鐘和棋盤
    - 處理遊戲事件（關閉、調整視窗大小等）
    - 處理視窗控制按鈕事件
    - 更新遊戲狀態和畫面
    """
    global screen
    clock = pygame.time.Clock()
    current_size = DEFAULT_WINDOW_SIZE
    board = ChessBoard(current_size)
    
    # 建立視窗右上角的控制按鈕
    buttons = update_button_positions(screen.get_width())
    
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
                buttons = update_button_positions(screen.get_width())
            
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
                    buttons = update_button_positions(screen.get_width())
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
        
        # 繪製遊戲畫面
        screen.fill(BEIGE)
        board.draw(screen)
        
        # 繪製按鈕
        for button in buttons:
            button.draw(screen)
        
        # 處理滑鼠點擊和懸停事件
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

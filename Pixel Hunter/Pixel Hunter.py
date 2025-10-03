"""
Pixel Hunter - Ferramenta de captura de pixels com zoom
========================================================

Mostra uma janela com zoom 200x200 que segue o mouse.
Pressione '`' (grave/crase) para printar as coordenadas no terminal.
Pressione ESC para fechar.

Perfeito para capturar coordenadas e cores de pixels do jogo!
"""

import tkinter as tk
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageTk
import win32api
import win32con
import win32gui
import time
import keyboard
import threading


class PixelHunter:
    def __init__(self):
        self.running = True
        self.last_print = 0  # Evita spam de prints
        
        # Configurações
        self.zoom_size = 200  # Tamanho da área de zoom
        self.capture_size = 20  # Área capturada (será ampliada)
        self.update_interval = 50  # ms entre atualizações
        
        # Cria janela
        self.root = tk.Tk()
        self.root.title("Pixel Hunter - Caçador de Pixels")
        self.root.attributes('-topmost', True)  # Sempre no topo
        self.root.attributes('-alpha', 0.95)  # Levemente transparente
        self.root.resizable(False, False)
        
        # Canvas para desenhar
        self.canvas = tk.Canvas(
            self.root, 
            width=self.zoom_size + 20, 
            height=self.zoom_size + 130,
            bg='#2b2b2b',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Labels para informações
        self.window_label = tk.Label(
            self.root,
            text="Janela: N/A",
            font=('Consolas', 9),
            fg='#00ff00',
            bg='#2b2b2b'
        )
        self.window_label.place(x=10, y=self.zoom_size + 25)
        
        self.coord_label = tk.Label(
            self.root,
            text="X: 0, Y: 0 (Relativo à janela)",
            font=('Consolas', 11, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        self.coord_label.place(x=10, y=self.zoom_size + 45)
        
        self.screen_coord_label = tk.Label(
            self.root,
            text="Tela: X: 0, Y: 0",
            font=('Consolas', 9),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.screen_coord_label.place(x=10, y=self.zoom_size + 65)
        
        self.color_label = tk.Label(
            self.root,
            text="Color: #000000",
            font=('Consolas', 11, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        self.color_label.place(x=10, y=self.zoom_size + 85)
        
        # Instruções
        instructions = tk.Label(
            self.root,
            text="` = Print | ESC = Sair",
            font=('Consolas', 8),
            fg='#888888',
            bg='#2b2b2b'
        )
        instructions.place(x=10, y=self.zoom_size + 105)
        
        # Inicia captura
        self.update_zoom()
        
        # Monitora tecla '`' em thread separada
        self.monitor_thread = threading.Thread(target=self.monitor_key, daemon=True)
        self.monitor_thread.start()
        
        # Bind ESC para fechar
        self.root.bind('<Escape>', lambda e: self.close())
        
        # Protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        # Inicia loop
        self.root.mainloop()
    
    def monitor_key(self):
        """Monitora a tecla '`' para printar no terminal"""
        while self.running:
            try:
                if keyboard.is_pressed('`'):
                    # Evita spam (cooldown de 0.5s)
                    current_time = time.time()
                    if current_time - self.last_print > 0.5:
                        self.last_print = current_time
                        self.print_current_pixel()
                time.sleep(0.1)
            except Exception as e:
                print(f"[DEBUG] Erro no monitor de tecla: {e}")
                time.sleep(1)
    
    def get_mouse_position(self):
        """Obtém posição do mouse"""
        try:
            x, y = win32api.GetCursorPos()
            return x, y
        except:
            return 0, 0
    
    def get_window_under_mouse(self, x, y):
        """Obtém informações da janela sob o mouse"""
        try:
            # Pega a janela sob o ponto
            hwnd = win32gui.WindowFromPoint((x, y))
            
            # Pega o título da janela
            try:
                window_title = win32gui.GetWindowText(hwnd)
                if not window_title:
                    window_title = "Sem título"
            except:
                window_title = "N/A"
            
            # Pega a posição da ÁREA DO CLIENTE (sem bordas do Windows)
            try:
                # GetWindowRect retorna a posição da janela COM bordas
                window_rect = win32gui.GetWindowRect(hwnd)
                # GetClientRect retorna apenas o tamanho da área útil (0,0,width,height)
                client_rect = win32gui.GetClientRect(hwnd)
                
                # ClientToScreen converte ponto (0,0) da área do cliente para coordenadas da tela
                # Isso nos dá a posição REAL da área útil, sem contar bordas
                client_origin = win32gui.ClientToScreen(hwnd, (0, 0))
                
                window_x = client_origin[0]
                window_y = client_origin[1]
            except:
                # Fallback: usa GetWindowRect se ClientToScreen falhar
                try:
                    window_rect = win32gui.GetWindowRect(hwnd)
                    window_x = window_rect[0]
                    window_y = window_rect[1]
                except:
                    window_x = 0
                    window_y = 0
            
            return hwnd, window_title, window_x, window_y
        except Exception as e:
            return 0, "N/A", 0, 0
    
    def screen_to_window_coords(self, screen_x, screen_y, window_x, window_y):
        """Converte coordenadas da tela para coordenadas relativas à janela"""
        relative_x = screen_x - window_x
        relative_y = screen_y - window_y
        return relative_x, relative_y
    
    def get_pixel_color(self, x, y):
        """Obtém cor do pixel na posição x, y"""
        try:
            # Captura 1 pixel
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel = screenshot.getpixel((0, 0))
            
            # Converte RGB para hex
            if isinstance(pixel, tuple) and len(pixel) >= 3:
                hex_color = '#{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])
                colorref = '0x00{:02X}{:02X}{:02X}'.format(pixel[2], pixel[1], pixel[0])  # BGR format
                return hex_color, colorref, pixel
            return '#000000', '0x00000000', (0, 0, 0)
        except Exception as e:
            return '#000000', '0x00000000', (0, 0, 0)
    
    def capture_area(self, center_x, center_y):
        """Captura área ao redor do mouse"""
        try:
            # Calcula área de captura
            half_size = self.capture_size // 2
            left = center_x - half_size
            top = center_y - half_size
            right = center_x + half_size
            bottom = center_y + half_size
            
            # Captura screenshot
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # Redimensiona com zoom (nearest neighbor para pixels nítidos)
            zoomed = screenshot.resize(
                (self.zoom_size, self.zoom_size),
                Image.NEAREST
            )
            
            # Desenha crosshair no centro
            draw = ImageDraw.Draw(zoomed)
            center = self.zoom_size // 2
            
            # Cruz vermelha
            line_length = 10
            draw.line(
                [(center - line_length, center), (center + line_length, center)],
                fill='red',
                width=2
            )
            draw.line(
                [(center, center - line_length), (center, center + line_length)],
                fill='red',
                width=2
            )
            
            # Círculo ao redor do pixel central
            circle_radius = 5
            draw.ellipse(
                [
                    center - circle_radius,
                    center - circle_radius,
                    center + circle_radius,
                    center + circle_radius
                ],
                outline='red',
                width=2
            )
            
            return zoomed
        except Exception as e:
            # Retorna imagem preta em caso de erro
            return Image.new('RGB', (self.zoom_size, self.zoom_size), color='black')
    
    def update_zoom(self):
        """Atualiza o zoom e informações"""
        if not self.running:
            return
        
        try:
            # Obtém posição do mouse (coordenadas da tela)
            screen_x, screen_y = self.get_mouse_position()
            
            # Obtém informações da janela sob o mouse
            hwnd, window_title, window_x, window_y = self.get_window_under_mouse(screen_x, screen_y)
            
            # Converte para coordenadas relativas à janela
            relative_x, relative_y = self.screen_to_window_coords(screen_x, screen_y, window_x, window_y)
            
            # Captura área com zoom
            zoomed_image = self.capture_area(screen_x, screen_y)
            
            # Converte para PhotoImage
            photo = ImageTk.PhotoImage(zoomed_image)
            
            # Atualiza canvas
            self.canvas.delete('all')
            self.canvas.create_image(10, 10, anchor=tk.NW, image=photo)
            self.canvas.image = photo  # Mantém referência
            
            # Obtém cor do pixel central
            hex_color, colorref, rgb = self.get_pixel_color(screen_x, screen_y)
            
            # Atualiza labels
            window_display = window_title[:30] + "..." if len(window_title) > 30 else window_title
            self.window_label.config(text=f"Janela: {window_display} (HWND: {hwnd})")
            self.coord_label.config(text=f"X: {relative_x}, Y: {relative_y} (Relativo)")
            self.screen_coord_label.config(text=f"Tela: X: {screen_x}, Y: {screen_y}")
            self.color_label.config(text=f"Hex: {hex_color} | RGB: {rgb}")
            
            # Atualiza cor de fundo do label de cor
            try:
                self.color_label.config(bg=hex_color)
                # Calcula luminosidade para ajustar cor do texto
                luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
                text_color = '#000000' if luminance > 0.5 else '#ffffff'
                self.color_label.config(fg=text_color)
            except:
                pass
            
            # Posiciona janela próxima ao mouse (offset para não cobrir)
            window_x = screen_x + 30
            window_y = screen_y + 30
            
            # Ajusta se sair da tela
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if window_x + self.zoom_size + 40 > screen_width:
                window_x = screen_x - self.zoom_size - 60
            
            if window_y + self.zoom_size + 150 > screen_height:
                window_y = screen_y - self.zoom_size - 150
            
            self.root.geometry(f"+{window_x}+{window_y}")
            
            # Armazena valores atuais para print
            self.current_screen_x = screen_x
            self.current_screen_y = screen_y
            self.current_relative_x = relative_x
            self.current_relative_y = relative_y
            self.current_hwnd = hwnd
            self.current_window_title = window_title
            self.current_hex = hex_color
            self.current_colorref = colorref
            self.current_rgb = rgb
            
        except Exception as e:
            print(f"[DEBUG] Erro ao atualizar zoom: {e}")
        
        # Agenda próxima atualização
        if self.running:
            self.root.after(self.update_interval, self.update_zoom)
    
    def print_current_pixel(self):
        """Printa informações do pixel atual no terminal"""
        print("\n" + "="*70)
        print("🎯 PIXEL CAPTURADO")
        print("="*70)
        print(f"Janela:      {self.current_window_title}")
        print(f"HWND:        {self.current_hwnd}")
        print(f"─"*70)
        print(f"Coordenadas: ({self.current_relative_x}, {self.current_relative_y})  # Relativo à janela")
        print(f"Tela:        ({self.current_screen_x}, {self.current_screen_y})  # Absoluto")
        print(f"─"*70)
        print(f"Hex Color:   {self.current_hex}")
        print(f"ColorRef:    {self.current_colorref}  # Para config.py")
        print(f"RGB:         {self.current_rgb}")
        print("="*70)
        print(f'("Nome", ({self.current_relative_x}, {self.current_relative_y}), [{self.current_colorref}]),')
        print("="*70 + "\n")
    
    def close(self):
        """Fecha a aplicação"""
        self.running = False
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass


if __name__ == "__main__":
    print("="*60)
    print("🎯 PIXEL HUNTER - Caçador de Pixels v1.0")
    print("="*60)
    print()
    print("📋 Instruções:")
    print("  1. Mova o mouse sobre o pixel que deseja capturar")
    print("  2. Veja o zoom em tempo real na janela")
    print("  3. Pressione '`' (crase) para printar coordenadas")
    print("  4. Pressione ESC para fechar")
    print()
    print("💡 Dica: Use para capturar pixels do jogo e adicionar no config.py")
    print("="*60)
    print()
    
    try:
        app = PixelHunter()
    except KeyboardInterrupt:
        print("\n👋 Pixel Hunter encerrado.")
    except Exception as e:
        print(f"❌ Erro ao iniciar Pixel Hunter: {e}")
        print("\n📦 Instale as dependências:")
        print("   pip install pillow keyboard pywin32")

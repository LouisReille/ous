import pyxel
import math
from pathlib import Path

try:
    import vlc
    VLC_AVAILABLE = True
except (ImportError, OSError):
    VLC_AVAILABLE = False
    print("Warning: VLC not available. Game will run without audio.")

SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440

MAP_WIDTH = 24
MAP_HEIGHT = 24

worldMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],    
    [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class App:
    def __init__(self):
        # Audio disabled
        self.player = None

        # pl init state
        self.posX = 22
        self.posY = 12
        self.dirX = -1
        self.dirY = 0
        self.planeX = 0
        self.planeY = 0.66

        # nextbot init
        self.botX = 5
        self.botY = 5

        # pause state
        self.paused = False

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Raycaster")
        pyxel.mouse(True)

        # store mousex for rotation
        self.last_mouse_x = pyxel.mouse_x

        pyxel.run(self.update, self.draw)

    def update(self):
        # Handle pause toggle with ESC
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.paused = not self.paused
            if self.paused:
                pyxel.mouse(False)  # Release mouse to allow it to leave window
            else:
                pyxel.mouse(True)  # Capture mouse again
                self.last_mouse_x = pyxel.mouse_x  # Reset mouse tracking

        # If paused, only handle menu interactions
        if self.paused:
            # Check for quit button click
            mouse_x = pyxel.mouse_x
            mouse_y = pyxel.mouse_y
            quit_button_x = SCREEN_WIDTH // 2 - 100
            quit_button_y = SCREEN_HEIGHT // 2 + 50
            quit_button_w = 200
            quit_button_h = 50
            
            if (quit_button_x <= mouse_x <= quit_button_x + quit_button_w and
                quit_button_y <= mouse_y <= quit_button_y + quit_button_h and
                pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                pyxel.quit()
            return

        moveSpeed = 0.2
        botSpeed = 0.1
        sensitivity = 0.003  # mouse sensitivity

        # player movement forward/backward
        if pyxel.btn(pyxel.KEY_UP):
            if worldMap[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX += self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == 0:
                self.posY += self.dirY * moveSpeed

        if pyxel.btn(pyxel.KEY_DOWN):
            if worldMap[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX -= self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == 0:
                self.posY -= self.dirY * moveSpeed

        # strafe left/right (crab movement)
        if pyxel.btn(pyxel.KEY_LEFT):
            # Move perpendicular to direction (use plane vector for strafe)
            if worldMap[int(self.posX - self.planeX * moveSpeed)][int(self.posY)] == 0:
                self.posX -= self.planeX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY - self.planeY * moveSpeed)] == 0:
                self.posY -= self.planeY * moveSpeed

        if pyxel.btn(pyxel.KEY_RIGHT):
            # Move perpendicular to direction (use plane vector for strafe)
            if worldMap[int(self.posX + self.planeX * moveSpeed)][int(self.posY)] == 0:
                self.posX += self.planeX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY + self.planeY * moveSpeed)] == 0:
                self.posY += self.planeY * moveSpeed

        # mouse rotation (unlimited)
        mouse_x = pyxel.mouse_x
        edge_threshold = 20  # pixels from edge to trigger reset
        
        # Calculate mouse delta
        mouse_dx = mouse_x - self.last_mouse_x
        
        # When mouse reaches edge, reset tracking position to center to allow continuous rotation
        # This prevents rotation from stopping when mouse hits screen boundaries
        if mouse_x <= edge_threshold:
            # At or near left edge - reset to right side to allow continued left rotation
            self.last_mouse_x = SCREEN_WIDTH - edge_threshold
        elif mouse_x >= SCREEN_WIDTH - edge_threshold:
            # At or near right edge - reset to left side to allow continued right rotation
            self.last_mouse_x = edge_threshold
        else:
            # Normal case - update tracking position
            self.last_mouse_x = mouse_x
        
        # Recalculate delta after potential reset
        mouse_dx = mouse_x - self.last_mouse_x
        angle = -mouse_dx * sensitivity

        if angle != 0:
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(angle) - self.dirY * math.sin(angle)
            self.dirY = oldDirX * math.sin(angle) + self.dirY * math.cos(angle)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(angle) - self.planeY * math.sin(angle)
            self.planeY = oldPlaneX * math.sin(angle) + self.planeY * math.cos(angle)

        # nextbot simple follow collision
        dx = self.posX - self.botX
        dy = self.posY - self.botY
        dist = math.hypot(dx, dy)
        if dist > 0.1:
            moveX = (dx / dist) * botSpeed
            moveY = (dy / dist) * botSpeed
            # collision check
            if worldMap[int(self.botX + moveX)][int(self.botY)] == 0:
                self.botX += moveX
            if worldMap[int(self.botX)][int(self.botY + moveY)] == 0:
                self.botY += moveY

    def draw(self):
        pyxel.cls(0)

        # draw world
        for x in range(SCREEN_WIDTH):
            cameraX = 2 * x / SCREEN_WIDTH - 1
            rayDirX = self.dirX + self.planeX * cameraX
            rayDirY = self.dirY + self.planeY * cameraX

            mapX = int(self.posX)
            mapY = int(self.posY)

            deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else 1e30
            deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else 1e30

            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - self.posX) * deltaDistX

            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - self.posY) * deltaDistY

            hit = 0
            side = 0

            while hit == 0:
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1

                if worldMap[mapX][mapY] > 0:
                    hit = 1

            if side == 0:
                perpWallDist = sideDistX - deltaDistX
            else:
                perpWallDist = sideDistY - deltaDistY

            lineHeight = int(SCREEN_HEIGHT / perpWallDist)
            drawStart = max(0, -lineHeight // 2 + SCREEN_HEIGHT // 2)
            drawEnd = min(SCREEN_HEIGHT - 1, lineHeight // 2 + SCREEN_HEIGHT // 2)

            color = worldMap[mapX][mapY] % 16
            if side == 1:
                color = (color + 8) % 16

            pyxel.line(x, drawStart, x, drawEnd, color)

        # draw nextbot once per frame
        dx = self.botX - self.posX
        dy = self.botY - self.posY
        invDet = 1.0 / (self.planeX * self.dirY - self.dirX * self.planeY)
        transformX = invDet * (self.dirY * dx - self.dirX * dy)
        transformY = invDet * (-self.planeY * dx + self.planeX * dy)
        if transformY > 0:
            spriteScreenX = int((SCREEN_WIDTH / 2) * (1 + transformX / transformY))
            spriteHeight = int(SCREEN_HEIGHT / transformY)
            drawStartY = max(0, SCREEN_HEIGHT//2 - spriteHeight//2)
            drawEndY = min(SCREEN_HEIGHT-1, SCREEN_HEIGHT//2 + spriteHeight//2)
            pyxel.line(spriteScreenX, drawStartY, spriteScreenX, drawEndY, 10)

        # Draw pause menu overlay
        if self.paused:
            # Semi-transparent dark overlay
            pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)
            
            # Menu box
            menu_x = SCREEN_WIDTH // 2 - 150
            menu_y = SCREEN_HEIGHT // 2 - 100
            menu_w = 300
            menu_h = 200
            
            # Menu background
            pyxel.rect(menu_x, menu_y, menu_w, menu_h, 1)
            pyxel.rectb(menu_x, menu_y, menu_w, menu_h, 7)
            
            # Menu title
            title_text = "PAUSED"
            title_x = SCREEN_WIDTH // 2 - len(title_text) * 4
            pyxel.text(title_x, menu_y + 30, title_text, 7)
            
            # Quit button
            quit_button_x = SCREEN_WIDTH // 2 - 100
            quit_button_y = SCREEN_HEIGHT // 2 + 50
            quit_button_w = 200
            quit_button_h = 50
            
            # Check if mouse is hovering over quit button
            mouse_x = pyxel.mouse_x
            mouse_y = pyxel.mouse_y
            hover = (quit_button_x <= mouse_x <= quit_button_x + quit_button_w and
                     quit_button_y <= mouse_y <= quit_button_y + quit_button_h)
            
            # Draw quit button with hover effect
            button_color = 8 if hover else 2
            pyxel.rect(quit_button_x, quit_button_y, quit_button_w, quit_button_h, button_color)
            pyxel.rectb(quit_button_x, quit_button_y, quit_button_w, quit_button_h, 7)
            
            # Quit button text
            quit_text = "QUIT"
            quit_text_x = SCREEN_WIDTH // 2 - len(quit_text) * 4
            pyxel.text(quit_text_x, quit_button_y + 18, quit_text, 7)

App()

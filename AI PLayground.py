import sys
import math
import pygame


# =========================
# Config & Globals
# =========================
pygame.init()
WIN_W, WIN_H = 1000, 600
FPS = 60

BASE = 16           # base pixel-art grid size
SCALE = 3           # upscale pixel-art (nearest-neighbor)
TILE = BASE * SCALE # world tile size (48px if BASE=16 and SCALE=3)

GRAVITY = 2200.0
JUMP_VEL = 860.0
MAX_FALL = 1500.0
GROUND_ACCEL = 2600.0
AIR_ACCEL = 1600.0
GROUND_FRICTION = 2400.0
MAX_RUN = 340.0
COYOTE = 0.12
JUMP_BUFFER = 0.12

DASH_SPEED = 900.0
DASH_TIME = 0.15
DASH_COOLDOWN = 0.45

BG_COL = (17, 19, 27)
UI_COL = (230, 235, 245)

# =========================
# Tiny Pixel-Art Factory
# =========================
def make_sprite(pixels, palette, scale=SCALE):
    """
    pixels: list of strings with characters referencing keys in palette (e.g. ".#xo")
    palette: dict {char: (r,g,b, [a])}
    """
    h = len(pixels)
    w = len(pixels[0]) if h else 0
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for y, row in enumerate(pixels):
        for x, ch in enumerate(row):
            if ch == " ":
                continue
            col = palette.get(ch, None)
            if col:
                surf.set_at((x, y), col if len(col) == 4 else (*col, 255))
    if scale != 1:
        surf = pygame.transform.scale(surf, (w * scale, h * scale))
    return surf.convert_alpha()

def tint(surf, color):
    s = surf.copy()
    s.fill(color + (0,), special_flags=pygame.BLEND_RGBA_MULT)
    return s

# =========================
# Pixel Art Assets (drawn in code)
# =========================
PALETTE = {
    ".": (0, 0, 0, 0),   # transparent
    "#": (84, 92, 120),
    "B": (58, 66, 90),
    "g": (113, 176, 108),
    "d": (75, 126, 70),
    "s": (210, 70, 70),
    "y": (230, 208, 120),
    "w": (235, 235, 245),
    "t": (40, 44, 60),
    "b": (80, 120, 190),
    "k": (40, 40, 40),
    "c": (140, 220, 200),
    "o": (200, 140, 200),
}

# Ground tile (mossy stone)
GROUND_PIX = [
"################",
"#BBBBBBBBBBBBBB#",
"#B###########BB#",
"#B#gggggggg##B#",
"#B#ggdggggg##B#",
"#B###########B#",
"#B###########B#",
"#B###########B#",
"#B###########B#",
"#B###########B#",
"#B###########B#",
"#BBBBBBBBBBBBBB#",
"################",
"################",
"################",
"################",
]
GROUND_TILE = make_sprite(GROUND_PIX, PALETTE)

# One-way platform
PLAT_PIX = [
"................",
"................",
"................",
"................",
"................",
"................",
"................",
"................",
"................",
"................",
"................",
"################",
"################",
"################",
"################",
"################",
]
PLAT_TILE = make_sprite(PLAT_PIX, {**PALETTE, "#": (140, 140, 170)})

# Spike
SPIKE_PIX = [
"................",
"................",
"................",
".......ss.......",
"......sss.......",
".....sssss......",
"....sssssss.....",
"...sssssssss....",
"..sssssssssss...",
".sssssssssssss..",
"sssssssssssssss.",
"ssssssssssssssss",
"ssssssssssssssss",
"ssssssssssssssss",
"ssssssssssssssss",
"ssssssssssssssss",
]
SPIKE_TILE = make_sprite(SPIKE_PIX, PALETTE)

# Dash block (breakable while dashing)
DASH_PIX = [
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbkkkbbbbbbbb",
"bbbbkkkkkbbbbbbb",
"bbbbbkkkbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
"bbbbbbbbbbbbbbbb",
]
DASH_TILE = make_sprite(DASH_PIX, PALETTE)

# Save statue
SAVE_PIX = [
"................",
"......yyyy......",
".....yyyyyy.....",
"......yyyy......",
".......yy.......",
".......yy.......",
"......yyyy......",
".....yyyyyy.....",
"......yyyy......",
"......yyyy......",
"....yyyyyyyy....",
"...yyyyyyyyyy...",
"..yyyyyyyyyyyy..",
"..yyyyyyyyyyyy..",
"...yyyyyyyyyy...",
"....yyyyyyyy....",
]
SAVE_TILE = make_sprite(SAVE_PIX, PALETTE)

# Ability pickups
PICKUP_DJ_PIX = [
"................",
".......cc.......",
"......cccc......",
".....cccccc.....",
"......cccc......",
".......cc.......",
"......cccc......",
".....cccccc.....",
"......cccc......",
".......cc.......",
"................",
"................",
"................",
"................",
"................",
"................",
]
PICKUP_DS_PIX = [
"................",
".......ooo......",
"......ooooo.....",
".....ooooooo....",
"......ooooo.....",
".......ooo......",
"......ooooo.....",
".....ooooooo....",
"......ooooo.....",
".......ooo......",
"................",
"................",
"................",
"................",
"................",
"................",
]
PICKUP_MF_PIX = [
"................",
".......ggg......",
"......ggggg.....",
".....ggggggg....",
"......ggggg.....",
".......ggg......",
"......ggggg.....",
".....ggggggg....",
"......ggggg.....",
".......ggg......",
"................",
"................",
"................",
"................",
"................",
"................",
]
PICKUP_DJ = make_sprite(PICKUP_DJ_PIX, {**PALETTE, "c": (140, 220, 200)})
PICKUP_DS = make_sprite(PICKUP_DS_PIX, {**PALETTE, "o": (200, 140, 200)})
PICKUP_MF = make_sprite(PICKUP_MF_PIX, {**PALETTE, "g": (120, 200, 140)})

# Player (standing and morph)
PLAYER_STAND_PIX = [
"......kkkk......",
".....kkkkkk.....",
".....kkkkkk.....",
"......kkkk......",
"......wwww......",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"....wwwwwwww....",
".....wwwwww.....",
"......wwww......",
"......wwww......",
"......wwww......",
"......wwww......",
]
PLAYER_STAND = make_sprite(PLAYER_STAND_PIX, PALETTE)
PLAYER_MORPH_PIX = [
"................",
"................",
"................",
"................",
"................",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"...wwwwwwwwww...",
"................",
"................",
"................",
"................",
]
PLAYER_MORPH = make_sprite(PLAYER_MORPH_PIX, PALETTE)

# Walker enemy
WALKER_PIX = [
"................",
"................",
"......BBBB......",
".....BBBBBB.....",
"....BBBBBBBB....",
"...BBBBBBBBBB...",
"...BBBBBBBBBB...",
"...BBBBBBBBBB...",
"...BBBBBBBBBB...",
"...BBBBBBBBBB...",
"....BBBBBBBB....",
".....BBBBBB.....",
"......BBBB......",
"......BBBB......",
"......BBBB......",
"................",
]
WALKER = make_sprite(WALKER_PIX, {**PALETTE, "B": (150, 100, 120)})

# =========================
# World Layout
# Legend:
#   ' ' empty,
#   '#' solid ground,
#   '_' one-way platform,
#   '^' spikes (damage -> respawn),
#   'D' dash block (solid unless dashing, then breaks),
#   'a' Double Jump pickup,
#   'b' Dash pickup,
#   'c' Morph pickup,
#   'S' Save/checkpoint statue,
#   '|' crawl tunnel (1 tile high) – only passable when morphed
# =========================
WORLD = [
"################################################################################################################################################################",
"#                                                                              #                                                                               #",
"#                                    a                                         #                                           #######                              #",
"#                    #######                                                   #                                                S                               #",
"#                    #     #                            #######                #                    ######                                                          #",
"#        #######     #     #                            #     #                #                    #    #                                                         #",
"#        #     #     #     ######          #######      #     #       #######  #####       #####    #    #                                                         #",
"#   S    #     #     #           #          #   #       #     #       #     #      #       #   #    #    #    ^^^^                                                #",
"#        #     #     #     ^^^   ####       #   #    ####     #       #     #      #       #   #    ######     ^^                                                 #",
"#        #     ##### #############  ######  #   #      |                a    ##     #####  #   #        #        ^^                                                #",
"#        #                          _______  #   #      |                     #            ###          #######   #                                                #",
"#        #                 D                 #   #      |                     #                          D  #     #                           ######              #",
"#   ^^^^^#                                   #   #      |                     #                             #     #                          ##    ##             #",
"#        #                            b      #   #      |                     #                             #     #                         ##      ##            #",
"#        ##############   ####################   #      |                     #                             #     ######                   ##        ##           #",
"#                     #   #                        #######                    #                             #          #                 ##          ##          #",
"#     #######         #   #                              #################    #                             #######     #              ###            ###         #",
"#     #     #     ____#   #____                                                   ___                      #     #     #            ###                ###       #",
"#     #     #                              ________           #######             ___                     ##     ##    #          ###                    ###     #",
"#     #     #######        #########################          #     #                                     #       #    #######  ###                        ###   #",
"#     #             #                                    c    #  S  #                                     #   c   #          #####                            ### #",
"#     #   ^^^^^     #         ^^^^^                           #     #                               ^^^^^ #       #                                               ##",
"#     #             #######                                   #######                                     ##     ##                                              ##",
"#     #                    #     S                                  #                                       #     #                                               #",
"#     #######             ##                                        #######                                 #####     #     ##########                           #",
"#           #            ##                                                #                              ##    D     #     #        #                          #",
"#           #           ##                                                 #                             ##           #####   ####   #                          #",
"#           #   b      ##                                                  #                         ####                        #   #                          #",
"#     S     #         ##                                                   #                     #####                          #   #                          #",
"#           #        ##                                                    #######             ###                             #   #         a                 #",
"#___________#_______##______________________________________________________#____#_____________##_____________________________#__#__ ___________________________#",
"################################################################################################################################################################",
]

WORLD_H = len(WORLD)
WORLD_W = len(WORLD[0])

def in_bounds(tx, ty):
    return 0 <= tx < WORLD_W and 0 <= ty < WORLD_H

def ch_at(world, tx, ty):
    if in_bounds(tx, ty):
        return world[ty][tx]
    return '#'

# =========================
# Utility
# =========================
def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

# =========================
# Player
# =========================
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, int(10 * SCALE), int(14 * SCALE))  # approx to player sprite
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote = 0.0
        self.jump_buf = 0.0
        self.face = 1
        self.double_used = False

        # abilities
        self.abilities = {"DoubleJump": False, "Dash": False, "Morph": False}
        # morph state
        self.morph = False
        self.stand_size = self.rect.size
        self.morph_size = (self.rect.w, int(8 * SCALE))

        # dash state
        self.dashing = False
        self.dash_t = 0.0
        self.dash_cd = 0.0

        # checkpoint
        self.checkpoint = self.rect.topleft

    def has(self, name): return self.abilities.get(name, False)
    def give(self, name): self.abilities[name] = True
    def set_checkpoint(self, pos): self.checkpoint = pos

    def respawn(self):
        self.rect.topleft = self.checkpoint
        self.vel.xy = (0, 0)
        self.on_ground = False
        self.coyote = 0.0
        self.jump_buf = 0.0
        self.double_used = False
        self.dashing = False
        self.dash_t = 0.0
        self.dash_cd = 0.0
        self.morph = False
        # size reset
        self.rect.size = self.stand_size

    def toggle_morph(self, is_solid):
        if not self.has("Morph"):
            return
        if not self.morph:
            # morph: shrink (always possible)
            self.morph = True
            bottom = self.rect.bottomleft
            self.rect.size = self.morph_size
            self.rect.bottomleft = bottom
        else:
            # stand up: only if clear above
            test = self.rect.copy()
            test.size = self.stand_size
            test.bottomleft = (self.rect.left, self.rect.bottom)
            if not is_solid(test, morph=True, dashing=self.dashing, platforms=True, vely=self.vel.y):
                self.morph = False
                self.rect = test

    def input(self, keys):
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        jump = keys[pygame.K_w] or keys[pygame.K_SPACE]
        morph_key = keys[pygame.K_s] or keys[pygame.K_DOWN]
        dash_key = keys[pygame.K_k]
        return left, right, jump, morph_key, dash_key

    def update(self, dt, keys, is_solid, break_dash_blocks):
        left, right, jump, morph_key, dash_key = self.input(keys)

        # buffers
        if jump:
            self.jump_buf = JUMP_BUFFER
        else:
            self.jump_buf = max(0.0, self.jump_buf - dt)
        self.coyote = max(0.0, self.coyote - dt)

        # morph toggle (only on ground to prevent weirdness)
        if morph_key and self.has("Morph") and self.on_ground and abs(self.vel.y) < 5:
            self.toggle_morph(is_solid)

        # movement intent
        move = (-1 if left else 0) + (1 if right else 0)
        if move != 0:
            self.face = move

        accel = GROUND_ACCEL if self.on_ground else AIR_ACCEL
        self.vel.x += move * accel * dt
        if move == 0 and self.on_ground:
            if abs(self.vel.x) < GROUND_FRICTION * dt:
                self.vel.x = 0
            else:
                self.vel.x -= math.copysign(GROUND_FRICTION * dt, self.vel.x)

        max_run = MAX_RUN * (1.0 if self.on_ground else 1.15)
        self.vel.x = clamp(self.vel.x, -max_run, max_run)

        # dash
        if self.has("Dash"):
            if not self.dashing:
                if self.dash_cd > 0:
                    self.dash_cd -= dt
                if dash_key and self.dash_cd <= 0 and move != 0:
                    self.dashing = True
                    self.dash_t = DASH_TIME
                    self.vel.y = 0
                    self.vel.x = self.face * DASH_SPEED
            else:
                self.dash_t -= dt
                if self.dash_t <= 0:
                    self.dashing = False
                    self.dash_cd = DASH_COOLDOWN

        # gravity
        g = GRAVITY * (0.25 if self.dashing else 1.0)
        self.vel.y = min(self.vel.y + g * dt, MAX_FALL)

        # jump & double jump
        if self.on_ground:
            self.double_used = False
        can_jump = (self.on_ground or self.coyote > 0.0) and self.jump_buf > 0.0
        if can_jump:
            self.vel.y = -JUMP_VEL
            self.on_ground = False
            self.coyote = 0.0
            self.jump_buf = 0.0
        elif (not self.on_ground) and self.has("DoubleJump") and (not self.double_used) and self.jump_buf > 0.0:
            self.vel.y = -JUMP_VEL * 0.9
            self.double_used = True
            self.jump_buf = 0.0

        # variable jump height (early release)
        if not jump and self.vel.y < 0:
            self.vel.y += 1600 * dt

        # pre-move: break dash blocks if dashing
        if self.dashing:
            break_dash_blocks(self.rect)

        # move & collide
        self._move_and_collide(dt, is_solid)

        # post-move: break dash blocks again
        if self.dashing:
            break_dash_blocks(self.rect)

    def _move_and_collide(self, dt, is_solid):
        # X
        dx = self.vel.x * dt
        self.rect.x += int(dx)
        if is_solid(self.rect, morph=self.morph, dashing=self.dashing, platforms=False, vely=self.vel.y):
            step = -1 if dx > 0 else 1
            while is_solid(self.rect, morph=self.morph, dashing=self.dashing, platforms=False, vely=self.vel.y):
                self.rect.x += step
            self.vel.x = 0

        # Y
        dy = self.vel.y * dt
        self.rect.y += int(dy)
        hit = is_solid(self.rect, morph=self.morph, dashing=self.dashing, platforms=True, vely=self.vel.y)
        if hit:
            step = -1 if dy > 0 else 1
            while is_solid(self.rect, morph=self.morph, dashing=self.dashing, platforms=True, vely=self.vel.y):
                self.rect.y += step
            if dy > 0:
                self.on_ground = True
                self.coyote = COYOTE
            self.vel.y = 0
        else:
            self.on_ground = False

# =========================
# Enemy
# =========================
class Walker:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, int(12 * SCALE), int(12 * SCALE))
        self.velx = -100
        self.alive = True

    def update(self, dt, is_solid, tiles):
        if not self.alive:
            return
        # patrol: turn at edges or walls
        self.rect.x += int(self.velx * dt)
        if is_solid(self.rect, platforms=False, morph=True, dashing=False, vely=0):
            # hit wall -> turn
            self.rect.x -= int(self.velx * dt)
            self.velx *= -1
        # edge detect: if tile below front is empty, turn
        front = self.rect.midbottom
        frontx = front[0] + (8 if self.velx > 0 else -8)
        foot_tx = int(frontx // TILE)
        foot_ty = int((self.rect.bottom + 4) // TILE)
        if not (0 <= foot_tx < WORLD_W and 0 <= foot_ty < WORLD_H):
            self.velx *= -1
        else:
            below = tiles[foot_ty][foot_tx]
            if below == " ":
                self.velx *= -1

    def draw(self, surf, camx, camy):
        if not self.alive:
            return
        surf.blit(WALKER, (self.rect.x - camx, self.rect.y - camy))

# =========================
# Game
# =========================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Gated Caverns — Metroidvania (pygame)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)

        # world is mutable (so we can break dash blocks / collect items)
        self.world = [list(row) for row in WORLD]

        # spawn at first S
        sp = self.find_first('S') or (2, 2)
        self.player = Player(sp[0] * TILE + 6, sp[1] * TILE - 4)
        self.player.set_checkpoint((sp[0] * TILE + 6, sp[1] * TILE - 4))

        # enemies
        self.enemies = [
            Walker(20 * TILE, 22 * TILE),
            Walker(60 * TILE, 22 * TILE),
            Walker(90 * TILE, 10 * TILE),
        ]

        # camera
        self.camx = 0
        self.camy = 0

        # message
        self.message = ""
        self.msg_t = 0.0

        # discovered for minimap
        self.discovered = set()

    # ---------- helpers ----------
    def find_first(self, ch):
        for y, row in enumerate(self.world):
            for x, c in enumerate(row):
                if c == ch:
                    return (x, y)
        return None

    def set_msg(self, text, t=2.6):
        self.message = text
        self.msg_t = t

    def ch(self, tx, ty):
        if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            return self.world[ty][tx]
        return '#'

    def set_ch(self, tx, ty, ch):
        if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            self.world[ty][tx] = ch

    def is_solid_rect(self, rect, *, morph=False, dashing=False, platforms=True, vely=0):
        tminx, tmaxx = rect.left // TILE, (rect.right - 1) // TILE
        tminy, tmaxy = rect.top // TILE, (rect.bottom - 1) // TILE
        for ty in range(tminy, tmaxy + 1):
            for tx in range(tminx, tmaxx + 1):
                ch = self.ch(tx, ty)
                # platforms (only when falling and feet above)
                if platforms and ch == "_":
                    if vely >= 0 and rect.bottom > ty * TILE and (rect.bottom - vely / max(1, FPS)) <= ty * TILE + 10:
                        return True
                    continue
                if self.is_solid_ch(ch, morph=morph, dashing=dashing):
                    return True
        return False

    def is_solid_ch(self, ch, *, morph=False, dashing=False):
        if ch == '#':
            return True
        if ch == 'D':
            return not dashing
        if ch == '|':
            return not morph
        return False

    def spikes_hit(self, rect):
        tminx, tmaxx = rect.left // TILE, (rect.right - 1) // TILE
        tminy, tmaxy = rect.top // TILE, (rect.bottom - 1) // TILE
        for ty in range(tminy, tmaxy + 1):
            for tx in range(tminx, tmaxx + 1):
                if self.ch(tx, ty) == '^':
                    return True
        return False

    def collectables_at(self, rect):
        got = []
        tminx, tmaxx = rect.left // TILE, (rect.right - 1) // TILE
        tminy, tmaxy = rect.top // TILE, (rect.bottom - 1) // TILE
        for ty in range(tminy, tmaxy + 1):
            for tx in range(tminx, tmaxx + 1):
                ch = self.ch(tx, ty)
                if ch in ('a', 'b', 'c', 'S'):
                    got.append((tx, ty, ch))
        return got

    def break_dash_blocks(self, rect):
        tminx, tmaxx = rect.left // TILE, (rect.right - 1) // TILE
        tminy, tmaxy = rect.top // TILE, (rect.bottom - 1) // TILE
        for ty in range(tminy, tmaxy + 1):
            for tx in range(tminx, tmaxx + 1):
                if self.ch(tx, ty) == 'D':
                    self.set_ch(tx, ty, ' ')

    # ---------- update/draw ----------
    def update(self, dt):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        # player
        self.player.update(dt, keys, self.is_solid_rect, self.break_dash_blocks)

        # spikes -> respawn
        if self.spikes_hit(self.player.rect):
            self.player.respawn()
            self.set_msg("Ouch! Back to the last save statue.")

        # items & save
        for tx, ty, ch in self.collectables_at(self.player.rect):
            if ch == 'a':
                if not self.player.has("DoubleJump"):
                    self.player.give("DoubleJump")
                    self.set_msg("Double Jump unlocked!")
                self.set_ch(tx, ty, ' ')
            elif ch == 'b':
                if not self.player.has("Dash"):
                    self.player.give("Dash")
                    self.set_msg("Dash unlocked! (K)")
                self.set_ch(tx, ty, ' ')
            elif ch == 'c':
                if not self.player.has("Morph"):
                    self.player.give("Morph")
                    self.set_msg("Morph/Crawl unlocked! (S)")
                self.set_ch(tx, ty, ' ')
            elif ch == 'S':
                self.player.set_checkpoint((tx * TILE + 6, ty * TILE - 4))
                self.set_msg("Game saved.")

        # enemies
        for en in self.enemies:
            en.update(dt, self.is_solid_rect, self.world)

        # camera
        targetx = self.player.rect.centerx - WIN_W // 2
        targety = self.player.rect.centery - WIN_H // 2
        self.camx += int((targetx - self.camx) * 0.15)
        self.camy += int((targety - self.camy) * 0.15)
        self.camx = clamp(self.camx, 0, WORLD_W * TILE - WIN_W)
        self.camy = clamp(self.camy, 0, WORLD_H * TILE - WIN_H)

        # message timer
        if self.msg_t > 0:
            self.msg_t -= dt
            if self.msg_t <= 0:
                self.message = ""

        # discovered
        self.mark_discovered()

    def mark_discovered(self):
        tminx, tmaxx = self.camx // TILE, (self.camx + WIN_W) // TILE
        tminy, tmaxy = self.camy // TILE, (self.camy + WIN_H) // TILE
        for ty in range(max(0, tminy), min(WORLD_H, tmaxy + 1)):
            for tx in range(max(0, tminx), min(WORLD_W, tmaxx + 1)):
                self.discovered.add((tx, ty))

    def draw_text(self, surf, text, pos, color=UI_COL, center=False):
        """Draw text; 'center' is keyword-only to avoid arg mixups."""
        img = self.font.render(text, True, color)
        rect = img.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        surf.blit(img, rect)

    def draw_tile(self, ch, x, y, surf):
        px, py = x * TILE - self.camx, y * TILE - self.camy
        if ch == '#':
            surf.blit(GROUND_TILE, (px, py))
        elif ch == '_':
            surf.blit(PLAT_TILE, (px, py))
        elif ch == '^':
            surf.blit(SPIKE_TILE, (px, py))
        elif ch == 'D':
            surf.blit(DASH_TILE, (px, py))
        elif ch == 'S':
            surf.blit(SAVE_TILE, (px, py))
        elif ch == 'a':
            surf.blit(PICKUP_DJ, (px, py))
        elif ch == 'b':
            surf.blit(PICKUP_DS, (px, py))
        elif ch == 'c':
            surf.blit(PICKUP_MF, (px, py))
        elif ch == '|':
            # narrow crawl tunnel hint
            pygame.draw.rect(surf, (90, 120, 90), (px, py + TILE - int(TILE * 0.35), TILE, int(TILE * 0.35)))

    def draw_world(self, surf):
        # simple parallax strips
        surf.fill(BG_COL)
        for i in range(7):
            y = ((i * 90) - (self.camy // 4)) % (WIN_H + 90) - 90
            pygame.draw.rect(surf, (22 + i * 3, 24 + i * 3, 32 + i * 3), (0, y, WIN_W, 50))

        # tiles
        tminx, tmaxx = self.camx // TILE - 1, (self.camx + WIN_W) // TILE + 1
        tminy, tmaxy = self.camy // TILE - 1, (self.camy + WIN_H) // TILE + 1
        for ty in range(max(0, tminy), min(WORLD_H, tmaxy + 1)):
            for tx in range(max(0, tminx), min(WORLD_W, tmaxx + 1)):
                ch = self.ch(tx, ty)
                if ch != ' ':
                    self.draw_tile(ch, tx, ty, surf)

        # enemies
        for en in self.enemies:
            en.draw(surf, self.camx, self.camy)

        # player sprite
        pr = self.player.rect.move(-self.camx, -self.camy)
        if self.player.morph:
            surf.blit(PLAYER_MORPH, (pr.x - (PLAYER_MORPH.get_width() - pr.w) // 2,
                                     pr.y - (PLAYER_MORPH.get_height() - pr.h)))
        else:
            # face direction: flip when facing left
            img = pygame.transform.flip(PLAYER_STAND, self.player.face < 0, False)
            surf.blit(img, (pr.x - (img.get_width() - pr.w) // 2,
                            pr.y - (img.get_height() - pr.h)))

        # UI
        # abilities HUD
        x = 10
        def pill(lbl, on):
            nonlocal x
            w, h = 150, 28
            pygame.draw.rect(surf, (70, 110, 200) if on else (60, 60, 70), (x, 8, w, h), border_radius=14)
            pygame.draw.rect(surf, (255, 255, 255), (x, 8, w, h), 1, border_radius=14)
            self.draw_text(surf, lbl, (x + w // 2, 22), center=True)
            x += w + 8
        pill("Double Jump", self.player.has("DoubleJump"))
        pill("Dash (K)", self.player.has("Dash"))
        pill("Morph (S)", self.player.has("Morph"))

        # message bar
        if self.message:
            box = pygame.Rect(0, WIN_H - 64, WIN_W, 56)
            pygame.draw.rect(surf, (20, 20, 24), box)
            pygame.draw.rect(surf, (255, 255, 255), box, 1)
            self.draw_text(surf, self.message, (16, WIN_H - 40))

        # minimap strip
        mm_w, mm_h = 240, 90
        mm = pygame.Rect(WIN_W - mm_w - 10, 8, mm_w, mm_h)
        pygame.draw.rect(surf, (25, 27, 34), mm, border_radius=6)
        pygame.draw.rect(surf, (255, 255, 255), mm, 1, border_radius=6)
        sx = mm_w / WORLD_W
        sy = mm_h / WORLD_H
        for (tx, ty) in self.discovered:
            rx = int(mm.x + tx * sx)
            ry = int(mm.y + ty * sy)
            surf.fill((80, 120, 180), (rx, ry, max(1, int(sx)), max(1, int(sy))))
        px = int(mm.x + (self.player.rect.centerx / TILE) * sx)
        py = int(mm.y + (self.player.rect.centery / TILE) * sy)
        pygame.draw.rect(surf, (255, 255, 255), (px, py, 2, 2))

    def draw(self):
        self.draw_world(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.update(dt)
            self.draw()

# =========================
# Boot
# =========================
if __name__ == "__main__":
    Game().run()

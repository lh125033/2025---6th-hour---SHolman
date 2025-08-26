#!/usr/bin/env python3
"""
Pixel Blackjack – an in‑depth blackjack game with retro pixel art
=================================================================

Single‑file pygame program. No external assets required.

Features
--------
• 6‑deck shoe with realistic dealing/shuffling (cut card, burn)
• Player bank + chip betting (1, 5, 25, 100, 500)
• Actions: Hit, Stand, Double, Split (re‑splits up to 4 hands), Surrender
• Insurance (when dealer shows Ace), Blackjack pays 3:2
• Dealer stands on soft 17 (configurable)
• Clean, crisp pixel‑art cards, suits, and chips rendered from code
• Pixel UI with buttons, hand labels, result banners

How to run
----------
1) Install pygame:    pip install pygame
2) Run:               python pixel_blackjack.py

Controls
--------
• Click chips to compose your bet. Click bet again to remove last chip.
• Click DEAL to start a hand.
• During your turn, click HIT, STAND, DOUBLE, SPLIT, or SURRENDER.
• When offered, click INSURE to place an insurance bet (up to half your main bet).
• After the round, click NEXT ROUND to continue.

Note: This is a single‑player game vs the dealer.
"""

import math
import random
import sys
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import pygame

# -----------------------------
# Config
# -----------------------------
SCREEN_W, SCREEN_H = 1060, 720
FPS = 60
DECKS_IN_SHOE = 6
BLACKJACK_PAYS = (3, 2)  # 3:2
DEALER_STAND_SOFT_17 = True
MAX_SPLIT_HANDS = 4

# Colors (RGB)
BLACK = (12, 12, 12)
WHITE = (240, 240, 240)
SHADOW = (0, 0, 0)
TABLE_GREEN = (14, 70, 44)
GOLD = (235, 190, 72)
RED = (205, 68, 68)
BLUE = (76, 138, 199)
GREY = (120, 120, 120)
DARKRED = (140, 30, 30)

# -----------------------------
# Utility: tiny pixel font (5x7) and helpers
# -----------------------------
# Each char is 5 columns x 7 rows, using strings of 0/1
PIX_FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'K': ["10001","10010","11100","10010","10001","10001","10001"],
    'Q': ["01110","10001","10001","10101","10011","01111","00001"],
    'J': ["00111","00001","00001","00001","10001","10001","01110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","11100"],
}


def blit_pix_text(surface: pygame.Surface, text: str, pos: Tuple[int, int], color=BLACK, scale=2):
    x, y = pos
    for ch in text:
        glyph = PIX_FONT.get(ch.upper())
        if glyph is None:
            x += 6 * scale
            continue
        for row, row_bits in enumerate(glyph):
            for col, bit in enumerate(row_bits):
                if bit == '1':
                    pygame.draw.rect(surface, color, (x + col*scale, y + row*scale, scale, scale))
        x += (5 + 1) * scale  # 1px gap

# -----------------------------
# Pixel‑art suits (16x16) built from code
# -----------------------------

def suit_surface(suit: str, fg=(40, 40, 40), scale=2) -> pygame.Surface:
    """Return a pixelated 16x16 suit icon surface scaled by 'scale'."""
    surf = pygame.Surface((16, 16), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    def px(x, y):
        surf.set_at((x, y), fg)

    if suit == 'S':  # spade
        for y in range(3, 11):
            for x in range(3 + abs(7 - y), 13 - abs(7 - y)):
                px(x, y)
        for y in range(11, 13):
            for x in range(6, 10):
                px(x, y)
        for y in range(13, 16):
            px(7, y); px(8, y)
    elif suit == 'H':  # heart
        for y in range(4, 10):
            for x in range(4 - (y-4), 7 + (y-4)):
                px(x, y)
            for x in range(9 - (y-4), 12 + (y-4)):
                px(x, y)
        for y in range(10, 15):
            for x in range(3 + (y-10), 13 - (y-10)):
                px(x, y)
    elif suit == 'D':  # diamond
        for y in range(3, 13):
            span = abs(8 - y)
            for x in range(8 - (7 - span), 9 + (7 - span)):
                px(x-1, y)
    elif suit == 'C':  # club
        # three blobs + stem
        for cx, cy, r in [(6, 7, 3), (10, 7, 3), (8, 4, 3)]:
            for y in range(cy-r, cy+r+1):
                for x in range(cx-r, cx+r+1):
                    if (x-cx)**2 + (y-cy)**2 <= r*r:
                        px(x, y)
        for y in range(11, 14):
            for x in range(7, 9):
                px(x, y)
        for y in range(14, 16):
            px(7, y); px(8, y)

    if scale != 1:
        surf = pygame.transform.scale(surf, (16*scale, 16*scale))
    return surf

# -----------------------------
# Card rendering (pixel card built from primitives, then scaled up)
# -----------------------------
CARD_W, CARD_H = 44, 60          # base pixel canvas size
CARD_SCALE = 4                   # on‑screen scale (final ~176x240)

RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
SUITS = ['S','H','D','C']


@dataclass
class Card:
    rank: str
    suit: str

    @property
    def value(self):
        if self.rank in ['J','Q','K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)


def draw_card_surface(card: Optional[Card], face_up=True) -> pygame.Surface:
    base = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)

    # Background with border
    card_bg = (235, 234, 230)
    border = (60, 60, 60)
    pygame.draw.rect(base, card_bg, (0, 0, CARD_W, CARD_H))
    for i in range(0, 2):
        pygame.draw.rect(base, border, (i, i, CARD_W-2*i-1, CARD_H-2*i-1), 1)

    if not face_up or card is None:
        # simple pixel back pattern
        for y in range(4, CARD_H-4, 2):
            for x in range(4 + (y%4), CARD_W-4, 4):
                pygame.draw.rect(base, BLUE, (x, y, 2, 2))
        # label
        blit_pix_text(base, "BJ", (CARD_W-14, CARD_H-12), color=WHITE, scale=1)
    else:
        # corners rank
        corner_col = DARKRED if card.suit in ('H','D') else (40, 40, 40)
        rank_text = card.rank if card.rank != '10' else '10'
        blit_pix_text(base, rank_text, (4, 4), color=corner_col, scale=1)
        blit_pix_text(base, rank_text, (CARD_W-4 - (len(rank_text)*6), CARD_H-12), color=corner_col, scale=1)

        # suit corner pips (tiny)
        tiny = suit_surface(card.suit, fg=corner_col, scale=1)
        base.blit(tiny, (4, 14))
        base.blit(tiny, (CARD_W-4-16, CARD_H-14-16))

        # big center suit
        center = suit_surface(card.suit, fg=corner_col, scale=2)
        base.blit(center, (CARD_W//2 - center.get_width()//2, CARD_H//2 - center.get_height()//2))

    if CARD_SCALE != 1:
        base = pygame.transform.scale(base, (CARD_W*CARD_SCALE, CARD_H*CARD_SCALE))
    return base

# Pre‑render a cache of all faces and back
CARD_CACHE = {}
for s in SUITS:
    for r in RANKS:
        CARD_CACHE[(r, s)] = draw_card_surface(Card(r, s), True)
CARD_BACK = draw_card_surface(None, False)

# -----------------------------
# Chips rendering
# -----------------------------
CHIP_DENOMS = [1, 5, 25, 100, 500]
CHIP_COLORS = {1: (232, 232, 232), 5: (220, 70, 70), 25: (40, 150, 90), 100: (60, 100, 180), 500: (160, 80, 170)}


def draw_chip(value: int, scale=3) -> pygame.Surface:
    r = 12
    d = r*2
    surf = pygame.Surface((d, d), pygame.SRCALPHA)
    base = CHIP_COLORS.get(value, GOLD)
    pygame.draw.circle(surf, base, (r, r), r)
    pygame.draw.circle(surf, WHITE, (r, r), r-3, 2)
    # spokes
    for i in range(8):
        ang = i*math.pi/4
        x1 = r + int((r-2) * math.cos(ang))
        y1 = r + int((r-2) * math.sin(ang))
        x0 = r + int((r-7) * math.cos(ang))
        y0 = r + int((r-7) * math.sin(ang))
        pygame.draw.line(surf, WHITE, (x0, y0), (x1, y1), 2)
    # value text (pixel font)
    txt = str(value)
    w = len(txt) * 6
    blit_pix_text(surf, txt, (r - w//2, r-3), color=BLACK, scale=1)
    if scale != 1:
        surf = pygame.transform.scale(surf, (d*scale, d*scale))
    return surf

CHIP_SURF = {v: draw_chip(v, 4) for v in CHIP_DENOMS}

# -----------------------------
# Shoe / dealing logic
# -----------------------------

def build_shoe(decks=DECKS_IN_SHOE) -> List[Card]:
    cards = [Card(r, s) for s in SUITS for r in RANKS] * decks
    random.shuffle(cards)
    return cards


@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    bet: int = 0
    insurance: int = 0
    surrendered: bool = False
    doubled: bool = False

    def add(self, card: Card):
        self.cards.append(card)

    def values(self) -> Tuple[int, int]:
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank == 'A')
        soft_total = total
        while soft_total > 21 and aces:
            soft_total -= 10
            aces -= 1
        hard_total = soft_total
        return hard_total, total  # (best <=21 if possible, raw with Aces as 11)

    def best_total(self) -> int:
        hard, raw = self.values()
        return hard

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.best_total() == 21

    def is_bust(self) -> bool:
        return self.best_total() > 21

    def can_split(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def is_soft(self) -> bool:
        # soft if an Ace counted as 11 and total <= 21
        total = sum(11 if c.rank == 'A' else (10 if c.rank in 'JQK' else int(c.rank)) for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return any(c.rank == 'A' for c in self.cards) and total <= 21 and sum(1 for c in self.cards if c.rank == 'A') > 0 and (sum(1 for c in self.cards if c.rank == 'A') >= 1)


@dataclass
class Player:
    bank: int = 1000
    hands: List[Hand] = field(default_factory=list)
    active_index: int = 0

    def reset_round(self):
        self.hands = []
        self.active_index = 0

    def active_hand(self) -> Hand:
        return self.hands[self.active_index]


# -----------------------------
# Game State
# -----------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pixel Blackjack")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("couriernew", 18)
        self.bigfont = pygame.font.SysFont("couriernew", 28, bold=True)

        self.shoe: List[Card] = build_shoe()
        self.cut_index = int(len(self.shoe) * 0.25)  # reshuffle when reaching this index from end
        self.discard: List[Card] = []

        self.player = Player()
        self.dealer_hand = Hand()

        self.state = 'BETTING'  # BETTING -> DEALING -> PLAYER_TURN -> DEALER_TURN -> RESOLVE
        self.message = "Place your bet"
        self.bets_selection: List[int] = []

        self.buttons = {}
        self._build_buttons()

    # ------------------------- UI helpers ------------------------
    def _build_buttons(self):
        def rect(x, y, w, h):
            return pygame.Rect(x, y, w, h)

        self.buttons = {
            'deal': rect(880, 620, 160, 40),
            'hit': rect(40, 620, 120, 40),
            'stand': rect(170, 620, 120, 40),
            'double': rect(300, 620, 120, 40),
            'split': rect(430, 620, 120, 40),
            'surrender': rect(560, 620, 140, 40),
            'insure': rect(710, 620, 160, 40),
            'next': rect(880, 620, 160, 40),
        }

    def draw_button(self, key: str, label: str, enabled=True):
        r = self.buttons[key]
        col = GOLD if enabled else GREY
        pygame.draw.rect(self.screen, col, r, border_radius=14)
        pygame.draw.rect(self.screen, SHADOW, r, 2, border_radius=14)
        textsurf = self.bigfont.render(label, True, BLACK if enabled else (60,60,60))
        self.screen.blit(textsurf, (r.centerx - textsurf.get_width()//2, r.centery - textsurf.get_height()//2))

    # ------------------------- dealing helpers -------------------
    def draw_from_shoe(self) -> Card:
        if len(self.shoe) <= self.cut_index:
            # reshuffle
            self.shoe = build_shoe()
        return self.shoe.pop()

    # ------------------------- game phases -----------------------
    def start_round(self):
        bet = sum(self.bets_selection)
        if bet <= 0 or bet > self.player.bank:
            self.message = "Invalid bet"
            return
        self.player.bank -= bet
        self.player.reset_round()
        self.player.hands = [Hand(bet=bet)]
        self.dealer_hand = Hand()

        # initial deal
        for _ in range(2):
            self.player.hands[0].add(self.draw_from_shoe())
            self.dealer_hand.add(self.draw_from_shoe())
        self.state = 'PLAYER_TURN'
        self.message = "Your move"

    def offer_insurance(self) -> bool:
        return self.dealer_hand.cards and self.dealer_hand.cards[0].rank == 'A'

    def current_actions(self):
        h = self.player.active_hand()
        can_split = h.can_split() and len(self.player.hands) < MAX_SPLIT_HANDS and self.player.bank >= h.bet
        can_double = (len(h.cards) == 2) and (self.player.bank >= h.bet)
        can_surrender = (len(h.cards) == 2) and not h.doubled and not h.surrendered
        can_insure = self.offer_insurance() and h.insurance == 0 and self.player.bank >= h.bet//2
        return dict(split=can_split, double=can_double, surrender=can_surrender, insure=can_insure)

    def settle(self):
        # Check dealer blackjack if showing Ace or 10 and insurance placed
        dealer_blackjack = self.dealer_hand.is_blackjack()

        for idx, h in enumerate(self.player.hands):
            result = None

            if h.surrendered:
                # Half bet returned (player already took half loss when marking surrendered)
                result = ("Surrender", -h.bet//2)
            elif h.is_bust():
                result = ("Bust", -h.bet)
            elif dealer_blackjack and not h.is_blackjack():
                # dealer blackjack beats all except player's blackjack (which pushes)
                loss = -h.bet
                ins = 0
                if h.insurance:
                    # insurance pays 2:1
                    ins = h.insurance * 2
                result = ("Dealer blackjack", loss + ins)
            else:
                # normal compare; ensure dealer plays out if needed
                if not dealer_blackjack:
                    self.dealer_playout()
                dealer_total = self.dealer_hand.best_total()
                player_total = h.best_total()

                if h.is_blackjack() and not self.dealer_hand.is_blackjack():
                    win = h.bet * BLACKJACK_PAYS[0] // BLACKJACK_PAYS[1]
                    result = ("Blackjack!", win)
                elif self.dealer_hand.is_bust():
                    result = ("Dealer busts", h.bet)
                elif player_total > dealer_total:
                    result = ("Win", h.bet)
                elif player_total < dealer_total:
                    result = ("Lose", -h.bet)
                else:
                    result = ("Push", 0)

                if h.insurance and self.dealer_hand.is_blackjack():
                    # this path only occurs if dealer_blackjack True; already handled above, but keep safe
                    result = (result[0], result[1] + h.insurance*2)

            self.player.bank += h.bet + result[1]  # return original bet plus net

        self.state = 'RESOLVE'
        if self.dealer_hand.is_blackjack():
            self.message = "Dealer has Blackjack"
        elif self.dealer_hand.is_bust():
            self.message = "Dealer busts"
        else:
            self.message = "Round settled"

    def dealer_playout(self):
        # Reveal and play out to 17 (stand on soft 17 if configured)
        while True:
            total = self.dealer_hand.best_total()
            soft = self.is_soft_hand(self.dealer_hand)
            if total < 17:
                self.dealer_hand.add(self.draw_from_shoe())
            elif total == 17 and soft and not DEALER_STAND_SOFT_17:
                self.dealer_hand.add(self.draw_from_shoe())
            else:
                break

    @staticmethod
    def is_soft_hand(hand: Hand) -> bool:
        # same as Hand.is_soft but simpler, for dealer
        total = sum(11 if c.rank == 'A' else (10 if c.rank in 'JQK' else int(c.rank)) for c in hand.cards)
        aces = sum(1 for c in hand.cards if c.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        # soft if any ace still counted as 11
        return any(c.rank == 'A' for c in hand.cards) and total <= 21 and aces > 0

    # ------------------------- input handlers --------------------
    def on_click(self, pos):
        x, y = pos
        if self.state == 'BETTING':
            # chip clicks
            for i, val in enumerate(CHIP_DENOMS):
                chip_rect = pygame.Rect(40 + i*100, 540, 64, 64)
                if chip_rect.collidepoint(pos):
                    if self.player.bank >= val:
                        self.bets_selection.append(val)
                        self.message = f"Bet: ${sum(self.bets_selection)}"
                    return
            # deal button
            if self.buttons['deal'].collidepoint(pos):
                self.start_round()
                return
            # remove last chip if clicking total area
            total_rect = pygame.Rect(40, 500, 500, 32)
            if total_rect.collidepoint(pos) and self.bets_selection:
                self.player.bank += self.bets_selection.pop()
                self.message = f"Bet: ${sum(self.bets_selection)}"
                return
        elif self.state == 'PLAYER_TURN':
            h = self.player.active_hand()
            acts = self.current_actions()
            if self.buttons['hit'].collidepoint(pos):
                h.add(self.draw_from_shoe())
                if h.is_bust():
                    self.advance_hand_or_dealer()
                return
            if self.buttons['stand'].collidepoint(pos):
                self.advance_hand_or_dealer()
                return
            if self.buttons['double'].collidepoint(pos) and acts['double']:
                self.player.bank -= h.bet
                h.bet *= 2
                h.doubled = True
                h.add(self.draw_from_shoe())
                self.advance_hand_or_dealer()
                return
            if self.buttons['split'].collidepoint(pos) and acts['split']:
                # split into two hands
                self.player.bank -= h.bet
                c2 = h.cards.pop()
                new_hand = Hand(cards=[c2], bet=h.bet)
                # draw one new card to each split hand
                h.add(self.draw_from_shoe())
                new_hand.add(self.draw_from_shoe())
                self.player.hands.insert(self.player.active_index+1, new_hand)
                return
            if self.buttons['surrender'].collidepoint(pos) and acts['surrender']:
                h.surrendered = True
                # immediately settle this hand as half loss
                self.advance_hand_or_dealer()
                return
            if self.buttons['insure'].collidepoint(pos) and acts['insure']:
                amt = min(h.bet//2, self.player.bank)
                self.player.bank -= amt
                h.insurance = amt
                self.message = f"Insurance placed: ${amt}"
                return
        elif self.state == 'RESOLVE':
            if self.buttons['next'].collidepoint(pos):
                self.message = "Place your bet"
                self.state = 'BETTING'
                self.bets_selection = []
                self.player.reset_round()
                self.dealer_hand = Hand()
                return

    def advance_hand_or_dealer(self):
        # move to next hand or dealer turn/settle
        h = self.player.active_hand()
        if h.is_bust():
            self.message = "Bust!"
        if self.player.active_index < len(self.player.hands) - 1:
            self.player.active_index += 1
            self.message = "Next hand"
        else:
            # dealer turn & settle
            self.state = 'DEALER_TURN'
            self.dealer_playout()
            self.settle()

    # ------------------------- drawing ---------------------------
    def draw_table(self):
        self.screen.fill(TABLE_GREEN)
        # title
        title = self.bigfont.render("PIXEL BLACKJACK", True, WHITE)
        self.screen.blit(title, (40, 24))
        # bank
        bank = self.bigfont.render(f"Bank: ${self.player.bank}", True, WHITE)
        self.screen.blit(bank, (SCREEN_W - bank.get_width() - 40, 24))

        # center banners
        msg = self.bigfont.render(self.message, True, WHITE)
        self.screen.blit(msg, (40, 70))

    def draw_betting_ui(self):
        # chips
        for i, val in enumerate(CHIP_DENOMS):
            chip = CHIP_SURF[val]
            x = 40 + i*100
            y = 540
            self.screen.blit(chip, (x, y))
            lbl = self.font.render(f"${val}", True, WHITE)
            self.screen.blit(lbl, (x + chip.get_width()//2 - lbl.get_width()//2, y + 66))

        total = sum(self.bets_selection)
        # stacked chips preview
        x0, y0 = 600, 540
        for i, val in enumerate(self.bets_selection[-10:]):  # show last 10 chips stacked
            self.screen.blit(CHIP_SURF[val], (x0 + i*10, y0 - i*6))
        # total label
        pygame.draw.rect(self.screen, (0,0,0,80), (40, 500, 500, 32))
        t = self.font.render(f"Click chips to bet — Total: ${total} (click here to remove last)", True, WHITE)
        self.screen.blit(t, (48, 504))

        # deal button
        self.draw_button('deal', 'DEAL', enabled=total>0 and total<=self.player.bank+total)

    def draw_hands(self):
        # dealer row
        self._draw_hand(self.dealer_hand, origin=(60, 150), face_down_first=(self.state in ('PLAYER_TURN') and not self.dealer_hand.is_blackjack()))

        # player hands
        for i, h in enumerate(self.player.hands):
            x = 60 + i * 240
            y = 360
            active = (i == self.player.active_index and self.state == 'PLAYER_TURN')
            self._draw_hand(h, origin=(x, y), face_down_first=False, highlight=active)
            # bet/chips indicator
            betlbl = self.font.render(f"Bet ${h.bet}" + (" (Doubled)" if h.doubled else "") + (" (Surr)" if h.surrendered else ""), True, WHITE)
            self.screen.blit(betlbl, (x, y - 28))
            if h.insurance:
                inslbl = self.font.render(f"Insurance ${h.insurance}", True, GOLD)
                self.screen.blit(inslbl, (x, y - 52))

    def _draw_hand(self, hand: Hand, origin=(60, 360), face_down_first=False, highlight=False):
        x, y = origin
        for idx, c in enumerate(hand.cards):
            face_up = not (face_down_first and idx == 0)
            surf = CARD_CACHE[(c.rank, c.suit)] if face_up else CARD_BACK
            self.screen.blit(surf, (x + idx*40, y))
        # total bubble
        tot = hand.best_total()
        col = GOLD if highlight else WHITE
        bubble = self.font.render(f"{tot}", True, col)
        self.screen.blit(bubble, (x, y + CARD_H*CARD_SCALE + 8))

    def draw_action_bar(self):
        if self.state == 'BETTING':
            self.draw_betting_ui()
            return
        if self.state in ('PLAYER_TURN',):
            acts = self.current_actions()
            self.draw_button('hit', 'HIT', True)
            self.draw_button('stand', 'STAND', True)
            self.draw_button('double', 'DOUBLE', acts['double'])
            self.draw_button('split', 'SPLIT', acts['split'])
            self.draw_button('surrender', 'SURRENDER', acts['surrender'])
            self.draw_button('insure', 'INSURE', acts['insure'])
        elif self.state == 'RESOLVE':
            self.draw_button('next', 'NEXT ROUND', True)
        else:
            # during dealer turn, no buttons
            pass

    # ------------------------- main loop -------------------------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click(event.pos)

            self.draw_table()
            self.draw_hands()
            self.draw_action_bar()

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    Game().run()

'''Date: 2019-07-26
    Author: James Wang with help from Shawn Song
    Thanks to shawn for lending his laptop and play testing
    Description: big chungus
    4 days for game logic
    another 3 for extra features
'''

# Import/Initialize
import math
import random
import pygame
pygame.init()

# Constants
SQUARE_SIZE = 25
GRID_WIDTH = SQUARE_SIZE * 10 + 11
GRID_HEIGHT = SQUARE_SIZE * 22 + 23
GRID_SIZE = (GRID_WIDTH, GRID_HEIGHT)

# Hold piece border
ICON_BACK = pygame.Surface((117,117))
ICON_BACK.fill((255,255,255))
BACK = pygame.Surface((109,109))
BACK.fill((0,0,0))
ICON_BACK.blit(BACK, (4,4))

# Colours
COLOURS = [(0, 0,255),(138,43,226),(255,140,0), (0,191,255), (94, 247, 47), (255,0,0), (255,255,0)]

#  Display
SCREEN = pygame.display.set_mode((480,GRID_HEIGHT+20))
pygame.display.set_caption("Tetros")

BACKGROUND = pygame.Surface(SCREEN.get_size())
BACKGROUND.fill((0,0,0))

START_SCREEN = pygame.image.load('tetros.png')

CLOCK = pygame.time.Clock()
VOLUME = 0.25

exit_program = False

#######################################################################################################
# Classes                                                                                             #
#######################################################################################################

class Grid(pygame.sprite.Sprite):
    '''Grid class. Just a picture of the grid, no functional use'''
    def __init__(self):
        '''Initializer method. Takes no parameters, draws the grid on a surface.'''
        pygame.sprite.Sprite.__init__(self)
        self.grid = pygame.Surface(GRID_SIZE)
        self.image = pygame.Surface((GRID_WIDTH+20,GRID_HEIGHT+20))
        self.image.fill((255,255,255))
        for i in range(0,GRID_WIDTH,SQUARE_SIZE+1):
            pygame.draw.line(self.grid,(255,255,255), (i,0),(i,GRID_HEIGHT),1)
        pygame.draw.line(self.grid,(255,255,255), (GRID_WIDTH,0),(GRID_WIDTH, GRID_HEIGHT),1)
        for i in range(0,GRID_HEIGHT,SQUARE_SIZE+1):
            pygame.draw.line(self.grid,(255,255,255), (0,i),(GRID_HEIGHT,i),1)
        pygame.draw.line(self.grid,(255,255,255), (0,GRID_HEIGHT),(GRID_WIDTH,GRID_HEIGHT),1)
        self.image.blit(self.grid,(10,10))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        

class Square(pygame.sprite.Sprite):
    '''Square class. Takes a coordinate and coordinate relative to the center of the block'''
    def __init__(self, coordinates, relative_cord, colour):
        pygame.sprite.Sprite.__init__(self)
        self.cord = coordinates.copy()
        self.og_cords = (coordinates.copy(), relative_cord.copy())
        self.image = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.relative_cord = relative_cord.copy()
        self.death_count = -1

    def fall(self):
        self.cord[1] += 1

    def rotate(self):
        new_rel_cord = [-self.relative_cord[1],self.relative_cord[0]]
        self.cord[0] -= self.relative_cord[0] - new_rel_cord[0]
        self.cord[1] -= self.relative_cord[1] - new_rel_cord[1]
        self.relative_cord = new_rel_cord

    def rotate_back(self):
        new_rel_cord = [self.relative_cord[1],-self.relative_cord[0]]
        self.cord[0] -= self.relative_cord[0] - new_rel_cord[0]
        self.cord[1] -= self.relative_cord[1] - new_rel_cord[1]
        self.relative_cord = new_rel_cord
        
    def move_right(self):
        self.cord[0] += 1

    def move_left(self):
        self.cord[0] -= 1

    def game_over(self, count):
        self.death_count = count + 15
        
    def update(self):
        self.rect.topleft = self.cord[0] * 26 + 11 , self.cord[1] * 26 + 11
        if self.death_count > 0:
            self.death_count -= 1
            if self.death_count == 15:
                self.image.fill((255,255,255))
        elif not self.death_count:
            self.kill()
            

class Dead_squares(pygame.sprite.Sprite):
    '''Dead_square class. Just a set of lists'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.squares = []
        self.cords = []

    def add_squares(self,squares):
        for square in squares:
            self.squares.append(square)
            self.cords.append(square.cord)

    def clear_rows(self, rows):
        rows.sort()
        kill_squares = []
        for square in self.squares:
            if square.cord[1] in rows:
                square.kill()
                kill_squares.append(square)
                try:
                    self.cords.remove(square.cord)
                except ValueError:
                    pass
        for row in rows:
            for square in self.squares:
                if square.cord[1] < row:
                    square.fall()
        for square in kill_squares:
            self.squares.remove(square)

    def game_over(self):
        for square in self.squares:
            square.game_over(self.squares.index(square)*3)
        self.end_tick = len(self.squares)*3+15

    def update(self):
        if self.end_tick > 0:
            self.end_tick -= 1
        elif not self.end_tick:
            self.squares = False
            
#######################################################################################################
# Blocks                                                                                              #
#######################################################################################################

class Block(pygame.sprite.Sprite):
    '''Block class. No image.'''
    def __init__(self, _id_):
        pygame.sprite.Sprite.__init__(self)
        self.block_id = _id_
        self.colour = COLOURS[self.block_id]
            
    def add_squares(self, squares):
        self.squares = squares

    def fall(self):
        in_ground = False
        for square in self.squares:
            square.fall()
            if square.cord[1] >= 22: in_ground = True
        if in_ground:
            for square in self.squares:
                square.cord[1] -= 1

    def move_L_R(self,is_left):
        if is_left:
            for square in self.squares:
                 square.move_left()
        else:
            for square in self.squares:
                 square.move_right()

    def rotate(self):
        for square in self.squares:
            square.rotate()

    def rotate_back(self):
        for square in self.squares:
            square.rotate_back()

    def set_og_cords(self):
        for square in self.squares:
            square.cord = square.og_cords[0]
            square.relative_cord = square.og_cords[1]
            
    def get_cords(self):
        cords = []
        for square in self.squares:
            cords.append(square.cord)
        return cords


class L(Block):
    '''L class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 0)
        self.shape = [[1,1],
                      [0,1],
                      [0,1]]
        self.relative_cords = [[1,1],[0,1],[0,0],[0,-1]]


class T(Block):
    '''T class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 1)
        self.shape = [[1,1,1],
                      [0,1,0]]
        self.relative_cords = [[1,0],[0,0],[-1,0],[0,-1]]


class J(Block):
    '''J class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 2)
        self.shape = [[0,1,1],
                      [0,1,0],
                      [0,1,0]]
        self.relative_cords = [[0,1],[-1,1],[0,0],[0,-1]]


class I(Block):
    '''I class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 3)
        self.shape = [[0,1],
                      [0,1],
                      [0,1],
                      [0,1]]
        self.relative_cords = [[0,2],[0,1],[0,0],[0,-1]]

        
class S(Block):
    '''S class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 4)
        self.shape = [[0,1,1],
                      [1,1,0]]
        self.relative_cords = [[0,1],[-1,1],[1,0],[0,0]]


class Z(Block):
    '''Z class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 5)
        self.shape = [[1,1,0],
                      [0,1,1]]
        self.relative_cords = [[1,1],[0,1],[0,0],[-1,0]]


class O(Block):
    '''O class, a subclass of Block, no image'''
    def __init__(self):
        Block.__init__(self, 6)
        self.shape = [[1,1],
                      [1,1]]
        self.relative_cords = [[0,1],[-1,1],[0,0],[-1,0]]
        
    def rotate(self):
        pass

    def rotate_back(self):
        pass

#######################################################################################################
# Scoreboard, hold block                                                                              #
#######################################################################################################

class Scorekeeper(pygame.sprite.Sprite):
    '''Scorekeeper class, displays the score and level'''
    def __init__(self, level = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200,240))
        self.score = 0
        self.level = level
        self.lines = 0
        self.font = pygame.font.SysFont('Century Gothic', 25)
        self.big_font = pygame.font.SysFont('Century Gothic', 35)
        self.text_score = self.font.render('SCORE', True, (255,255,255))
        self.text_level = self.font.render('LEVEL', True, (255,255,255))
        self.text_lines = self.font.render('LINES', True, (255,255,255))
        self.refresh()
        self.rect = self.image.get_rect()
        self.rect.right = 480
        self.rect.bottom = GRID_HEIGHT + 20

    def refresh(self):
        self.image.fill((0,0,0))
        self.score_text = self.big_font.render(str(self.score), True, (255,255,255))
        self.level_text = self.big_font.render(str(self.level), True, (255,255,255))
        self.line_text = self.big_font.render(str(self.lines), True, (255,255,255))
        self.image.blit(self.text_level, (195-self.text_level.get_width(), 5))
        self.image.blit(self.level_text, (195-self.level_text.get_width(), 35))
        self.image.blit(self.text_lines, (195-self.text_lines.get_width(), 80))
        self.image.blit(self.line_text, (195-self.line_text.get_width(), 115))
        self.image.blit(self.text_score, (195-self.text_score.get_width(), 160))
        self.image.blit(self.score_text, (195-self.score_text.get_width(), 195))

    def add_score(self, score):
        self.score += self.level * score
        self.refresh()

    def add_line(self, lines):
        self.lines += lines
        self.refresh()

    def level_up(self):
        self.level += 1
        self.refresh()


class Next_block(pygame.sprite.Sprite):
    def __init__(self, block):
        pygame.sprite.Sprite.__init__(self)
        self.block = block
        self.image = ICON_BACK.copy()
        self.change_block(block)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH + 30, 10)

    def change_block(self, block):
        self.block = block
        self.image.blit(BACK, (4,4))
        if not self.block.block_id: x,y = 0,1
        elif self.block.block_id in [1,2,3]: x,y = 1,1
        elif self.block.block_id in [4,5,6]: x,y = 1,0
        for square in self.block.squares:
            self.image.blit(square.image, ((square.relative_cord[0]+x) * 26 + 5, (square.relative_cord[1]+y) * 26 + 5))


class Hold_block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ICON_BACK.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH + 30, 250)

    def change_block(self, block):
        self.block = block
        self.block.set_og_cords()
        self.image.blit(BACK, (4,4))
        for square in self.block.squares:
            self.image.blit(square.image, ((square.relative_cord[0]+1) * 26 + 5, (square.relative_cord[1]+1) * 26 + 5))    
        
# buttons #############################################################################################

class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.select = False

    def update(self):
        if self.select:
            self.image, self.select = self.image1, False
        else:
            self.image = self.image0


class Cursor(Button):
    def __init__(self):
        self.image0 = pygame.image.load("c1_blue.png")
        Button.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Play(Button):
    def __init__(self):
        self.image0, self.image1 = pygame.image.load("play.png"), pygame.image.load("hi_play.png")
        Button.__init__(self)
        self.rect.center = (SCREEN.get_width()//2, 200)


class VolSlider(pygame.sprite.Sprite):
    def __init__(self, vol):
        pygame.sprite.Sprite.__init__(self)
        self.vol = vol
        self.image = pygame.Surface((20, 316))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.slider = pygame.Surface((10, 200))
        self.slider.fill((100, 100, 100))
        self.select = False
        self.level = pygame.image.load("speaker.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN.get_width()//2, 450)

    def setVol(self):
        x, y = pygame.mouse.get_pos()
        if y in range(350, 550):
            self.vol = (550 - y) / 200
        elif y < 350:
            self.vol = 1.0
        elif y > 550:
            self.vol = 0
        return self.vol

    def update(self):
        self.volIndicator = pygame.Surface((10, self.vol * 200))
        self.volIndicator.fill((0, 255, 255))
        self.image.blit(self.slider, (5, 58))
        self.image.blit(self.volIndicator, (5, 58 + 200 - (self.vol * 200)))
        self.image.blit(self.level, (4, 281))
        self.mask = pygame.mask.from_surface(self.image)
#######################################################################################################
# Game Code                                                                                           #
#######################################################################################################

def game():
    SCREEN.blit(BACKGROUND, (0,0))
    # Entities
    dead_squares = Dead_squares()
    grid = Grid()
    block = get_block()
    hold_block = Hold_block()
    next_block = Next_block(get_block())
    scoreKeeper = Scorekeeper()
    allSprites = pygame.sprite.OrderedUpdates(scoreKeeper, grid, block.squares, next_block, hold_block)
    
    # Assign
    global exit_program
    fall_tick = 50
    score = 0
    tick = 0
    run = True
    no_tick = False
    set_tick = -1
    block_count = 0
    can_hold = True
    game_over = False

    # Main game loop
    while run and not exit_program:
        # Game tick
        CLOCK.tick(120)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    if check_rotate(dead_squares.cords, block):
                        block.rotate()
                elif event.key == pygame.K_DOWN:
                    if check_fall(dead_squares.cords, block):
                        block.fall()
                        tick = 0
                elif event.key == pygame.K_RIGHT:
                    if check_move_right(dead_squares.cords, block):
                        block.move_L_R(False)
                elif event.key == pygame.K_LEFT:
                    if check_move_left(dead_squares.cords, block):
                        block.move_L_R(True)
                elif event.key == pygame.K_SPACE:
                    if check_fall(dead_squares.cords, block):
                        scoreKeeper.add_score(40)
                        while check_fall(dead_squares.cords, block):
                            block.fall()
                            set_tick = 0
                        no_tick = True
                elif event.key == pygame.K_c and can_hold:
                    try:
                        new_block = hold_block.block
                    except AttributeError:
                        new_block = next_block.block
                        next_block.change_block(get_block())
                    for square in block.squares:
                        square.kill()
                    hold_block.change_block(block)
                    block = new_block
                    can_hold = False
                    allSprites.add(block.squares)
                elif event.key in [pygame.K_p, pygame.K_ESCAPE]:
                    pause()
                    
        # Piece falling and row clearing
        if not game_over:
            if tick < fall_tick: tick += 1
            elif tick == fall_tick:
                if set_tick == -1 and not no_tick:
                    if check_fall(dead_squares.cords, block):
                        block.fall()
                    else:
                        set_tick = 40
                    tick = 0

            if set_tick > 0:
                set_tick -= 1
                if check_fall(dead_squares.cords, block):
                    set_tick = -1
            elif not set_tick and not check_fall(dead_squares.cords, block):    # row clearing
                dead_squares.add_squares(block.squares)
                full_rows = (check_clear(dead_squares.cords, block))
                dead_squares.clear_rows(full_rows)
                scoreKeeper.add_score(100*int(len(full_rows)**1.2))
                scoreKeeper.add_line(len(full_rows))
                block = next_block.block
                next_block.change_block(get_block())
                can_hold = True
                allSprites.add(block.squares)
                if check_dead(dead_squares.cords, block):
                    set_tick = 40
                    dead_squares.add_squares(block.squares)
                    dead_squares.add_squares(next_block.block.squares)
                    try:
                        dead_squares.add_squares(hold_block.block.squares)
                    except AttributeError:
                        pass
                    dead_squares.game_over()
                    game_over = True
                    tick = fall_tick + 1
                    set_tick = -1
                else:
                    block_count += 1
                    if block_count == 7:
                        block_count = 0
                        scoreKeeper.level_up()
                        if fall_tick > 1: fall_tick -= 1
                set_tick = -1
                no_tick = False
                tick = -10
            else:
                set_tick = -1
        else:
            dead_squares.update()
            if dead_squares.squares == False:
                run = False
                
        # Refresh the screen
        allSprites.clear(SCREEN, BACKGROUND)
        allSprites.update()
        allSprites.draw(SCREEN)
        pygame.display.flip()
    return scoreKeeper.score

# Spawning blocks #####################################################################################

def get_block():
    '''returns a random block'''
    block_num = random.randrange(7)
    centerx = 4
    centery = 1
    if not block_num: block = L()
    elif block_num == 1: block = T()
    elif block_num == 2: block, centerx = J(), 5
    elif block_num == 3: block, centerx = I(), 5
    elif block_num == 4: block, centery = S(), 0
    elif block_num == 5: block, centery = Z(), 0
    elif block_num == 6: block, centerx, centery = O(), 5,0
    squares = []
    for y in range(len(block.shape)):
        for x in range(len(block.shape[y])):
            if block.shape[y][x] != 0:
                cords = block.relative_cords[len(squares)]
                squares.append(Square([centerx + cords[0], centery + cords[1]], cords,block.colour))
    block.add_squares(squares)
    return block

# Checking movement ###################################################################################

def check_fall(dead_square_cords, block):
    '''Checks if the block can fall down'''
    can_fall = True
    for square in block.squares:
        square.cord[1] += 1
    for square in block.squares:
        if square.cord in dead_square_cords or square.cord[1] == 22:
            can_fall = False
    for square in block.squares:
        square.cord[1] -= 1
    return can_fall


def check_move_right(dead_square_cords, block):
    '''Checks if the block can move right'''
    can_move = True
    for square in block.squares:
        square.cord[0] += 1
    for square in block.squares:
        if square.cord in dead_square_cords or square.cord[0] == 10:
            can_move = False
    for square in block.squares:
        square.cord[0] -= 1
    return can_move


def check_move_left(dead_square_cords, block):
    '''Checks if the block can move right'''
    can_move = True
    for square in block.squares:
        square.cord[0] -= 1
    for square in block.squares:
        if (square.cord in dead_square_cords) or square.cord[0] <= -1:
            can_move = False
    for square in block.squares:
        square.cord[0] += 1
    return can_move


def check_rotate(dead_square_cords, block):
    '''Checks if the block can rotate, and moves it over so it can turn if possible'''
    can_rotate = True
    block.rotate()
    for square in block.squares:
        if (square.cord in dead_square_cords) or square.cord[0] <= -1 or square.cord[0] >= 10 or square.cord[1] >= 22:
            can_rotate = False
            for i in range(2):
                if square.cord[0] <= -1:
                    block.move_L_R(False)
                    can_rotate = True
                elif square.cord[0] >= 10:
                    block.move_L_R(True)
                    can_rotate = True
            
    block.rotate_back() 
    return can_rotate


def check_clear(dead_square_cords, block):
    '''checks if there is a row to clear'''
    rows = []
    y_cords = []
    clear_rows = []
    for square in block.squares:
        if square.cord[1] not in rows:
            rows.append(square.cord[1])
    for cord in dead_square_cords:
        y_cords.append(cord[1])
    for row in rows:
        if y_cords.count(row) == 10:
            clear_rows.append(row)
    return clear_rows

def check_dead(dead_square_cords, block):
    dead = False
    for square in block.squares:
        if square.cord in dead_square_cords:
            dead = True
    return dead

#######################################################################################################
# menu, pause, start, options                                                                         #
#######################################################################################################

def menu():
    global exit_program
    global VOLUME
    highscore = 0

    volSlider = VolSlider(VOLUME)
    playButton = Play()
    buttons = [volSlider, playButton]
    cursor = Cursor()
    SCREEN.blit(START_SCREEN,(0,0))

    allSprites = pygame.sprite.OrderedUpdates(volSlider, playButton, cursor)
    while not exit_program:
        CLOCK.tick(30)

        hit = pygame.sprite.spritecollide(cursor, buttons, False, pygame.sprite.collide_mask)
        for button in hit:
            button.select = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.select:
                    playButton.select = False
                    score = game()
                    SCREEN.fill((0,0,0))
                    if score > highscore:
                        highscore = score

        if any(pygame.mouse.get_pressed()):
            if volSlider.select:
                VOLUME = volSlider.setVol()
                pygame.mixer.music.set_volume(VOLUME)

        allSprites.clear(SCREEN, START_SCREEN)
        allSprites.update()
        allSprites.draw(SCREEN)
        pygame.display.flip()
    return


def start():
    global exit_program
    font = pygame.font.SysFont('Century Gothic', 30)
    text = font.render('PRESS ANYTHING TO START', True, (255,255,255))
    tick = 0
    pygame.mouse.set_visible(False)
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(VOLUME)
    pygame.mixer.music.play(-1)

    while not exit_program:
        CLOCK.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                SCREEN.blit(BACKGROUND, (0,0))
                return
        
        tick += 1
        if tick == 10:
            SCREEN.blit(text, ((SCREEN.get_width() - text.get_width())//2,(SCREEN.get_height() - text.get_height())//2))
        elif tick == 25:
            SCREEN.blit(START_SCREEN, (0,0))
            tick = 0

        pygame.display.flip()

def pause():
    global exit_program
    pause = True
    SCREEN.blit(BACKGROUND,(0,0))
    while pause and not exit_program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False
        pygame.display.flip()

def main():
    while not exit_program:
        start()
        menu()
    pygame.quit()

main()

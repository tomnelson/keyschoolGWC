import math
import os
from PIL import Image, ImageTk
import codesters
stage = codesters.Environment()

# Written by Tom Nelson
#field = codesters.Rectangle(0,0,500,500,"black")
tie_image = "http://tomnelson.github.io/keyschoolGWC/tie-fighter.jpg"
xwing_image="http://tomnelson.github.io/keyschoolGWC/x-wing.gif"
#tie_image = "./tie-fighter.jpg"
#xwing_image="./x-wing.gif"

stage.set_background("space")
instructions = []
inst_text = []
instructions.append("Use the mouse to control the xwing")
instructions.append("Use the 's' key to shoot")
instructions.append("The 'a' key raises shields")
instructions.append("Watch out for attackers!")
instructions.append("1 point for hitting tie fighter in formation")
instructions.append("5 points for hitting attacking tie fighter")
offset = 40
for inst in instructions:
    inst_text.append(codesters.Text(inst, 0, offset, "red"))
    offset -= 20

def clear_instructions():
    for text in inst_text:
        stage.remove_sprite(text)
# you get 1 point for hitting a tie fighter in formation
# and 5 points for hitting one while it is attacking
score = 0
stage.disable_all_walls()
xwing_count = 3

# vector functions
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def mul(u, m):
    return [ u[i]*m for i in range(len(u)) ]

def div(u, d):
    return [ u[i]/d for i in range(len(u)) ]

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    if vmag == 0:
        return [0,0]
    return [ v[i]/vmag  for i in range(len(v)) ]


class Player(codesters.Circle):
    
    def __init__(self, p, v, diam, color):
        codesters.Circle.__init__(self, p[0], p[1], diam, color)
        self.set_x_speed(v[0])
        self.set_y_speed(v[1])
        self.headingAngle = normalize(v)
        

    # the position as a vector
    def getPos(self):
        return [self.get_x(),self.get_y()]
    
    # the actual velocity
    def getVelocity(self):
        return [self.get_x_speed(),self.get_y_speed()]
    
    # a normalized vector of the velocity
    def getHeading(self):
        return self.headingAngle
    
    def setVelocity(self,v):
        self.set_x_speed(v[0])
        self.set_y_speed(v[1])
        self.headingAngle = normalize(v)
        

    def __str__(self):
        return "Player pos:"+str(self.getPos())+" velocity:"+str(self.getVelocity())

# Shot is a subclass of Player and includes a reference to the
# target of the Shot
class Shot(Player):
    def __init__(self, p, v, target, diam, color):
        Player.__init__(self, p, v, diam, color)
        self.target = target
        self.tracking_limit = math.pi/12
        

    def getTarget(self):
        return self.target
        
    def getAngleToTarget(self):
        ap = self.getPos()
        # target position
        tp = self.target.getPos()
        # vector from attacker to target
        v = sub(tp, ap)
        # normalize v so it is length 1
        n = normalize(v)
        return angle_between_normalized(self.getHeading(), n)

    def adjust(self):
        ap = self.getPos()
        # target position
        tp = self.getTarget().getPos()
        # vector from attacker to target
        v = sub(tp, ap)
        if magSq(v) == 0:
            remove_shot(self)
        # normalize v so it is length 1
        # I do this because I want every shot to go the same
        # speed no matter how close or far the target is.
        n = normalize(v)
        anglebet = self.getAngleToTarget()
        # set the speed of the shot using the power of the shot
        # This makes the shot go towards the target
        if anglebet < self.tracking_limit:
            # multiplied by 5 (power of the shot as a vector)
            p = mul(n, 5)
            self.setVelocity(p)
        else:
            self.set_color("orange")
    
    def __str__(self):
        return str(self.getPos())+":"+str(self.getVelocity())

class Fighter(codesters.Sprite):
    
    def __init__(self, image, p, v, size):
       # self.photo = Image.open(image)
       # self.base_photo = Image.open(image)
        codesters.Sprite.__init__(self, image, p[0], p[1])
        self.set_x_speed(v[0])
        self.set_y_speed(v[1])
        self.set_size(size)
        self.headingAngle = normalize(v)
        self.target = None
        self.home = p
        self.alive = True
#        self.photo = Image.open(image)
        
    def isAlive(self):
        return self.alive
        
    def setAlive(self, alive):
        self.alive = alive
        
    # the position as a vector
    def getPos(self):
        return [self.get_x(),self.get_y()]
    
    def glideTo(self, p):
        self.glide_to(p[0],p[1])
        
    def goHome(self):
        self.glideTo(self.home)
        
    def setPos(self, v):
        self.set_x(v[0])
        self.set_y(v[1])
    # the actual velocity
    def getVelocity(self):
        return [self.get_x_speed(),self.get_y_speed()]
    
    # a normalized vector of the velocity
    def getHeading(self):
        return self.headingAngle
    
    def setVelocity(self,v):
        self.set_x_speed(v[0])
        self.set_y_speed(v[1])
        self.headingAngle = normalize(v)
        
    def setTarget(self, target):
        self.target = target
        
    def getTarget(self):
        return self.target
        
    def attack(self, target):
        if target != None and target != 0:
            p = self.getPos()
            tp = target.getPos()
            v = mul(normalize(sub(tp,p)),6)
            self.setVelocity(v)
            
        
    def shoot(self, target, collision):
        # don't shoot at myself!
        if self != target and target != None and target != 0:
            self.set_color("blue")
            # attacker position
            ap = self.getPos()
            # target position
            tp = target.getPos()
            # vector from attacker to target
            v = sub(tp, ap)
            # normalize v so it is length 1
            # I do this because I want every shot to go the same
            # speed no matter how close or far the target is.
            n = normalize(v)
            # multiplied by 10 (power of the shot as a vector)
            p = mul(n, 10)
            # On extra step....
            # Move the shot start position 15 away from where it
            # was, because if the shot starts at the center of the
            # shooter, I will get a collision event as soon as the
            # shot is created, like it collided with the shooter!
            # You may need to make it larger than 15, depending on 
            # the size of your shooter sprite
            sp = add(ap, mul(n, 15))
            # make a shot starting at the offset position
            shot = Shot(sp, p, target, 5, "yellow")
            # register a collision listener for the shot
            shot.event_collision(collision)
    
    def __str__(self):
        return "Player pos:"+str(self.getPos())+" velocity:"+str(self.getVelocity())


# Increment forever_counter every time the iterval function is
# called (once per second). If I check it like this:
# if forever_counter % 5 == 0:
# then I can do something once every 5 seconds
# if forever_counter % 10 == 0:
# would do something once every 10 seconds
forever_counter = 0
# this is set to the tie fighter that is attacking, or
# 0 when none is attacking
# ox and oy are the original position of the attacking
# tie fighter. They are saved so that the tie fighter can
# return to its original place in the formation after attacking
tie_fighters = []

# make 4 'walls' around the field, so that when sprites/shapes
# collide with them (and are no longer visible), I can remove
# them from the stage, or return them to base.
north_wall = codesters.Rectangle(0, 260, 500, 40)
south_wall = codesters.Rectangle(0,-260, 500, 40)
east_wall = codesters.Rectangle(260, 0 , 40, 500)
west_wall = codesters.Rectangle(-260, 0, 40, 500)

def loser():
    text = codesters.Text("GAME OVER! score:"+str(score),0,0,"red")

def winner():
    text = codesters.Text("WINNER! score:"+str(score),0,0,"red")

def make_xwing():
    # image for the xwing
    global xwing_count
    xwing_count -= 1
    if xwing_count < 0:
        loser()
        return None
    xwing = Fighter(xwing_image, [0, -200], [0,0], 0.5)
    return xwing

xwing = make_xwing()
shield = None

def remove_shield():
    global shield
    if shield != None:
        stage.remove_sprite(shield)
        shield = None

def collision_for_tie_fighter(sprite, hit_sprite):
#    global attacking_tie_fighter
    global xwing
    # if the tie fighter hits a wall (east, west, south) return
    # it to base formation
    if hit_sprite == east_wall or hit_sprite == west_wall or hit_sprite == south_wall:
        sprite.go_to(0, 300)
        sprite.goHome()
    
    if hit_sprite == shield:
        remove_shield()
        stage.remove_sprite(sprite)
    # if the tie fighter hits the xwing, both are destroyed
    if hit_sprite == xwing:
        xwing = None
        stage.remove_sprite(hit_sprite)
        stage.remove_sprite(sprite)
        hit_sprite.setAlive(False)

def make_tie_fighters(rows, cols):
    x = -200
    y = 220
    for count in range(rows):
        x = -200
        for count in range(cols):
            tie = Fighter(tie_image,[x, y],[0,0],1)
            tie.event_collision(collision_for_tie_fighter)
            tie_fighters.append(tie)
            x += 66
        y -= 27

make_tie_fighters(5, 7)

# control the position of the xwing with the mouse
def mouse_move():
    if xwing != None and xwing != 0:
        xwing.set_position(stage.mouse_x(),xwing.get_y())
    if shield != None and xwing != None and xwing != 0:
        shield.set_position(stage.mouse_x(),xwing.get_y())

stage.event_mouse_move(mouse_move)

# collision between a shot from a tie fighter and the xwing
def collision_for_tiefighter_shot(sprite, hit_sprite):
    global xwing
    # if the shot hit the south wall, remove the shot to save memory
    if hit_sprite == south_wall:
        stage.remove_sprite(sprite)
    if hit_sprite == shield:
        remove_shield()
        stage.remove_sprite(sprite)
    # if the shot hit the xwing, remove both
    if hit_sprite == xwing:
        stage.remove_sprite(hit_sprite)
        stage.remove_sprite(sprite)
        hit_sprite.setAlive(False)
        # this will let the game try to make a new xwing
        xwing = None

# 's' key makes the xwing shoot at the tie fighters
def s_key():
    # if there is no xwing, there are no shots!
    if xwing != None:
        # make the shot, firing upwards from the xwing
        shot = codesters.Ellipse(xwing.get_x(), xwing.get_y(), 5, 10, "orange")
        shot.set_y_speed(10)
        shot.set_x_speed(0)
        shot.event_collision(collision_for_xwing_shot)

def a_key():
    global shield
    if shield == None and xwing != None:
        shield = codesters.Circle(xwing.get_x(), xwing.get_y(), 100, None, "yellow")
# collision of a shot from the xwing with a tie fighter
def collision_for_xwing_shot(sprite, hit_sprite):
    global xwing
    global score
    # If the shot hit the north wall, remove it to save memory
    if hit_sprite == north_wall:
        stage.remove_sprite(sprite)

    # if the shot hit a tie fighter, remove both and adjust score
    if hit_sprite in tie_fighters:
        # the shot hit a tie fighter, remove both
        stage.remove_sprite(hit_sprite)
        stage.remove_sprite(sprite)
        hit_sprite.setAlive(False)
        # you get another 4 points if you hit the attacking tie fighter
        if hit_sprite.getTarget() != None:
            score += 4

        # you get 1 point for hitting a tie fighter in formation
        score += 1
        tie_fighters.remove(hit_sprite)
        if len(tie_fighters) == 0:
            # there are no more tie fighters left, you win
            winner()


def interval():
    global forever_counter
    forever_counter += 1
    global xwing

    # every 5 seconds, see if we need a new xwing  
    if forever_counter % 5 != 0 and xwing == None:
        xwing = make_xwing()
    
    # send out a tie fighter once every 2 to 5 seconds
    if forever_counter % random.randint(2,5) == 0:
        clear_instructions()
        remove_shield()
        if len(tie_fighters) > 0:
            attacker = random.choice(tie_fighters)
            attacker.attack(xwing)
            attacker.shoot(xwing,collision_for_tiefighter_shot)


stage.event_key("s", s_key)
stage.event_key("a", a_key)
stage.event_interval(interval, 1)




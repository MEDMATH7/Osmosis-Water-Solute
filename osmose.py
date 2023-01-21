import pygame
import pymunk
import pymunk.pygame_util
import random


pygame.init()

WIDTH, HEIGHT = 800,800
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0,0)
draw_options = pymunk.pygame_util.DrawOptions(window)
FPS = 60

#   user preferences 

solute_spheres_quantity = int(input(f'How many solute spheres must there be in the system?\n'))
water_spheres_quantity = int(input(f'How many water spheres must there be in the system?\n'))


class SoluteSphere:
    def __init__(self):
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body,10)
        randomsx = random.randint(75,375)
        randomsy = random.randint(525,725)
        self.body.position = randomsx,randomsy
        randomvx = random.randint(-135,135)
        randomvy = random.randint(-135,135)
        self.body.velocity = randomvx,randomvy
        self.shape.color = (255,255,0,100)
        self.shape.elasticity = 1
        self.shape.density = 0.9
        self.shape.collision_type = 1
        space.add(self.body, self.shape)

    def transport_right(self, arbiter, space, data):

        #   Storing the velocity before collision with the membrane + transport to after the membrane

        velx = self.body.velocity.x
        vely = self.body.velocity.y

        self.body.position = (self.body.position.x + 26, self.body.position.y)

        #   Making the velocity after transport to remain the same as before collision with the membrane

        self.body.velocity = (-velx,vely)

    def transport_left(self, arbiter, space, data):

        #   Storing the velocity before collision with the membrane + transport to after the membrane

        velx = self.body.velocity.x
        vely = self.body.velocity.y

        self.body.position = (self.body.position.x - 26, self.body.position.y)
        
        #   Making the velocity after transport to remain the same as before collision with the membrane

        self.body.velocity = (-velx,vely)

class WaterSphere:
    def __init__(self):
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body,15)
        randomsx = random.randint(75,375)
        randomsy = random.randint(525,725)
        self.body.position = randomsx,randomsy
        randomvx = random.randint(-135,135)
        randomvy = random.randint(-135,135)
        self.body.velocity = randomvx,randomvy
        self.shape.color = (100,255,200,100)
        self.shape.elasticity = 1
        self.shape.density = 1 
        space.add(self.body,self.shape)

class VerticalWall:
    def __init__(self,x = 50):

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body,(x,500),(x,750),5)        
        self.shape.color = (0,0,0,100)
        self.shape.elasticity = 1
        space.add(self.body,self.shape)       
        
class HorizontalWall:
    def __init__(self,y = 750):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (50,y),(750,y),4)
        self.shape.color = (0,0,0,100)
        self.shape.elasticity = 1
        space.add(self.body,self.shape)

class Membrane1:
    def __init__(self):

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body,(398,500),(398,750),1)        
        self.shape.color = (255,0,0,100)
        self.shape.elasticity = 1
        self.shape.collision_type = 2
        space.add(self.body,self.shape) 

class Membrane2:
    def __init__(self):

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body,(402,500),(402,750),1)        
        self.shape.color = (255,0,0,100)
        self.shape.elasticity = 1
        #self.shape.density = 2
        self.shape.collision_type = 3
        space.add(self.body,self.shape) 
        
def Game():

    #   Creation of the interface + walls + membranes

    floor = HorizontalWall()
    roof = HorizontalWall(500)
    wall1 = VerticalWall()
    wall2 = VerticalWall(750)
    leftmembrane = Membrane1()
    rightmembrane = Membrane2()



    #   List of solvent spheres + collision treatment

    spheres = []
    collision_type_counter = 1

    for i in range(1,solute_spheres_quantity + 1):
        sphere = SoluteSphere()
        sphere.shape.collision_type = collision_type_counter
        space.add_collision_handler(sphere.shape.collision_type,leftmembrane.shape.collision_type).separate = sphere.transport_right
        space.add_collision_handler(sphere.shape.collision_type,rightmembrane.shape.collision_type).separate = sphere.transport_left
        spheres.append(sphere)
        collision_type_counter += 1


    # list of water spheres

    waterspheres = []

    for i in range(1,water_spheres_quantity + 1):
        watersphere = WaterSphere()
        waterspheres.append(watersphere)



    #   Loop creation + details

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        window.fill("white")
        space.debug_draw(draw_options)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

Game()
pygame.quit()
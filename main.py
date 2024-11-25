'''
home-dash

Smart home dashboard interface, high fidelity prototype

by Alex McColm
for CSCI 310 at VIU

started November 21st, 2024
'''
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel

from time import strftime, gmtime

class Device(object):
    '''
    Stores device name, icon & on/off state.    
    '''
    def __init__(self, name, icon):
        self.name = name
        self.on = True
        self.icon = '' # TODO: Path to an icon.

# class Camera(Device):
#     '''
#     Example subclass of Device
#     '''
#     def __init__(self, name, icon):
#         super()
#         self.feed = '' # TODO: path to image representing camera feed.

class Room(object):
    '''
    Stores a width and height in pixels.
    Contains a list of devices.
    '''
    def __init__(self, name):
        self.name = name
        self.w = 20
        self.h = 20
        self.devices = []


class Floor(object):
    '''
    Stores a number of rooms and their positions relative to eachother.
    Contains a single untitled room by default.
    Can be rendered to screen.
    '''
    def __init__(self, name):
        self.name = name
        self.rooms = [Room('Untitled Room')]
        self.adjacency = [[]]

class House(object):
    '''
    Stores a collection of named floors.
    By default, a house has one floor and one room.
    '''
    def __init__(self):
        self.floors = [Floor('Ground Floor')]

class Screen(object):
    '''
    Creates UI elements, which will be discarded when the GC
    discards this object.
    '''
    def __init__(self, manager):
        self.manager = manager
        self.elems = {}
        self.createCommonElements()
        self.create()
    
    def createCommonElements(self):
        self.elems["clock"] = UILabel(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text=strftime('%H:%M', gmtime())
        )
        self.elems["battery"] = UILabel(
            relative_rect=pygame.Rect((250, 0), (30, 50)),
            text='98%'
        )
        self.elems["home"] = UIButton(
            relative_rect=pygame.Rect((5, 500), (75, 50)),
            text='Home',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.elems["rooms"] = UIButton(
            relative_rect=pygame.Rect((80, 500), (75, 50)),
            text='Rooms',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.elems["activity"] = UIButton(
            relative_rect=pygame.Rect((155, 500), (75, 50)),
            text='Activity',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.elems["addnew"] = UIButton(
            relative_rect=pygame.Rect((230, 500), (75, 50)),
            text='Add New',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )

    def create(self):
        raise NotImplementedError('Screen is an abstract class!')

class HomeScreen(Screen):
    def create(self):
        self.elems["turnoffall"] = UIButton(
            relative_rect=pygame.Rect((100, 400), (200, 50)),
            text='Turn Off All Devices',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )

        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((50, 350), (100, 50)),
            text='Master Switch'
        )

        self.elems["quickaccess"] = UILabel(
            relative_rect=pygame.Rect((150, 10), (100, 50)),
            text='Quick Access'
        )

        self.elems["welcome"] = UILabel(
            relative_rect=pygame.Rect((50, 200), (100, 50)),
            text='Welcome'
        )

class AddNewScreen(Screen):
    def create(self):
        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((50, 350), (100, 50)),
            text='Add New'
        )

class DashDemo(object):
    '''
    Frontend and stores rooms.
    '''

    states = {
        "home":         0,
        "addnew":       1,
        "adddevice":    2,
        "addroom":      3,
        "viewfloor":    4,
        "viewdevice":   5,
        "activity":     6
    }
    screenDimensions = (300, 600)

    def __init__(self):
        self.state = self.states['home']

        pygame.init()
        self.surf = pygame.display.set_mode(self.screenDimensions)
        self.bg = pygame.Surface(self.screenDimensions)
        self.bg.fill(pygame.Color('#FFFFFF'))
        self.clock = pygame.time.Clock()
        self.running = True

        self.manager = pygame_gui.UIManager(self.screenDimensions,
            theme_path="home-dash.json")

        self.screen = HomeScreen(self.manager)

        self.mainLoop()
    
    def mainLoop(self):
        while self.running:
            
            self.td = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if isinstance(self.screen, HomeScreen):
                        self.manager.clear_and_reset()
                        self.screen = AddNewScreen(self.manager)
                    else:
                        self.manager.clear_and_reset()
                        self.screen = HomeScreen(self.manager)

                self.manager.process_events(event)

            self.manager.update(self.td)

            self.surf.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.surf)

            pygame.display.update()

def main():
    demo = DashDemo()

if __name__ == "__main__":
    main()
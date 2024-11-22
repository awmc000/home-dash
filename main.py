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
from pygame_gui.elements import UIButton

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

class Floor(object):
    '''
    Stores a number of rooms and their positions relative to eachother.
    Can be rendered to screen.
    '''
    def __init__(self, name):
        self.name = name
        self.rooms = []

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
    screenDimensions = (400, 600)

    def __init__(self):
        self.state = self.states['home']
        self.elems = {}

        pygame.init()
        self.surf = pygame.display.set_mode(self.screenDimensions)
        self.bg = pygame.Surface(self.screenDimensions)
        self.bg.fill(pygame.Color('#FFFFFF'))
        self.clock = pygame.time.Clock()
        self.running = True

        self.manager = pygame_gui.UIManager(self.screenDimensions,
            theme_path="home-dash.json")

        self.elems["turnoffall"] = UIButton(
            relative_rect=pygame.Rect((100, 400), (200, 50)),
            text='Turn Off All Devices',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )

        self.mainLoop()
    
    def mainLoop(self):
        while self.running:
            
            self.td = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.manager.process_events(event)

            self.manager.update(self.td)

            self.surf.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.surf)

            pygame.display.update()

def main():
    demo = DashDemo()

if __name__ == "__main__":
    main()
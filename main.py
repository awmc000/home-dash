'''
home-dash

Smart home dashboard interface, high fidelity prototype

by Alex McColm
for CSCI 310 at VIU

started November 21st, 2024
'''
# Built-in libraries
from datetime import datetime

# Outside libraries
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel

# Modules in this project
from screen import *

class Device(object):
    '''
    Stores device name, icon & on/off state.    
    '''
    def __init__(self, name, icon):
        self.name = name
        self.on = True
        self.icon = icon # TODO: Path to an icon.

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
    Contains two adjacent, untitled rooms by default.
    Can be rendered to screen.
    '''
    def __init__(self, name):
        self.name = name
        self.rooms = [Room('Room 0'), Room('Room 1'), Room('Room 2')]
        self.grid = [
            [0, 1],
            [None, 2]
        ]

class House(object):
    '''
    Stores a collection of named floors.
    By default, a house has one floor and one room.
    '''
    def __init__(self):
        self.floors = [Floor('Ground Floor')]
        
        # Selected floor starts on ground floor
        self.selected_floor = self.floors[0]
        
        # Create activity log with startup event
        self.log = [(datetime.now(), 'Application started')]

        # Append a test device
        self.floors[0].rooms[0].devices.append(Device('TestDevice', ''))
    
    def log_event(self, desc: str):
        self.log.append((datetime.now(), desc))

    def turn_off_all(self):
        for floor in self.floors:
            for room in floor.rooms:
                for device in room.devices:
                    device.on = False
                    self.log_event(f'Turned off {device.name} in {room.name}')


class DashDemo(object):
    '''
    Frontend and stores rooms.
    '''

    states = {
        "home":         0,
        "addnew":       1,
        "adddevice":    2,
        "addroom":      3,
        "rooms":        4,
        "viewdevice":   5,
        "activity":     6
    }
    screenDimensions = (300, 600)

    def __init__(self):
        self.state = self.states['home']
        self.house = House()

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
    
    def draw_floor(self):
        '''
        It's not pretty but it'll have to do. 这个太脏了！！！
        
        Because drawing the rectangles is pygame and not pygame_gui,
        we're going to do it here in the DashDemo class and then tell
        the RoomsScreen class to write the labels... and see how that works.
        
        '''
        grid = self.house.selected_floor.grid
                
        startPos = (20, 100)
        roomSize = (75, 75)
        margin = 2
        
        roomInfo = {}
        
        for r, row in enumerate(grid):
            for c, col in enumerate(grid[r]):
                if col is not None:
                    # Compute the position of the room to place the label
                    roomPos = (
                        20 + c*(roomSize[0]+margin), 
                        100 + r*(roomSize[1]+margin)
                    )
                    # Pack up the room index, name, x, y for sending to RoomsScreen
                    roomInfo[col] = (self.house.selected_floor.rooms[col].name, r, c)
                    pygame.draw.rect(
                        self.bg,
                        "black",
                        pygame.Rect(roomPos, roomSize), 
                        width=2
                    )
        
        self.screen.label_rooms(roomInfo)
    
    def clear(self):
        # Destroy elements drawn with pygame_gui
        self.manager.clear_and_reset()
        
        # Draw elements drawn with just pygame (room squares, mostly)
        self.bg.fill(pygame.Color('#FFFFFF'))
    
    def handle_common_elements(self, event):
        if event.ui_element == self.screen.elems['home']:
            self.state = self.states['home']
            self.clear()
            self.screen = HomeScreen(self.manager)
        elif event.ui_element == self.screen.elems['rooms']:
            self.state = self.states['rooms']
            self.manager.clear_and_reset()
            self.clear()
            self.screen = RoomsScreen(self.manager)
            self.draw_floor()
        elif event.ui_element == self.screen.elems['activity']:
            self.state = self.states['activity']
            self.clear()
            self.screen = ActivityScreen(self.manager)
            self.screen.draw_logs(self.house.log)
        elif event.ui_element == self.screen.elems['addnew']:
            self.state = self.states['addnew']
            self.clear()
            self.screen = AddNewScreen(self.manager)

    def mainLoop(self):
        while self.running:
            
            self.td = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Common elements first, then state-specific
                    self.handle_common_elements(event)
                    
                    if self.state == self.states['home']:
                        if event.ui_element == self.screen.elems['turnoffall']:
                            self.house.turn_off_all()
                        elif event.ui_element == self.screen.elems['viewall']:
                            self.state = self.states['activity']
                            self.manager.clear_and_reset()
                            self.screen = ActivityScreen(self.manager)
                            self.screen.draw_logs(self.house.log)

                self.manager.process_events(event)

            self.manager.update(self.td)

            self.surf.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.surf)

            pygame.display.update()

def main():
    demo = DashDemo()

if __name__ == "__main__":
    main()
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

# Modules in this project
from screen import *
from device import *


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
        self.floors = [Floor('Ground Floor'), Floor('First Floor')]
        
        # Selected floor starts on ground floor
        self.selected_floor = self.floors[0]
        
        # Selected room will be room 0 on ground floor
        self.selected_room = self.selected_floor.rooms[0]
        
        # Create activity log with startup event
        self.log = [(datetime.now(), 'Application started')]

        # Append a test device
        self.floors[0].rooms[0].devices.append(Light('TestDevice', ''))
    
    def log_event(self, desc: str):
        self.log.append((datetime.now(), desc))

    def turn_off_all(self):
        for floor in self.floors:
            for room in floor.rooms:
                for device in room.devices:
                    device.turn_off()
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
        "room":         5,
        "viewdevice":   6,
        "activity":     7
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
        
        EDIT: Actually removed the drawing logic and just made the labels
        into buttons and this is probably going to work.
        
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
                    # pygame.draw.rect(
                    #     self.bg,
                    #     "black",
                    #     pygame.Rect(roomPos, roomSize), 
                    #     width=2
                    # )
        
        self.screen.label_rooms(roomInfo)
    
    def clear(self):
        # Destroy elements drawn with pygame_gui
        self.manager.clear_and_reset()
        
        # Draw elements drawn with just pygame (room squares, mostly)
        self.bg.fill(pygame.Color('#FFFFFF'))
    
    def handle_room_buttons(self, event):
        '''
        Handles opening a room on the view rooms screen.
        '''
        roomButtons = {v: k for k, v in self.screen.elems.items() if 'roombutton' in k}
        
        if event.ui_element not in roomButtons:
            return
        
        id = int(
            ''.join(
                [c for c in roomButtons[event.ui_element] 
                 if c.isdigit()]
            )
        )
        
        self.house.selected_room = self.house.selected_floor.rooms[id]
        self.go_room(event, id)

    def handle_floor_buttons(self, event):
        '''
        Handle buttons to go to prev/next floor on view rooms screen.
        '''
        nFloors = len(self.house.floors)
        i = self.house.floors.index(self.house.selected_floor)
        
        print(i)
        
        if event.ui_element == self.screen.elems['prevfloor']:
            if i > 0 and nFloors > 1:
                i -= 1
        elif event.ui_element == self.screen.elems['nextfloor']:
            if i < nFloors - 1:
                i += 1
        
        self.house.selected_floor = self.house.floors[i]
        self.go_rooms(event)

    def handle_device_buttons(self, event):
        '''
        Handle buttons to inspect a device.
        '''
        deviceButtons = {v:k for k,v in self.screen.elems.items() if 'device' in k}
        
        if event.ui_element not in deviceButtons:
            return
        
        id = int(
            ''.join(
                [c for c in deviceButtons[event.ui_element] 
                 if c.isdigit()]
            )
        )
        
        print(f'{id}, {deviceButtons}')
        self.go_device(event)

    def handle_device_controls(self, event):
        '''
        Handles controls for different devices eg power buttons
        '''
        elementNames = {v: k for k,v in self.screen.elems.items() }
        print(elementNames)

        if event.ui_element not in elementNames:
            print('not in elem names')
            return

        print(f'found control: {elementNames[event.ui_element]}')

        controlName = elementNames[event.ui_element]
        
        # All control names have a dot . in them. 
        # Nothing else does, so this distinguishes device controls from other
        # gui elements.
        # TODO: STUPID HACK!!
        if '.' not in controlName:
            return
        
        device, attr = controlName.split('.')
        
        devNum = int(''.join([c for c in device if c.isdigit()]))
        
        if attr == 'power':
            self.house.selected_room.devices[devNum].toggle_power()
        elif attr == 'intensity':
            print('intensity changed')
            self.house.selected_room.devices[devNum].attributes['intensity'] = event.ui_element.get_current_value()
            print(f'set to {event.ui_element.get_current_value()}')
        
        self.screen.update_labels(self.house.selected_room)

    def set_state(self, state: str):
        self.state = self.states[state]
        self.clear()

    def go_home(self, event):
        self.set_state('home')
        self.screen = HomeScreen(self.manager)

    def go_rooms(self, event):
        self.set_state('rooms')
        self.screen = RoomsScreen(self.manager)
        self.screen.update(self.house.selected_floor)
        self.draw_floor()
        
    def go_room(self, event, id):
        self.set_state('room')
        self.screen = RoomScreen(self.manager)
        self.screen.update(self.house.selected_floor.rooms[id])

    def go_device(self, event):
        self.set_state('viewdevice')
        self.screen = DeviceScreen(self.manager)
        self.screen.update(self.house.selected_room)

    def go_activity(self, event):
        self.set_state('activity')
        self.screen = ActivityScreen(self.manager)
        self.screen.draw_logs(self.house.log)

    def go_addnew(self, event):
        self.set_state('addnew')
        self.screen = AddNewScreen(self.manager)

    def handle_common_elements(self, event):
        if event.ui_element == self.screen.elems['home']:
            self.go_home(event)
        elif event.ui_element == self.screen.elems['rooms']:
            self.go_rooms(event)
        elif event.ui_element == self.screen.elems['activity']:
            self.go_activity(event)
        elif event.ui_element == self.screen.elems['addnew']:
            self.go_addnew(event)

    def mainLoop(self):
        while self.running:
            
            self.td = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(f'self.screen.elems at shutdown:{self.screen.elems}')
                    self.running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Common elements first, then state-specific
                    self.handle_common_elements(event)
                    
                    if self.state == self.states['home']:
                        if event.ui_element == self.screen.elems['turnoffall']:
                            self.house.turn_off_all()
                        elif event.ui_element == self.screen.elems['viewall']:
                            self.go_activity(event)
                        elif event.ui_element == self.screen.elems['viewroomsbutton']:
                            self.go_rooms(event)
                    
                    if self.state == self.states['rooms']:
                        print(f'Handling rooms buttons. State is {self.state}')
                        self.handle_room_buttons(event)
                        
                        # Check if state changed after this handler function.
                        if self.state != self.states['rooms']:
                            break
                        
                        self.handle_floor_buttons(event)
                    
                    if self.state == self.states['room']:
                        if event.ui_element == self.screen.elems['backbutton']:
                            self.go_rooms(event)
                        self.handle_device_buttons(event)

                    if self.state == self.states['viewdevice']:
                        self.handle_device_controls(event)

                self.manager.process_events(event)

            self.manager.update(self.td)

            self.surf.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.surf)

            pygame.display.update()

def main():
    demo = DashDemo()

if __name__ == "__main__":
    main()
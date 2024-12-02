'''
home-dash

Smart home dashboard interface, high fidelity prototype

by Alex McColm
for CSCI 310 at VIU

started November 21st, 2024

screen.py

Screen classes

Split off Nov 24
'''
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UIScrollingContainer

from time import strftime, gmtime

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
            relative_rect=pygame.Rect((240, 0), (50, 50)),
            text='98%'
        )

        navbar_x, navbar_y = 0, 525
        nav_button_width = 70
        nav_button_height = 70
        nav_spacing = 5

        self.elems["home"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing, navbar_y), (nav_button_width, nav_button_height)),
            text='Home',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button', object_id='#homebutton')
        )
        self.elems["rooms"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing + 1 * (nav_button_width), navbar_y), (nav_button_width, nav_button_height)),
            text='Rooms',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button', object_id='#roomsbutton')
        )
        self.elems["activity"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing + 2 * (nav_button_width), navbar_y), (nav_button_width, nav_button_height)),
            text='Activity',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button', object_id='#activitybutton')
        )
        self.elems["addnew"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing + 3 * (nav_button_width), navbar_y), (nav_button_width, nav_button_height)),
            text='Add New',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )

    def create(self):
        raise NotImplementedError('Screen is an abstract class!')

class HomeScreen(Screen):
    def create(self):
        
        # Welcome section
        self.elems["welcome"] = UILabel(
            relative_rect=pygame.Rect((100, 20), (100, 50)),
            text='Welcome'
        )

        self.elems["viewroomsbutton"] = UIButton(
            relative_rect=pygame.Rect((50, 80), (200, 50)),
            text='View Rooms',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )

        # Quick access section
        self.elems["quickaccess"] = UILabel(
            relative_rect=pygame.Rect((20, 120), (100, 50)),
            text='Quick Access'
        )
        
        quick_button_length = 80
        self.elems["quick1"] = UIButton(
            relative_rect=pygame.Rect((20, 170), (quick_button_length, quick_button_length)),
            text='quick1',
            manager=self.manager,
            object_id = ObjectID(class_id='@quickdevice')
        )
        
        self.elems["quick2"] = UIButton(
            relative_rect=pygame.Rect((100, 170), (quick_button_length, quick_button_length)),
            text='quick2',
            manager=self.manager,
            object_id = ObjectID(class_id='@quickdevice')
        )

        self.elems["quick3"] = UIButton(
            relative_rect=pygame.Rect((180, 170), (quick_button_length, quick_button_length)),
            text='quick3',
            manager=self.manager,
            object_id = ObjectID(class_id='@quickdevice')
        )
        
        # Recent activity section
        self.elems["recentactivity"] = UILabel(
            relative_rect=pygame.Rect((20, 250), (100, 50)),
            text='Recent Activity'
        )
        
        self.elems["viewall"] = UIButton(
            relative_rect=pygame.Rect((200, 250), (quick_button_length, 40)),
            text='See All',
            manager=self.manager,
            object_id = ObjectID(class_id='@quickdevice')
        )
        # Master switch section
        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((20, 350), (100, 50)),
            text='Master Switch'
        )
        
        self.elems["turnoffall"] = UIButton(
            relative_rect=pygame.Rect((50, 400), (200, 50)),
            text='Turn Off All Devices',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )



class AddNewScreen(Screen):
    def create(self):
        self.elems["activitylog"] = UILabel(
            relative_rect=pygame.Rect((100, 20), (100, 50)),
            text='Add New'
        )
        self.elems["turnoffall"] = UIButton(
            relative_rect=pygame.Rect((50, 200), (200, 80)),
            text='New Room',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )
        self.elems["turnoffall"] = UIButton(
            relative_rect=pygame.Rect((50, 400), (200, 80)),
            text='New Device',
            manager=self.manager,
            object_id = ObjectID(class_id='@turnoffall_button')
        )

class ActivityScreen(Screen):
    def create(self):
        self.elems["activitylog"] = UILabel(
            relative_rect=pygame.Rect((100, 20), (100, 50)),
            text='Activity Log'
        )

        self.elems["log"] = UIScrollingContainer(
            relative_rect=pygame.Rect((25, 100), (250, 400)),
            manager=self.manager,
            allow_scroll_x = False
        )
        self.elems["log"].set_scrollable_area_dimensions((200, 800))
        
    def draw_logs(self, log):
        i = 0
        for time, desc in reversed(log):
            self.elems[f'logitem{i}'] = UIButton(
                relative_rect=pygame.Rect((10, 20 + (i* 30)), (250, 30)),
                text=desc,
                container = self.elems["log"]
            )
            i += 1

class RoomsScreen(Screen):
    def create(self):
        self.elems["floortitle"] = UILabel(
            relative_rect=pygame.Rect((100, 20), (100, 50)),
            text='Ground Floor'
        )
        
        self.elems["prevfloor"] = UIButton(
            relative_rect=pygame.Rect((70, 50), (30, 30)),
            text='<<'
        )

        self.elems["nextfloor"] = UIButton(
            relative_rect=pygame.Rect((200, 50), (30, 30)),
            text='>>'
        )

    def update(self, floor):
        self.elems["floortitle"].set_text(floor.name)
        print(f'Set floor title to {floor.name}.')
    
    def label_rooms(self, roomInfo):
        startPos = (20, 100)
        roomSize = (75, 75)
        margin = 2
        
        for roomi, v in roomInfo.items():
            name, gx, gy = v
            x = startPos[0] + gy*(roomSize[0]+margin)
            y = startPos[1] + gx*(roomSize[1]+margin)
            self.elems[f"roombutton{roomi}"] = UIButton(
                relative_rect=pygame.Rect((x, y), roomSize),
                text=name
            )

class RoomScreen(Screen):
    def create(self):
        self.elems["backbutton"] = UIButton(
            relative_rect=pygame.Rect((20, 50), (80, 40)),
            text='Back',
            manager=self.manager
            # object_id = ObjectID(class_id='@turnoffall_button')
        )
        
        self.elems["room"] = UIButton(
            relative_rect=pygame.Rect((50, 100), (200, 200)),
            text='',
            manager=self.manager
            # object_id = ObjectID(class_id='@turnoffall_button')
        )
        
        self.elems["floortitle"] = UILabel(
            relative_rect=pygame.Rect((50, 300), (100, 50)),
            text='Device List'
        )
    
    def update(self, room):
        '''
        room: Room object
        '''
        self.room = room
        self.elems["roomtitle"] = UILabel(
            relative_rect=pygame.Rect((100, 20), (100, 50)),
            text=f'{room.name}'
        )
        
        devices = self.room.devices
        
        startingPos = (30, 350)
        labelSize = (150, 30)
        margin = 2
        
        iconStart = (50, 100)
        iconSize = (35, 35)
        
        for i, device in enumerate(devices):
            self.elems[f"devicelabel{i}"] = UIButton(
                relative_rect=pygame.Rect(
                    (startingPos[0] + i*(labelSize[0]+margin),
                    (startingPos[1]+ i*(startingPos[1]+margin))),
                    labelSize),
                text=device.name
            )
            self.elems[f"deviceicon{i}"] = UIButton(
                relative_rect=pygame.Rect(
                    (iconStart[0] + i*(iconSize[0]+margin) + margin,
                    (iconStart[1]+ i*(iconSize[1]+margin)) + margin),
                    iconSize),
                text=device.name[:2]
            )

class DeviceScreen(Screen):
    def create(self):
        self.elems["backbutton"] = UIButton(
            relative_rect=pygame.Rect((20, 50), (80, 40)),
            text='Back',
            manager=self.manager
            # object_id = ObjectID(class_id='@turnoffall_button')
        )
        self.elems["attributelist"] = UILabel(
            relative_rect=pygame.Rect((50, 300), (100, 50)),
            text='Attribute List'
        )
        
    def update(self, room):
        '''
        room: Room object. Should only ever be DashDemo.house.selected_room
        
        For all devices in the room:
            - Draws an icon and a label.
            - Get modifier, use it to draws controls and attribute labels
                - Add all those controls to elems for handling.
        '''
        
        # Draw device attributes list
        # TODO: This only supports one device right now
        device = room.devices[0]
        # for device in room.devices:
        #     startingPos = (30, 350)
        #     labelSize = (150, 30)
        #     margin = 2
        
        #     for i, attribute in enumerate(device.attributes):
        #         self.elems[f"attrlabel{i}"] = UIButton(
        #             relative_rect=pygame.Rect(
        #                 (startingPos[0] + i*(labelSize[0]+margin),
        #                 (startingPos[1]+ i*(startingPos[1]+margin))),
        #                 labelSize),
        #             text=attribute
        #         )
        
        # Draw device controls
        # TODO: This only supports one control right now
        modifier = device.get_modifier()
        modifier.linkManager(self.manager)
        
        for name, elem in modifier.uiElements.items():
            self.elems[device.name + '.' + name] = elem
            elem.set_position((50, 400))
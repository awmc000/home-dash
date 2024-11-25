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
from pygame_gui.elements import UIButton, UILabel

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
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.elems["rooms"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing + 1 * (nav_button_width), navbar_y), (nav_button_width, nav_button_height)),
            text='Rooms',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.elems["activity"] = UIButton(
            relative_rect=pygame.Rect((navbar_x + nav_spacing + 2 * (nav_button_width), navbar_y), (nav_button_width, nav_button_height)),
            text='Activity',
            manager=self.manager,
            object_id = ObjectID(class_id='@navbar_button')
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
            object_id = ObjectID(class_id='@quick')
        )
        
        self.elems["quick2"] = UIButton(
            relative_rect=pygame.Rect((100, 170), (quick_button_length, quick_button_length)),
            text='quick2',
            manager=self.manager,
            object_id = ObjectID(class_id='@quick')
        )

        self.elems["quick3"] = UIButton(
            relative_rect=pygame.Rect((180, 170), (quick_button_length, quick_button_length)),
            text='quick3',
            manager=self.manager,
            object_id = ObjectID(class_id='@quick')
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
            object_id = ObjectID(class_id='@quick')
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
        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((50, 350), (150, 50)),
            text='TODO: Add New'
        )

class ActivityScreen(Screen):
    def create(self):
        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((50, 350), (150, 50)),
            text='TODO: Activity Log'
        )

class RoomsScreen(Screen):
    def create(self):
        self.elems["masterswitch"] = UILabel(
            relative_rect=pygame.Rect((50, 350), (150, 50)),
            text='TODO: Rooms'
        )
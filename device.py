'''
home-dash

Smart home dashboard interface, high fidelity prototype

by Alex McColm
for CSCI 310 at VIU

started November 21st, 2024

device.py: Device classes and their attributes

Split off December 1st, 2024
'''

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel

class DeviceModifier(object):
    '''
    GUI element container that handles events by acting on the device.
    It's just the controls themselves, eg buttons & sliders.
    
    Initially elements have no manager. Once linked they will actually 
    be drawn.
    
    For each device there should be 3 elements in the room device list:
        - label with devices' name
        - pairs of controls & attribute labels
            - eg. power switch and "ON/OFF" label
            - eg. dimmer switch and integer 0-100 label
    '''
    def __init__(self, device):
        self.device = device
        
        # Construct a basic on/off switch which all devices have
        toggleSwitch = UIButton(
            relative_rect=pygame.Rect((0, 0), (50, 20)),
            text='ON/OFF',
            manager=None,
            object_id = ObjectID(class_id='@navbar_button')
        )
        self.uiElements = {'power': toggleSwitch}
    
    def linkManager(self, manager):
        self.manager = manager
        for elem in self.uiElements.values():
            elem.manager = manager
            elem.rebuild()
            
    def handle(self, event):
        print(f'{event.ui_element} == {self.uiElements['power']}')
        if event.ui_element == self.uiElements['power']:
            self.device.attributes['on'] = not self.device.attributes['on']
            print(f'device power now:{self.device.attributes['on']} ')
        else:
            # TODO: This is glitched, the power button doesn't match the power button.
            print('Not a match for power')

class Device(object):
    '''
    Stores device name, icon & on/off state.    
    '''
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon # TODO: Path to an icon.
        self.attributes = {'on': True}

    def toggle_power(self):
        if self.attributes['on']:
            self.attributes['on'] = False
        else:
            self.attributes['on'] = True

    def turn_off(self):
        self.attributes['on'] = False
    
    def get_modifier(self):
        '''
        Returns an object that can be used to modify & get gui elements for 
        modifying this device.
        '''
        return DeviceModifier(self)
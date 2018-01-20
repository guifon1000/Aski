
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.properties import ListProperty
from functools import partial
kv = """
<Pixel>:
    pcolor: 0.5, 0.1, 0.8, 0.2
    canvas.before:
        Color:
            rgba: self.pcolor
        Rectangle:
            size: (0.9 * self.size[0] , 0.9 * self.size[1] )
            pos: self.pos
"""

Builder.load_string(kv)
N = 79
class World(BoxLayout):
    def __init__(self, **kwargs):
        super(World, self).__init__(**kwargs)


class Controls(GridLayout):
    def __init__(self, **kwargs):
        super(Controls, self).__init__(**kwargs)
        lc = Label(text='symbol', size = (0.1, 0.1))
        tc = TextInput(text='*', multiline=False, id='symbol', size=(0.1, 0.1))
        export_button = Button(text='Export', id='export_button')
        selection_check = CheckBox(text='Selection', id='selection')
        self.add_widget(tc)
        self.add_widget(lc)
        self.add_widget(export_button)
        self.add_widget(selection_check)
        def get_string(self):
            string_array = []
            for p in self.parent.parent.walk():
                if p.id=='pixel':
                    string_array.append([p.index, p.text])
            string = sorted(string_array, key = lambda x:x[0])
            output = ''
            for i,c in enumerate(string):
                if c[1] == '':
                    output += ' '
                else:
                    output += str(c[1])
                if ((i+1) % N) ==0:
                    output += '\n'
            print '-----------'
            print output
            print '-----------'
        export_button.bind(on_press = get_string)
        

class PixelZone(GridLayout):
    def __init__(self, **kwargs):
        super(PixelZone, self).__init__(pos_hint={'center_x':.5, 'center_y':.5}, **kwargs)

    def export(self):
        for i,p in enumerate(self.children):
            print i
        
 
class AsciiKiApp(App):
    def build(self):
        pixel_zone = PixelZone(rows=int(0.65*N), cols=N, id='pixelzone')
        controls = Controls(rows=10, cols=2, id='controls' , size_hint = (0.25, None) )
        world = World()
        index = -1
        for i in range(pixel_zone.rows):
            for j in range(pixel_zone.cols):
                index += 1 
                pixel = Pixel(i,j, index, id='pixel')
                pixel_zone.add_widget(pixel)
        world.add_widget(controls)
        world.add_widget(pixel_zone)
        #Clock.schedule_interval(world.update, 0.1)
        return world



class Pixel(ButtonBehavior, Label):
#class Pixel(ButtonBehavior, Widget):
    def __init__(self, i=0, j=0, idx = 0, **kwargs):
        #self.pcolor = ListProperty([1., 1., 1., 1.])
        self.index = idx
        self.active = '+'
        self.text = ''
        self.selected = False
        sliding_selection = False
        super(Pixel, self).__init__(**kwargs)

        def selection_mode(self):
            for p in self.parent.parent.walk():
                if (p.id == 'selection'):
                    return p.active

        def switch_select(self):
            if not self.selected :
                self.pcolor=[0.5, 0.3, 0.6, 0.7]
                self.selected = True 
            elif self.selected :
                self.pcolor=[0.5, 0.1, 0.8, 0.2] 
                self.selected = False 



        def on_press_callback(self):
            if not selection_mode(self):
                self.set_text_default()
            else:
                sliding_selection = True
                print  'clic ' + str(self.index)
                switch_select(self)

        def on_release_callback(self):
            if selection_mode(self):
                print 'release '+str(self.index)


        def on_touch_move_callback(self, touch):
            if not selection_mode(self):
                if self.collide_point(touch.pos[0], touch.pos[1]):
                    self.set_text_default()
        
        self.bind(on_press = on_press_callback)
        self.bind(on_touch_move = on_touch_move_callback)
        self.bind(on_release = on_release_callback)

    def set_text_default(self):
        if (self.text == ''):
            for p in self.parent.parent.walk():
                if (p.id == 'symbol') and p.text:
                    st = str(p.text)[0]
                    break
            self.text = st


if __name__=='__main__':
    AsciiKiApp().run()

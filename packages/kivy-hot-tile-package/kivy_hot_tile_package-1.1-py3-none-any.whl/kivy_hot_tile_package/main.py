from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
import random

# class of the settings popup
class SettingsPopup(Popup):
    def __init__(self, caller):
        super(SettingsPopup, self).__init__()
        self.caller = caller
        self.ids.grid_size.text = str(caller.gridSize)
        self.ids.moving_target.active = caller.movingTarget
    # method for saving the settings
    def save_settings(self):
        if int(self.ids.grid_size.text) >= 2 and int(self.ids.grid_size.text) <= 30:
            self.caller.gridSize = int(self.ids.grid_size.text)
        self.caller.movingTarget = self.ids.moving_target.active
        self.caller.create_game()
        self.dismiss()
    # method for resuming the game
    def resume(self):
        self.caller.timeClockEvent = Clock.schedule_interval(self.caller.update_time, 1)
        self.dismiss()

# class of the tile
class Tile(Button):
    def __init__(self, caller, idd):
        super(Tile, self).__init__()
        self.caller = caller
        self.id = idd
    def click(self):
        if self.text == '':
            # getting the distance between the hot tile and the clicked tile
            position_of_clicked_tile = [0,0]
            for i in range(self.caller.gridSize):
                for j in range(self.caller.gridSize):
                    if self.caller.gameGrid[i][j].id == self.id:
                        position_of_clicked_tile = [i,j]
                        break
            distance = abs(self.caller.hotTile[0] - position_of_clicked_tile[0]) + abs(self.caller.hotTile[1] - position_of_clicked_tile[1])
            # checking if the player won
            if distance == 0:
                self.caller.ids.title_label.text = "You win!"
                Clock.unschedule(self.caller.timeClockEvent)
                self.background_normal = ''
                self.background_color = [0,1,0,1]
                for i in range(self.caller.gridSize):
                    for j in range(self.caller.gridSize):
                        self.caller.gameGrid[i][j].disabled = True
            else:
                self.text = str(distance)
                # setting the color based on the distance
                self.background_normal = ''
                self.background_down = ''
                if distance <=3:
                    color = 1 -0.3 * distance
                    if color < 0:
                        color = 0.1
                    self.background_color = [color,0,0,1]
                elif distance > 3 and distance <= 6:
                    color = 1 - 0.1 * distance
                    if color < 0:
                        color = 0.1
                    self.background_color = [color,color,0,1]
                else:
                    color = 1 - 0.1 * distance
                    if color < 0:
                        color = 0.1
                    self.background_color = [0,0,color,1]
                self.caller.moves -= 1
                self.caller.ids.moves_label.text = 'Moves Left: ' + str(self.caller.moves)
                # if the moving target is enabled, moving the hot tile
                if self.caller.movingTarget:
                    rands = [random.randint(-1,1), random.randint(-1,1)]
                    while True:
                        if self.caller.hotTile[0] + rands[0] >= 0 and self.caller.hotTile[0] + rands[0] < self.caller.gridSize and self.caller.hotTile[1] + rands[1] >= 0 and self.caller.hotTile[1] + rands[1] < self.caller.gridSize and self.caller.gameGrid[self.caller.hotTile[0] + rands[0]][self.caller.hotTile[1] + rands[1]].text == '':
                            break
                        else:
                            rands = [random.randint(-1,1), random.randint(-1,1)]
                    self.caller.hotTile = [self.caller.hotTile[0] + rands[0], self.caller.hotTile[1] + rands[1]]
                # checking if the game is over
                if self.caller.moves == 0:
                    self.caller.ids.title_label.text = "You lose!"
                    Clock.unschedule(self.caller.timeClockEvent)
                    for i in range(self.caller.gridSize):
                        for j in range(self.caller.gridSize):
                            self.caller.gameGrid[i][j].disabled = True

# class of the main grid
class MainGrid(BoxLayout):
    # method for creating/reseting the game
    def create_game(self):
        self.time = 0
        self.moves = self.gridSize * 2
        self.ids.moves_label.text = 'Moves Left: ' + str(self.moves)
        self.ids.time_label.text = 'Time: 00:00'
        self.ids.title_label.text = "Hot Tile"
        self.gameGrid = []
        self.ids.game_grid.clear_widgets()
        if self.timeClockEvent: # this should never be true, however just in case
            Clock.unschedule(self.timeClockEvent)
        self.time = 0
        self.timeClockEvent = Clock.schedule_interval(self.update_time, 1)
        self.hotTile = [random.randint(0, self.gridSize-1), random.randint(0, self.gridSize-1)]
        num = 0
        for i in range(self.gridSize):
            self.gameGrid.append([])
            for j in range(self.gridSize):
                tile = Tile(self, num)
                num += 1
                self.gameGrid[i].append(tile)
                self.ids.game_grid.add_widget(tile)
        self.ids.game_grid.cols = self.gridSize
    # method for starting the game
    def settings(self):
        Clock.unschedule(self.timeClockEvent)
        popup = SettingsPopup(self)
        popup.open()
    # method for updating the time label
    def update_time(self, t):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.ids.time_label.text = 'Time: %02d:%02d' % (minutes, seconds)

# app class
class hot_tileApp(App):
    def build(self):
        return MainGrid()

# running the app
def main():
    hot_tileApp().run()
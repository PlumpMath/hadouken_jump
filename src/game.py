#-*-coding:utf-8-*-

from src.config import *

import direct.directbase.DirectStart
import sys

from panda3d.core import Point3
from pandac.PandaModules import ClockObject
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.DirectGui import DirectButton
from src.functions import load_object
from src.blanka import Blanka
from src.ryu import Ryu


class Game(DirectObject):

    def __init__(self):
        self.player = Blanka(self)
        self.ryu = Ryu()

        self.setup_panda()
        self.setup_keys()
        self.load_sounds()
        self.load_textures()
        self.load_sprites()
        self.setup_gui()
        self.start_game()

    def setup_panda(self):
        FPS = 30
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(FPS)

    def setup_keys(self):
        self.keys = {'move_left': 0, 'move_right': 0, 'jump': 0}
        self.accept('escape', sys.exit)
        self.accept('arrow_left',     self.set_key, ['move_left', 1])
        self.accept('arrow_left-up',  self.set_key, ['move_left', 0])
        self.accept('arrow_right',    self.set_key, ['move_right', 1])
        self.accept('arrow_right-up', self.set_key, ['move_right', 0])
        self.accept('arrow_up',       self.set_key, ['jump', 1])
        self.accept('arrow_up-up',    self.set_key, ['jump', 0])

    def set_key(self, key, value):
        self.keys[key] = value

    def setup_game_task(self):
        self.game_task = taskMgr.add(self.game_loop, 'game_loop')
        self.game_task.last = 0
        taskMgr.add(self.player.manage_collisions, 'manage_collisions')

    def load_sounds(self):
        music = loader.loadSfx('sound/guile_theme.ogg')
        music.setLoop(True)
        music.setVolume(0.7)
        music.play()

    def load_textures(self):
        self.player.load_textures()
        self.ryu.load_textures()
        self.background_sprite = loader.loadTexture('im/Stage.png')
        self.ko_image = loader.loadTexture('im/KO.png')

    def load_sprites(self):
        stage = load_object(self.background_sprite, scale=550, pos=Point3(0, 400, 0), transparency=False)
        self.ryu.load_sprite()
        self.player.load_sprite()

    def setup_gui(self):
        self.ko = load_object(self.ko_image, scale=10, transparency=True, pos=(0, 40, 0))
        self.play_again_button = DirectButton(text = "Play again", scale=0.2, command=self.start_game)
        self.init_gui()

    def game_loop(self, task):
        dt = task.time - task.last
        task.last = task.time
        self.player.update_position()
        return task.cont

    def start_game(self):
        self.init_gui()
        taskMgr.add(self.ryu.begin_to_throw, 'begin_to_throw')
        self.setup_game_task()

    def init_gui(self):
        self.ko.reparentTo(hidden)
        self.ko.setSx(20)
        self.play_again_button.setZ(100)
        self.play_again_button.setX(0.05)

    def end_game(self):
        self.ryu.win_sound.play()
        self.ryu.hadouken.move_to_initial_position()
        self.ryu.hadouken.set_hidden(True)
        self.ryu.state = 'idle'

        taskMgr.remove('manage_collisions')
        taskMgr.remove('game_loop')
        taskMgr.remove('throw_hadoukens')
        taskMgr.remove('move_hadouken')

        self.ko.reparentTo(camera)
        self.play_again_button.setZ(-0.8)



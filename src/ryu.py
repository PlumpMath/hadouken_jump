#-*-coding:utf-8-*-

import random

from panda3d.core import Point3
from src.functions import load_object
from src.hadouken import Hadouken


class Ryu(object):

    def __init__(self):
        self.state = 'idle'
        self.random_time_set = False
        self.animation_is_reverse = False
        self.hadouken_thrown = False

        self.hadouken = Hadouken()
        self.load_sounds()
        self.setup_tasks()
        self.setup_sprites()

    def load_sounds(self):
        self.hadouken_sound = loader.loadSfx('sound/Hadouken.mp3')
        self.win_sound = loader.loadSfx('sound/Death.mp3')

    def setup_tasks(self):
        taskMgr.add(self.animate, 'animate_ryu')
        taskMgr.add(self.begin_to_throw, 'begin_to_throw')

    def setup_sprites(self):
        self.number_of_sprites = {'idle': 5, 'throwing': 5}
        self.idle_sprites = []
        self.throwing_sprites = []
        self.sprite = None

    def load_textures(self):
        for i in xrange(self.number_of_sprites['idle']):
            self.idle_sprites.append(loader.loadTexture('im/Ryu_idle_{0}.png'.format(i + 1)))

        for i in xrange(self.number_of_sprites['throwing']):
            self.throwing_sprites.append(loader.loadTexture('im/Ryu_throwing_{0}.png'.format(i + 1)))

    def load_sprite(self):
        self.sprite = load_object(self.idle_sprites[0], scale=40, pos=Point3(50, 201, -27), transparency=True)

    def animate(self, task):
        if task.time < 0.15:
            return task.cont

        texture_file = str(self.sprite.getTexture().getFilename())

        if self.state == 'idle':
            if 'idle' in texture_file:
                self.set_next_texture(texture_file, self.idle_sprites)
            else:
                self.sprite.setTexture(self.idle_sprites[0])

        elif self.state == 'throwing':
            if 'throwing' in texture_file:
                self.set_next_texture(texture_file, self.throwing_sprites)
            else:
                self.sprite.setTexture(self.throwing_sprites[0])

        return task.again

    def set_next_texture(self, texture_file, sprites):
        prefix = 'im/Ryu_{0}_'.format(self.state)
        remainder = texture_file.replace(prefix, '')
        index = int(remainder.replace('.png', '')) - 1

        if index == len(sprites) - 1:
            self.animation_is_reverse = True
        elif index == 0:
            self.animation_is_reverse = False

        if self.animation_is_reverse:
            self.sprite.setTexture(sprites[index - 1])
        else:
            self.sprite.setTexture(sprites[index + 1])

    def begin_to_throw(self, task):
        if task.time < 1:
            return task.cont

        taskMgr.add(self.throw_hadoukens, 'throw_hadoukens')
        taskMgr.remove('begin_to_throw')
        return task.exit

    def throw_hadoukens(self, task):
        if not self.random_time_set:
            self.random_time = random.uniform(0.1, 2)
            self.random_time_set = True
        
        if task.time < self.random_time:
            return task.cont

        if task.time >= self.random_time:
            self.hadouken_sound.play()
            self.state = 'throwing'

        if task.time >= self.random_time + 0.15 * 4 and not self.hadouken_thrown:
            self.throw_one_hadouken()
            self.hadouken_thrown = True

        if task.time >= self.random_time + 0.15 * 5:
            self.state = 'idle'
            self.hadouken_thrown = False
            self.random_time_set = False
            return task.again

        return task.cont

    def throw_one_hadouken(self):
        if self.hadouken.is_hidden():
            self.hadouken.set_hidden(False)
        else:
            self.hadouken.move_to_initial_position()
            
        taskMgr.add(self.hadouken.move, 'move_hadouken')



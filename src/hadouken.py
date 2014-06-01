#-*-coding:utf-8-*-

from panda3d.core import Point3
from src.functions import load_object


class Hadouken(object):

    def __init__(self):
        self.animation_is_reverse = False
        self.setup_sprites()
        self.load_textures()
        self.load_sprite()
        self.set_hidden(True)
        self.setup_tasks()

    def setup_sprites(self):
        self.number_of_sprites = 4
        self.sprites = []
        self.sprite = None

    def setup_tasks(self):
        taskMgr.add(self.animate, 'animate_hadouken')

    def load_textures(self):
        for i in xrange(self.number_of_sprites):
            self.sprites.append(loader.loadTexture('im/Hadouken_{0}.png'.format(i + 1)))

    def load_sprite(self):
        self.sprite = load_object(self.sprites[0], scale=30, transparency=True)
        self.move_to_initial_position()

    def animate(self, task):
        if task.time < 0.15:
            return task.cont

        texture_file = str(self.sprite.getTexture().getFilename())
        self.set_next_texture(texture_file)
        return task.again

    def set_next_texture(self, texture_file):
        remainder = texture_file.replace('im/Hadouken_', '')
        index = int(remainder.replace('.png', '')) - 1

        if index == len(self.sprites) - 1:
            self.animation_is_reverse = True
        elif index == 0:
            self.animation_is_reverse = False

        if self.animation_is_reverse:
            self.sprite.setTexture(self.sprites[index - 1])
        else:
            self.sprite.setTexture(self.sprites[index + 1])

    def move_to_initial_position(self):
        self.sprite.setPos(Point3(32, 200, -27))

    def set_hidden(self, yes):
        if yes:
            self.sprite.setZ(100)
        else:
            self.sprite.setZ(-27)

    def is_hidden(self):
        return self.sprite.getZ() == 100

    def move(self, task):
        if task.time < 0.0001:
            return task.cont

        offset = 2

        if self.sprite.getX() - offset >= -100:
            self.sprite.setX(self.sprite.getX() - offset)
            return task.again

        self.move_to_initial_position()
        self.set_hidden(True)
        taskMgr.remove('move_hadouken')
        return task.exit
    


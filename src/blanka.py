#-*-coding:utf-8-*-

from panda3d.core import Point3
from src.functions import load_object


class Blanka(object):

    def __init__(self, app=None):
        self.app = app
        self.state = 'idle'
        self.animation_is_reverse = False
        self.jump_maximum_height = 3
        self.jump_up = True
        self.jumping = False
        self.setup_tasks()
        self.setup_sprites()

    def setup_tasks(self):
        taskMgr.add(self.animate, 'animate_player')

    def setup_sprites(self):
        self.number_of_sprites = {'idle': 4, 'moving': 2, 'jumping': 3, 'dying': 1}
        self.idle_sprites = []
        self.moving_sprites = []
        self.jumping_sprites = []
        self.dying_sprites = []
        self.sprite = None

    def load_textures(self):
        for i in xrange(self.number_of_sprites['idle']):
            self.idle_sprites.append(loader.loadTexture('im/Blanka_idle_{0}.png'.format(i + 1)))

        for i in xrange(self.number_of_sprites['moving']):
            self.moving_sprites.append(loader.loadTexture('im/Blanka_moving_{0}.png'.format(i + 1)))

        for i in xrange(self.number_of_sprites['jumping']):
            self.jumping_sprites.append(loader.loadTexture('im/Blanka_jumping_{0}.png'.format(i + 1)))

        for i in xrange(self.number_of_sprites['dying']):
            self.dying_sprites.append(loader.loadTexture('im/Blanka_dying_{0}.png'.format(i + 1)))

    def load_sprite(self):
        self.sprite = load_object(self.idle_sprites[0], scale=35, pos=Point3(-50, 200, -30), transparency=True)

    def update_position(self):
        offset = 3

        if self.app.keys['jump'] and not self.jumping:
            taskMgr.add(self.animate_jump, 'animate_player_jump')

        if self.app.keys['move_left']:
            self.state = 'moving'
            
            if self.sprite.getX() - offset >= -100:
                self.sprite.setPos(Point3(self.sprite.getX() - offset, 200, self.sprite.getZ()))

            return

        if self.app.keys['move_right']:
            self.state = 'moving'
            
            if self.sprite.getX() + offset <= 100:
                self.sprite.setPos(Point3(self.sprite.getX() + offset, 200, self.sprite.getZ()))

            return

        self.state = 'idle'

    def animate(self, task):
        if task.time < 0.15:
            return task.cont
        
        texture_file = str(self.sprite.getTexture().getFilename())

        if self.state == 'dying':
            if 'dying' in texture_file:
                self.set_next_texture(texture_file, self.dying_sprites, self.state)
            else:
                self.sprite.setTexture(self.dying_sprites[0])

        elif self.jumping:
            if 'jumping' in texture_file:
                self.set_next_texture(texture_file, self.jumping_sprites, 'jumping')
            else:
                self.sprite.setTexture(self.jumping_sprites[0])
            
        elif self.state == 'idle':
            if 'idle' in texture_file:
                self.set_next_texture(texture_file, self.idle_sprites, self.state)
            else:
                self.sprite.setTexture(self.idle_sprites[0])

        elif self.state == 'moving':
            if 'moving' in texture_file:
                self.set_next_texture(texture_file, self.moving_sprites, self.state)
            else:
                self.sprite.setTexture(self.moving_sprites[0])

        return task.again

    def set_next_texture(self, texture_file, sprites, state):
        prefix = 'im/Blanka_{0}_'.format(state)
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

    def animate_jump(self, task):
        offset = 3
        self.jumping = True

        if task.time < 0.01:
            return task.cont

        if self.jump_up:
            if self.sprite.getZ() + offset <= self.jump_maximum_height:
                self.sprite.setPos(Point3(self.sprite.getX(), 200, self.sprite.getZ() + offset))
            else:
                self.jump_up = False

            return task.again

        else:
            if self.sprite.getZ() - offset + 10 >= -30:
                self.sprite.setPos(Point3(self.sprite.getX(), 200, self.sprite.getZ() - offset))
                return task.again
            else:
                self.sprite.setZ(-30)
                self.jump_up = True
                taskMgr.remove('animate_player_jump')
                self.jumping = False

                if self.state != 'dying':
                    self.state = 'idle'
                    
                return task.exit

    def manage_collisions(self, task):
        if not self.app.ryu.hadouken.is_hidden():
            hadouken_x = self.app.ryu.hadouken.sprite.getX()
            player_x = self.sprite.getX()
            player_z = self.sprite.getZ()

            if player_x + 10 >= hadouken_x and hadouken_x >= player_x:
                if player_z <= -10:
                    self.die()
                    return task.exit

        return task.again

    def die(self):
        self.state = 'dying'
        self.app.end_game()


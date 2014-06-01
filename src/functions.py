#-*-coding:utf-8-*-

from panda3d.core import Point3


def load_object(tex=None, pos=Point3(0, 200, 0), scale=1, transparency=True):
    obj = loader.loadModel('models/plane')
    obj.reparentTo(camera)
    obj.setScale(scale)
    obj.setPos(pos)
    obj.setBin('unsorted', 0)

    if transparency:
        obj.setTransparency(1)

    if tex:
        obj.setTexture(tex, 1)

    return obj


import nuke

import pipeline_nodes

import os

import delivery
import publish
import ih_config.manager

from helpers import get_presets


menubar = nuke.menu("Nuke")
m = menubar.addMenu(os.environ['IH_SHOW_CODENAME'])
n = m.addMenu("&Delivery")
for preset in get_presets():
    n.addCommand("%s"%preset, "delivery.deliver('%s')"%preset)

n.addCommand('MATTES',"nuke.createNode('IT_MATTES')")

n = m.addMenu("&Publish")
n.addCommand("Publish", "nuke.message(publish.publish(nuke.getFilename('Select folder to Publish')))")

m.addCommand("Reload Config", "ih_config.manager.loadConfig()")

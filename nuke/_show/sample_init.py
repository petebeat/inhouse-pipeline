import nuke

import sys

import os

#this is the path to the show's _pipeline/nuke folder
os.environ['SHOW_PATH'] = 'Z:\\13th_Floor\\_pipeline\\nuke\\'
#this is just to set the artist name, used by the delivery for slates.
os.environ['IH_ARTIST'] = 'Artist Name'
#this is the path to the config file. If all your paths are the same, this could be shared_elements
#you can also have a different one per artist to enable artists to work locally on their machines
#or a different one for windows vs mac users.
os.environ['CONFIG_PATH'] = 'Z:\\13th_Floor\\_pipeline\\nuke\\_show\\show_config.cfg'


if os.path.exists(os.environ['SHOW_PATH']):

    nuke.pluginAddPath(os.environ['SHOW_PATH'])

print "SHOW_PATH:",os.environ['SHOW_PATH']

print "ARTIST:",os.environ['IH_ARTIST']

print "CONFIG_PATH:",os.environ['CONFIG_PATH']

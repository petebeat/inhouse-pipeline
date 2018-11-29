#! usr/bin/python
import nuke
import os


print 'LOADING SHOW PIPELINE'
nuke.pluginAddPath('./ih_utils')
nuke.pluginAddPath('./ih_config')
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./color')

nuke.pluginAddPath('./_show/delivery')
nuke.pluginAddPath('./_show')

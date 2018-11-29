import nuke
import sys


import nukescripts
import delivery

print sys.argv[1]

import ih_utils.delivery.pipeline_nodes

nuke.scriptOpen(sys.argv[1])
for n in nuke.selectedNodes():
    n['selected'].setValue(False)

w=nuke.toNode("SHOT_WRITE")
w['selected'].setValue(True)

delivery.deliver('DPX_RENDER_AND_DELIVER_101',True)

nuke.scriptClose()

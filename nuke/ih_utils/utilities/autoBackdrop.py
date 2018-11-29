# Copyright (c) 2013 Varnish FX  All Rights Reserved.
#
# This example will automatically put a backdrop behind the selected nodes


import nuke, nukescripts, operator, random

def autoBackdrop():
	name=nuke.getInput("Label?")
	selNodes = nuke.selectedNodes()
	if not selNodes:
		return nuke.nodes.BackdropNode(label = name)
	
	n = nukescripts.autoBackdrop()
	n.knob("label").setValue(name) 
	xmin = n["xpos"].value()
	xmax = xmin+n["bdwidth"].value()
	ymin = n["ypos"].value()
	ymax = ymin+n["bdheight"].value()

	for node in nuke.selectedNodes():
	    x,y = node["xpos"].value(), node["ypos"].value()
	    if x>xmin and x<xmax and y>ymin and y<ymax and node.Class() == "BackdropNode":
		new= nuke.clone(node)
		nuke.delete(node)
		new["xpos"].setValue(x)
		new["ypos"].setValue(y)






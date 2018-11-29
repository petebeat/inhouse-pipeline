import nuke, nuke.rotopaint as rp, _curvelib as cl

def create_linked_layer(tracker_node, roto_node=False):
	'''
	Creates a layer in roto_node linked to tracker_node
	if roto_node is False, creates a roto node next to tracker node to link to
	'''
	grid_x = int(nuke.toNode('preferences').knob('GridWidth').value())
	grid_y = int(nuke.toNode('preferences').knob('GridHeight').value())
 
	tracker_name = tracker_node.name()
 
	# If Roto node not selected, create one.
	if not roto_node:
		roto_node = nuke.nodes.Roto()
		roto_node.setXYpos(tracker_node.xpos()-grid_x*1, tracker_node.ypos()-grid_y*0)
 
	# Create linked layer in Roto Node
	curves_knob = roto_node["curves"]
	stab_layer = rp.Layer(curves_knob)
	stab_layer.name = "stab_"+tracker_name
 
	trans_curve_x = cl.AnimCurve()
	trans_curve_y = cl.AnimCurve()
 
	trans_curve_x.expressionString = "parent.{0}.translate.x".format(tracker_name)
	trans_curve_y.expressionString = "parent.{0}.translate.y".format(tracker_name)
	trans_curve_x.useExpression = True
	trans_curve_y.useExpression = True
 
	rot_curve = cl.AnimCurve()
	rot_curve.expressionString = "parent.{0}.rotate".format(tracker_name)
	rot_curve.useExpression = True
 
	scale_curve = cl.AnimCurve()
	scale_curve.expressionString = "parent.{0}.scale".format(tracker_name)
	scale_curve.useExpression = True
 
	center_curve_x = cl.AnimCurve()
	center_curve_y = cl.AnimCurve()
	center_curve_x.expressionString = "parent.{0}.center.x".format(tracker_name)
	center_curve_y.expressionString = "parent.{0}.center.y".format(tracker_name)
	center_curve_x.useExpression = True
	center_curve_y.useExpression = True
 
	# Define variable for accessing the getTransform()
	transform_attr = stab_layer.getTransform()
	# Set the Animation Curve for the Translation attribute to the value of the previously defined curve, for both x and y
	transform_attr.setTranslationAnimCurve(0, trans_curve_x)
	transform_attr.setTranslationAnimCurve(1, trans_curve_y)
	# Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
	# http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
	transform_attr.setRotationAnimCurve(2, rot_curve)
	transform_attr.setScaleAnimCurve(0, scale_curve)
	transform_attr.setScaleAnimCurve(1, scale_curve)
	transform_attr.setPivotPointAnimCurve(0, center_curve_x)
	transform_attr.setPivotPointAnimCurve(1, center_curve_y)
	curves_knob.rootLayer.append(stab_layer)


def linkTrackToRoto():
	sel = nuke.selectedNodes()
	if len(sel)<2:
		if sel[0].Class()!="Tracker4":
			nuke.message("Select the tracker node and (optionally) a roto/paint to link it to")
		else:
			create_linked_layer(sel[0])
	else:

		if sel[1].Class()!="Tracker4":
			nuke.message("You must select a tracker first")
		else:



			if sel[0].Class()=="Roto" or sel[0].Class()== "RotoPaint":

			    create_linked_layer(sel[1],sel[0])
		    
			else:
			    nuke.message("your second selection must be a roto node, or nothing")      


		


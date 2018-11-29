import sys
import os.path
import nuke
import nukescripts

import autoBackdrop
from SetEnabledByName import *
from utilities import *
from vclf_multi_autotrack import *
import scaleDagNodes

import trackLinker


import RotoShapes_to_trackers

import quickload



menubar = nuke.menu("Nuke")
m = menubar.addMenu("InHouse")
m.addCommand('Open Counts', "reveal_in_finder(os.environ['IH_PATH_COUNTS'])")
n = m.addMenu("&File")
n.addCommand("Read from Write", "read_from_write()", "#r")
n.addCommand("Reveal in Finder", "reveal_node_in_finder()", "^f")
b=n.addMenu("&Copy Read Node To")
b.addCommand("Copy Read To Scans", "copyReadToShot('SCANS')")
b.addCommand("Copy Read To Elements", "copyReadToShot('ELEMENTS')")
b.addCommand("Copy Read To Prerenders", "copyReadToShot('PRERENDERS')")
b.addCommand("Copy Read To Sequence Shared Elements", "copyReadToShot('SHARED_ELEMENTS')")
b.addCommand("Copy Read To Show Share Elements", "copyReadToShot('SHOW_ELEMENTS')")



n.addCommand("Copy Render To Shot","copyRenderToShot()")
n.addCommand("Get Shot QT","quickload.getShotQT()","#^f")
n.addCommand("Get Show Shot QT","quickload.getShowTreeShotQT()")
n.addCommand("Open Comp","quickload.openComp()","#^o")
n.addCommand("ML Fix Relative Paths","utilities.fix_relative_paths()")
n.addCommand("Create Prerender Write", "create_precomp_node()")
n = m.addMenu("&Time")
n.addCommand( 'Hold at Current Frame', 'nuke.createNode("FrameHold")["first_frame"].setValue( nuke.frame() )', 'alt+h', icon="FrameHold.png")

#tbmenu = m.addMenu("&Render")
#tbmenu.addCommand("Render with Deadline", DeadlineNukeClient.main, "")
#try:
#    if nuke.env[ 'studio' ]:
#        import DeadlineNukeFrameServerClient
#        tbmenu.addCommand("Reserve Frame Server Slaves", DeadlineNukeFrameServerClient.main, "")
#except:
#    pass

# n = m.addMenu("&Filter")
# n.addCommand("Gradient Blur", "nuke.createNode(\"GradientBlur.nk\")")
# n.addCommand("Weighted Blur", "nuke.createNode(\"WeightedBlur.nk\")")
# n.addCommand("Edge Scatter", "nuke.createNode(\'EdgeScatter\')")
# n.addCommand("Arri Alexa Grain", "nuke.createNode(\'ScannedGrainIH\')")

n=m.addMenu("&Utility")

n.addCommand('Named Auto Backdrop', lambda: autoBackdrop.autoBackdrop(), 'alt+b')
n.addCommand("Roto/Set name to roto paint stroke range","setNameToStrokesRange()")
n.addCommand("Set Enabled Range from Name","setEnabledByName()")
n.addCommand("Roto/How is your paint going?","makeSad()")
n.addCommand("Link Roto to Tracker","trackLinker.linkTrackToRoto()","alt+o")
n.addCommand("DAG/scale Nodes up", "scaleDagNodes.scaleNodes(1.1)","alt+=")
n.addCommand("DAG/scale Nodes down", "scaleDagNodes.scaleNodes(.9)","alt+-")
n.addCommand("Roto/RotoShapes To Trackers", "RotoShapes_to_trackers.RotoShape_to_Trackers()")
n.addCommand("Quick Label", "quickLabel()", "N")
n.addCommand("OpticalFlare Auto Multitrack", "vclf_multi_autotrack()")

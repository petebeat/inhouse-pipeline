import nuke


#sets an expression on the disabled knob based on the name of the node -- must be in teh format name_%dto%d currently has a 1000 frame offset to make the numbers more readable for shots starting at 1001
def setEnabledByName():
    for n in nuke.selectedNodes():
       
        frames=n.name().split("_")[-1].split("to")
        try:
            n['disable'].setExpression("(frame>=%d & frame<=%d)?0:1"%(int(frames[0])+1000,int(frames[1])+1000))
        except:
            nuke.message("nodes must be named in teh format name_(number)to(number), ie left_roto_13to134")

def setNameToStrokesRange():
	nds = nuke.selectedNodes()
	for sel in nds:
		if sel.Class() in ("RotoPaint","Roto"):
		    rt = sel['curves'].rootLayer
		    
		    
		    maxFrame=0
		    minFrame=100000
		    
		    for a in rt:
		        inFrame=a.getAttributes().getValue(1,"ltn")
		        outFrame=a.getAttributes().getValue(1,"ltm")
		        if inFrame<minFrame:
		            minFrame=inFrame
		        if outFrame>maxFrame:
		            maxFrame=outFrame
		    
		    sel['name'].setValue("%s_%dto%d" % (sel.name(),minFrame-1000,maxFrame-1000))
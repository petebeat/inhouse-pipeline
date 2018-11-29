import nuke

def scaleNodes(scale):
    nds=nuke.selectedNodes()
    minX=nds[0]['xpos'].getValue()
    minY=nds[0]['ypos'].getValue()
    maxX,maxY=minX,minY
    for n in nds:
        minX=min(minX,n['xpos'].getValue())
        minY=min(minY,n['ypos'].getValue())
        maxX=max(maxX,n['xpos'].getValue())
        maxY=max(maxY,n['ypos'].getValue())
    center = ((minX+maxX)/2,(minY+maxY)/2)

    for n in nds:
        offsetX=n['xpos'].getValue()-center[0]
        offsetY=n['ypos'].getValue()-center[1]

        n['xpos'].setValue(center[0]+offsetX*scale)
        n['ypos'].setValue(center[1]+offsetY*scale)

        if n.Class() =="BackdropNode":
            n['bdwidth'].setValue(n['bdwidth'].getValue()*scale)
            n['bdheight'].setValue(n['bdheight'].getValue()*scale)
            n['note_font_size'].setValue(n['note_font_size'].getValue()*scale)

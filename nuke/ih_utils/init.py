import nuke


nuke.pluginAddPath('./delivery')
nuke.pluginAddPath('./utilities')

def force24fps():
    nuke.root()['fps'].setValue(24)

def setupshot():
    for n in nuke.allNodes('NoOp'):
        if n.name()=='SETUP':
            print "PERFORMING INITIAL SHOT SETUP..."
            nuke.delete(n)
            nuke.delete(nuke.toNode('ModifyMetaData1'))
            nuke.delete(nuke.toNode('ModifyMetaData2'))
            nuke.root()['first_frame'].setValue(nuke.toNode('Read1')['first'].getValue()+16)
            nuke.root()['last_frame'].setValue(nuke.toNode('Read1')['last'].getValue()-16)

            pf = nuke.toNode('MAE_PLATE_FORMATTER_v2')
            
            nuke.delete(nuke.toNode('MAE_PLATE_FORMATTER_v2'))
            nuke.scriptReadFile(os.path.join(os.environ['IH_PATH_SERVER'],
                                '13th_Floor','_pipeline','nuke',
                                'ToolSets','mae_shared',
                                'mae_plate_formatter.nk'))

nuke.addOnScriptLoad(setupshot)


#nuke.knobDefault("Grade.black_clamp", "False")

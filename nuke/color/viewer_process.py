
import os

import nuke

import xml.etree.ElementTree as ET

from color.helpers import getCCCID

_CLEANUP = []

def create_viewer_proc(opt):
    '''
    viewerprocs act funny with expression cdl file paths so we will just set that
    value directly
    '''

    try:
        cccFile=os.environ['IH_PATH_CDL']
        print cccFile
        #cccId=getCCCID(cccFile)

        n = nuke.nodes.Show_luts(
                                    vieweroptions=opt,
                                    file=cccFile,
                                    )
    except:
        n = nuke.nodes.CheckerBoard2()
        _CLEANUP.append(opt)

    return n

def cleanup_failed_viewers():
    '''
    if for some reason a ViewerProcess failed to find a file or otherwise had an exception
    we will remove them from the menu instead of putting broken viewers
    '''

    for name in _CLEANUP:
        nuke.ViewerProcess.unregister(name)

def add_viewer_luts_from_gizmo():
    '''
    this function reads all of the vieweroptions from the Show_luts gizmo and
    creates a viewer process option for each one, using the names of the options
    as the different viewer functions
    '''


    n=nuke.nodes.Show_luts()
    options= n['vieweroptions'].values()
    nuke.delete(n)


    for opt in options:
        args = (opt,)
        nuke.ViewerProcess.register(opt,create_viewer_proc,args)



### enable these lines to enable the viewer process color integrations
add_viewer_luts_from_gizmo()
cleanup_failed_viewers()

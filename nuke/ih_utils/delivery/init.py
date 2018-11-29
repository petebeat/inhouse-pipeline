import nuke
import os

nuke.pluginAddPath(os.path.join(os.environ['SHOW_PATH'],'_show','presets'))


def fixTimelineWrite():
    if nuke.root().knob('timeline_write_node') is None:
        k=nuke.String_Knob('timeline_write_node')

        nuke.root().addKnob(k)
        nuke.root()['timeline_write_node'].setValue('SHOT_WRITE')





nuke.addOnScriptLoad(fixTimelineWrite)


import nuke

import manager

print "LOADING CONFIG"

manager.loadConfig()

nuke.addOnScriptLoad(manager.loadConfig)
nuke.addOnScriptSave(manager.loadConfig)

import os
import os.path as path
import ConfigParser
import re

import nuke

import __builtin__
__builtin__.CFG={}

def loadConfig():

    config_path=os.environ['CONFIG_PATH']
    print config_path
    config = ConfigParser.SafeConfigParser()
    config.read(config_path)
    for section in config.sections():
        CFG[section]={}
        for item in config.options(section):
            CFG[section][item]=config.get(section,item)
            global_name = 'IH_%s_%s' % (section,item)
            global_name = global_name.upper()

            os.environ[global_name]=config.get(section,item)


    populate_paths(shot_re_parse())


def shot_re_parse(script_name=None,regex=None):

    if not script_name:
        script_name = path.basename(nuke.root().name())

    if not regex:
        regex=CFG['re']['basename']

    match = re.search(regex,script_name)

    if match:
        ## setup the shotEnvSetup
        shot_info=match.groupdict()
        print "FOUND INFO FOR SHOT %s: INIT SHOTENV" % shot_info['fullname']
        for key,value in shot_info.iteritems():
            os.environ['IH_INFO_%s'%key.upper()]=value
            print 'SETTING: IH_INFO_%s to %s'%(key.upper(),value)


        return shot_info



def populate_paths(shot_info,prefix='IH_PATH_%s'):
    '''takes shot info dict and plugs it into all the various paths'''
    if shot_info:

        CFG['path']={}
        for key,raw_path in CFG['raw_path'].iteritems():

            populated_path=raw_path.format(**shot_info)
            os.environ[prefix%key.upper()]=populated_path
            CFG['path'][key]=populated_path
            print 'SETTING: %s to %s'%(prefix%key.upper(),populated_path)





if __name__ == '__main__':
    loadConfig()
    print CFG['path']

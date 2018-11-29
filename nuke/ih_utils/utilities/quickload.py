import string
import glob
import os
import nuke
import re



class PartialFormatter(string.Formatter):
    def __init__(self, missing='*', bad_fmt='!!'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val=None,field_name
        return val

    def format_field(self, value, spec):
        # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt
            else: raise


def parse_shotname(name):
    base_re=os.environ['IH_RE_SHORTNAME']
    match_dict=re.search(base_re,name).groupdict()
    return match_dict

def getShotQT():
    pfmt=PartialFormatter()
    sn=nuke.getInput('read qt from shotname:')
    if sn:
        shot_dict=parse_shotname(sn)

        print shot_dict

        path=pfmt.format(os.environ['IH_RAW_PATH_QT'],**shot_dict)
        print path
        qts=glob.glob(path)
        print qts
        sorted(qts)
        if os.path.exists(qts[-1]):
            n=nuke.createNode("Read")
            n['file'].fromUserText(qts[-1])


def openComp():
    pfmt=PartialFormatter()
    sn=nuke.getInput('open .nk from mono shotname:').upper()
    if sn:
        shot_dict=parse_shotname(sn)
        path=pfmt.format(os.environ['IH_RAW_PATH_NUKE'],**shot_dict)
        scripts=glob.glob(path)
        print sorted(scripts)
        nuke.scriptOpen(sorted(scripts)[-1])

import string

def getShowTreeShotQT():
    sn=string.upper(nuke.getInput('read highest v qt from _vfx shot_tree shotname:'))
    print sn
    path='/Volumes/monovfx/_vfx/SHOT_TREE/%s/%s/output/*_vfx.mov' %(sn[:3],sn)
    print path
    qts=glob.glob(path)
    print qts
    qt=sorted(qts)[-1]
    if os.path.exists(qt):
        n=nuke.createNode("Read")
        n['file'].fromUserText(qt)
    else:
        return 'Shot Not Found'

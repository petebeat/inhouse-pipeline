import os

import sys
import re
import shutil

import cdl_convert
import argparse

parser = argparse.ArgumentParser(description='this script scans folders to find cdl files and converts them to .cc files for nuke(maelstromvfx):')
parser.add_argument('-win', action="store_true", default=False, dest='windows_flag', help='use windows path')
parser.add_argument('search_path', action="store", help='path to start recursive search from')
parser.add_argument('-t', action="store_true", default=False, dest='test_mode',help="test mode: print output but don't move or rename anything")

cdl_re=r'(?P<shot>(?P<seq>[A-Z]{3})_[0-9]{4})_(fg|FG|Fg)[0-9]'
cdl_path='/Volumes/maelstromvfx/inhouse/To_Inhouse/SHOTS/{seq}/_CDLS/'




def convert_cdl(cdlfile,dest):
    cdl_convert.reset_all()
    ccc = cdl_convert.parse_cdl(cdlfile)
    cc = ccc.color_decisions[0].cc
    cc.id=dest['shot']
    destpath=cdl_path.format(**dest)

    if not os.path.exists(destpath):
        os.makedirs(destpath)
    cc.determine_dest('cc',destpath)
    cdl_convert.write_cc(cc)

def process_all_ccc(folder):
    for dirName, subdir, fileList in os.walk(folder):
        for fname in fileList:

            if os.path.splitext(fname)[1] == '.cdl':
                print 'Found: %s' %fname
                fullpath=os.path.join(dirName,fname)
                m = re.search(cdl_re,fname)
                if m:
                    gd = m.groupdict()
                    print 'Injesting %s' %fname
                    convert_cdl(fullpath,gd)
                    if os.path.exists(cdl_path.format(**gd)):
                        os.rename(fullpath,os.path.join(dirName,fname+'.injested'))
                    else:
                        print "creation error: %s"
                else:
                    print 'Skipping and Archiving: %s' %fname
                    os.rename(fullpath,os.path.join(dirName,fname+'.skipped'))



filere=r'(?P<fullname>(?P<shot>(?P<seq>[A-Z]{2})[0-9]{3}_[0-9]{4})_?(?P<type>[a-z]+)?_?(?P<version>v[0-9]{3})?)'





if __name__ == '__main__':
    args=parser.parse_args()
    TEST_MODE=args.test_mode
    if args.windows_flag:
        cdl_path='Z:/To_Inhouse/SHOTS/{seq}/_CDLS/'
    process_all_ccc(args.search_path)

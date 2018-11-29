
import nuke
import csv
import glob
import os
import datetime
import shutil
import sys
import subprocess

from color.helpers import getCCCID
from helpers import copytree

import cdl_convert


def cc_to_cdl_node(node):
        source_file=node['source_file'].getValue()
        dest_file=node['dest_file'].getValue()
        cc = cdl_convert.parse_cc(os.environ['IH_DELIVERY_CDL'])
        cdl = cdl_convert.ColorCollection()
        cdl.append_child(cc)
        cdl.set_to_cdl()
        with open(dest_file,'w') as f:
            f.write(cdl.xml)

def set_tc_node(node,inputnode='Input1'):
        tc_node=nuke.toNode(node['tc_node'].getValue())


        startcode=nuke.toNode(inputnode).metadata("input/timecode",nuke.thisGroup()['in_frame'].getValue())
        tc_node['startcode'].setValue(startcode)
        tc_node['frame'].setValue(nuke.thisGroup()['in_frame'].getValue())

def load_qt_node(node):
        qt_node=nuke.toNode(node['qt_node'].getValue())
        load_path=node['qt_path'].getEvaluatedValue()

        qt_node['file'].fromUserText(load_path)

def open_finder_node(node):

        file_path = node['path'].getValue()
        reveal_path = os.path.dirname(file_path)
        if os.path.splitext(file_path)[1] == ".mov":
            reveal_path = file_path
        if sys.platform == "darwin":
            subprocess.Popen(["/usr/bin/open", "-R", reveal_path])
        elif sys.platform == "linux2":
            subprocess.Popen(["/usr/bin/nautilus", "--browser", reveal_path])
        else:
            subprocess.Popen(["C:/Windows/explorer.exe", reveal_path])

def write_csv_node(node):

    headers=os.environ['IH_DELIVERY_CSV_HEADERS'].split(',')

    csv_file=node['csv_file'].getEvaluatedValue()
    if node['append_to_csv'].getValue():
        mode='a'
    else:
        mode='w'

    with open(csv_file, mode) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers,extrasaction='ignore')

        if node['write_header'].getValue():
            writer.writeheader()
        knob_dict={v.label():v.getValue() for k,v in node.knobs().iteritems()}
        writer.writerow(knob_dict)

def load_cccid_node(node):
    try:
        cdl_node=nuke.toNode(node['cdl_node'].getValue())
        cdl_path=node['cccfile'].getValue()
        #cdl_cccid=getCCCID(cdl_path)

        cdl_node['file'].setValue(cdl_path)
        #cdl_node['cccid'].setValue(cdl_cccid)
    except KeyError as e:
        nuke.message('Error: %s' % e)



def copy_files_node(node):

    source=node['source_file'].getValue()
    destination=node['destination'].getValue()

    print 'COPY %s to %s' %(source, destination)

    if node['sequence'].getValue():

        base = os.path.basename(source).split('.')[0] + "*" + os.path.splitext(source)[1]
        fileList = glob.glob(os.path.join(os.path.dirname(source), base))
    else:
        fileList = [source]

    print fileList

    dest = destination
    if not os.path.exists(dest):
        os.makedirs(dest)

    task = nuke.ProgressTask("Copying Files")
    fileCount = len(fileList)

    for count, imgfile in enumerate(fileList):
        task.setMessage("copying file: %d of %d" % (count, fileCount))
        task.setProgress(int(100 * (count / float(fileCount))))
        shutil.copy(imgfile, dest)



def move_files_node(node):

    source=node['source_file'].getValue()
    destination=node['destination'].getValue()
    if not os.path.exists(destination):
        try:
            os.makedirs(os.path.dirname(destination))
        except:
            pass
    shutil.move(source,destination)

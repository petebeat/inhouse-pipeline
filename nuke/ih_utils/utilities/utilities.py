#!/usr/bin/python

import os
import nuke
import nukescripts
import glob
import subprocess
import datetime
import xml.etree.ElementTree as etree
import shutil
import xml.dom.minidom as minidom
import socket
import re
import threading
import math
import sys
from operator import itemgetter

def create_precomp_node():
    name=nuke.getInput("PreComp Name")
    name=name.replace(' ', '_')
    path=os.environ['IH_PATH_SHOT']
    name='_'.join([os.environ['IH_INFO_SHOT'],name,os.environ['IH_INFO_VERSION']])
    path=os.path.join(path,'images','precomps',name,name+'.%04d.exr')

    w=nuke.createNode('Write')
    w['file'].setValue(path)
    w['file_type'].setValue('exr')
    w['create_directories'].setValue(True)
    w['channels'].setValue('all')

def quickLabel():
    sel = nuke.selectedNodes()[0]
    sel['label'].setValue(nuke.getInput('Enter Label Text'))

def getPixDir(style):
    typedict={'SCANS':'',
                'ELEMENTS':'',
                'PRERENDERS':'',
                'SHARED_ELEMENTS':'',
                'SHOW_ELEMENTS':'',
                }

    for key in typedict:
        print key
        typedict[key]=os.getenv('IH_PATH_%s'%key)

    return typedict[style]

def copyReadToShot(destination):
    s = nuke.selectedNodes()
    for node in s:
        if node.Class() == "Read":

            file = node['file'].getValue()
            base = os.path.basename(file).split('.')[0] + "*" + os.path.splitext(file)[1]

            fileList = glob.glob(os.path.join(os.path.dirname(file), base))
            print fileList
            dest = os.path.join(getPixDir(destination), os.path.basename(file).split('.')[0])
            while os.path.exists(dest):
                dest += "_1"
                print dest
            os.mkdir(dest)
            print dest
            task = nuke.ProgressTask("Copying Read To Shot Tree")
            fileCount = len(fileList)

            for count, imgfile in enumerate(fileList):
                task.setMessage("copying file: %d of %d" % (count, fileCount))
                task.setProgress(int(100 * (count / float(fileCount))))
                shutil.copy(imgfile, dest)
            node['file'].setValue(os.path.join(dest, os.path.basename(file)))


def copyRenderToShot():
    s = nuke.selectedNodes()
    for node in s:
        if node.Class() == "Write":

            file = node['file'].getValue()
            base = os.path.basename(file).split('.')[0] + "*" + os.path.splitext(file)[1]

            fileList = glob.glob(os.path.join(os.path.dirname(file), base))

            dest = os.path.join(getRenderDir(), os.path.basename(file).split('.')[0])
            if not os.path.exists(dest):
                os.mkdir(dest)
            task = nuke.ProgressTask("Copying Files")

            for count, imgfile in enumerate(fileList):
                shutil.copy(imgfile, dest)
                task.setProgress(int(count / float(len(fileList)) * 100))
            node['file'].setValue(os.path.join(dest, os.path.basename(file)))
        else:
            nuke.message("Selected write nodes will copy to the delivery folder for the shot")


def setup_luts():
    nuke.root()['defaultViewerLUT'].setValue("OCIO LUTs")
    nuke.root()['OCIO_config'].setValue("custom")


def copyFiles(render_path, exr_dest_fulldir):
    task = nuke.ProgressTask("Copy Files")
    task.setMessage("Copying files")
    fileList = glob.glob(os.path.join(os.path.dirname(render_path), r'*.exr'))

    for count, exrfile in enumerate(fileList):
        shutil.copy(exrfile, exr_dest_fulldir)
        if task.isCancelled():
            nuke.executeInMainThread(nuke.message, args=("Copy Cancelled!"))
            break;
        task.setProgress(float(count) / float(len(fileList)))


## makeSad() tells you how many roto/paint layers you have.
def makeSad():
    count = 0
    for sel in nuke.allNodes():
        if sel.Class() in ("RotoPaint", "Roto"):
            rt = sel['curves'].rootLayer
            count += len(rt)

    nuke.message("You have used %d paint strokes for only %d frames! You should feel very proud." % (
    count, (nuke.root()['last_frame'].getValue() - nuke.root()['first_frame'].getValue())))


# creates a read node from a write node.

def read_from_write():
    sel = None
    file_path = ""
    start_frame = 1000
    end_frame = 1001
    node = None
    xpos = 0
    ypos = 0
    try:
        sel = nuke.selectedNodes()
    except:
        print "INFO: No nodes selected."
        return
    for nd in sel:
        if nd.Class() != "Write":
            continue
        file_path = nd.knob("file").value()
        file_type = nd.knob("file_type").value()
        read_node = nuke.createNode("Read", "file {" + file_path + "}", inpanel=True)
        if os.path.exists(os.path.dirname(file_path)):
            if not file_type == "mov":
                image_ar = sorted(glob.glob(file_path.replace('%04d', '*')))
                if (len(image_ar) == 0):
                    start_frame = int(nuke.root().knob("first_frame").value())
                    end_frame = int(nuke.root().knob("last_frame").value())
                else:
                    start_frame = int(image_ar[0].split('.')[1])
                    end_frame = int(image_ar[-1].split('.')[1])
            read_node.knob("first").setValue(start_frame)
            read_node.knob("origfirst").setValue(start_frame)
            read_node.knob("last").setValue(end_frame)
            read_node.knob("origlast").setValue(end_frame)
            read_node.knob("colorspace").setValue(re.search(r"(?:default \()?([\w\d]+)\)?",nd.knob("colorspace").value()).group(1))
            read_node.knob("raw").setValue(nd.knob("raw").value())
        xpos = nd.knob("xpos").value()
        ypos = nd.knob("ypos").value()
        read_node.knob("xpos").setValue(xpos)
        read_node.knob("ypos").setValue(ypos + 100)
        return read_node


# reveals the currently selected read or write node in the finder

def reveal_in_finder(reveal_path):
    if sys.platform == "darwin":
        subprocess.Popen(["/usr/bin/open", "-R", reveal_path])
    elif sys.platform == "linux2":
        subprocess.Popen(["/usr/bin/nautilus", "--browser", reveal_path])
    else:
        subprocess.Popen(["C:/Windows/explorer.exe", reveal_path])

def reveal_node_in_finder():
    sel = None
    try:
        sel = nuke.selectedNode()
    except:
        print "WARN: No nodes selected."
        return
    if not sel.Class() == "Write" and not sel.Class() == "Read":
        print "WARN: Please select either a read or a write node."
        return
    file_path = sel.knob("file").evaluate()
    reveal_path = os.path.dirname(file_path)
    reveal_in_finder(reveal_path)




def fix_relative_paths():
    for a in nuke.allNodes():
        try:
            print a['file'].getValue()
            a['file'].setValue(a['file'].getValue().replace("..",os.path.dirname(nuke.root()['project_directory'].evaluate())))
        except:
            print 'pass'
            pass

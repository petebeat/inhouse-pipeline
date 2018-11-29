#### Package Script
#version: v001
#date: 12/9/14



import os
import shutil
import math
import nuke
import threading
import random
import nukescripts
import re
import sys
import glob
import datetime
import xml.etree.ElementTree as etree
import xml.dom.minidom as minidom


def get_delivery_directory(str_path):
    calc_folder = ""
    lst_path = str_path.split('/')
    re_pattern = r'^inhouse$'
    path_idx = 0
    for path_component in lst_path:
        path_idx += 1
        mo = re.search(re_pattern, path_component)
        if not mo == None:
            break
    return_path_lst = lst_path[0:path_idx]
    return_path_lst.extend([lst_path[path_idx], '..', 'from_inhouse'])
    delivery_folder = os.path.normpath(os.path.sep.join(return_path_lst))
    tday = datetime.date.today().strftime('%Y%m%d')
    matching_folders = glob.glob(os.path.join(delivery_folder, "%s_*" % tday))
    noxl = ""
    max_dir = 0
    if len(matching_folders) == 0:
        calc_folder = os.path.join(delivery_folder, "%s_1" % tday)
    else:
        for suspect_folder in matching_folders:
            csv_spreadsheet = glob.glob(os.path.join(suspect_folder, "*.csv"))
            excel_spreadsheet = glob.glob(os.path.join(suspect_folder, "*.xls*"))
            if len(excel_spreadsheet) == 0 and len(csv_spreadsheet) == 0:
                noxl = suspect_folder
            else:
                dir_number = int(os.path.basename(suspect_folder).split('_')[-1])
                if dir_number > max_dir:
                    max_dir = dir_number
        if noxl != "":
            calc_folder = noxl
        else:
            calc_folder = os.path.join(delivery_folder, "%s_%d" % (tday, max_dir + 1))
    if sys.platform == "win32":
        if "/Volumes/monovfx" in calc_folder:
            calc_folder = calc_folder.replace("/Volumes/monovfx", "Y:")
    return calc_folder

def replaceGizmoWithGroup(node):
	### replaceGizmoWithGroup - takes a single node as input and if it is a gizmo, converts it into a group and replaces the old group.
	### Preserves the original selection state
	### requires nukescripts

    if isinstance(node, nuke.Gizmo):
        selection=nuke.selectedNodes()
        nukescripts.clear_selection_recursive()

        name=node['name'].getValue()
        inputs=node

        node.setSelected(True)




        group=node.makeGroup()

        group['xpos'].setValue(node['xpos'].getValue())
        group['ypos'].setValue(node['ypos'].getValue())

        for i in range (0,node.inputs()):
            group.setInput(i,node.input(i))

        for n in selection:
            n.setSelected(True)

        sel=node['selected'].getValue()
        nuke.delete(node)

        group['name'].setValue(name)
        group.setSelected(sel)


def setupOutputFolder(script, output):
    ### creates the folders for script package
    output=os.path.join(output,os.path.basename(os.path.splitext(script)[0])+"_nk")
    ### requires os
    osdir = nuke.callbacks.filenameFilter(output)
    folders= {
    			 'project':output,
                 'comp':os.path.join(output,'comp/'),
                 'source':os.path.join(output,'source/'),
                 'sequences':os.path.join(output,'source/sequences/'),
                 'stills':os.path.join(output,'source/stills/'),
                 'misc':os.path.join(output,'source/misc/'),
                 'cdl':os.path.join(output,'cdl/')
             }
    #print folders
    for folder in folders:
         try:
             #print "INFO: creating %s" % folders[folder]
             os.makedirs (folders[folder])
         except OSError:
             #print "ERROR: could not create %s" % folders[folder]
             pass
    #print folders['project']
    return folders

def fixName(name):
	return name.replace("Video 1","plate").replace(" ","_")

def sortOutput(path, folders):
	### returns the path to the folder where the file should go based on its file extension
	ext=os.path.splitext(path)[1]
	basename=os.path.basename(path)
	seq=re.search(r'(%\d+[d,D])',basename)
	folder=""
	if ext in {
				'.exr',
				'.jpg',
				'.dpx',
				'.mov',
				'.mp4',
				'.tif',
				'.tiff',
				'.png',
				'.hdr'
				}:
		if seq or ext=='.mov':
			folder=os.path.join(folders['sequences'],basename.replace('%','_').replace('.','_'))
		else:
			folder=folders['stills']
	else:
		if ext=='.nk':
			folder=folders['comp']
		elif ext=='.cdl':
			folder=folders['cdl']
		else:
			if seq:
				folder=os.path.join(folders['sequences'],basename.replace('%','_').replace('.','_'))
			else:
				folder=folders['misc']

	return folder

def saveScriptToOutput(folders):

	outputName=os.path.join(folders['comp'],os.path.basename(nuke.scriptName())[:-3]+"_collected.nk")

	nuke.scriptSaveAs(outputName, overwrite=True)


def processScript(scriptFile,folders):
	### goes through the nuke script and prep's it for transfer.
	fileList = []
	preComps = []
	blastList =[]
	nuke.scriptOpen(scriptFile)




	for a in nuke.allNodes():
		if isinstance(a, nuke.Gizmo):
			replaceGizmoWithGroup(a)
		if isinstance(a,nuke.Viewer):
			nuke.delete(a)


	for n in nuke.allNodes():


		if "Write" not in n.Class() and "SmartVector" not in n.Class():
			for k in n.knobs():

				if isinstance(n[k],nuke.File_Knob):
					#print n,n[k]
					dep=n.dependent()
					if n[k].getValue():
						if len(n.dependent())>0:
							filePath=n[k].getValue()
							if not "/elements/grain_plates/" in filePath:
								#print fixName(filePath)
								rePathFolder=sortOutput(fixName(filePath),folders)

								#print rePathFolder

								newValue=os.path.join(rePathFolder,os.path.basename(fixName(filePath))).replace(folders['project'],".")
								#print newValue
								n[k].setValue(newValue)

								if n.Class()=='Precomp':
									preComps.append(filePath)
								else:
									fileList.append(filePath)
						else:
							blastList.append(n)


	nuke.root()['project_directory'].setValue('[file dirname [python {nuke.script_directory()}]]')

	for b in blastList:
		#print "INFO: deleting unused node %s" %b.name()
		nuke.delete(b)



	saveScriptToOutput(folders)
	nuke.scriptClose()

	preCompsSet=set(preComps)
	for pk in preCompsSet:
		fileList.extend(processScript(pk,folders))



	return fileList




def copyFiles(fileList,folders):
    fileSet=set(fileList)

    totalSources=len(fileSet)

    for n,f in enumerate(fileSet, start=1):

        search,seq=re.subn(r'(%[0-9]+d)','*',f)

        fileSeq=glob.glob(search)

        folder=sortOutput(fixName(f),folders)
        if os.path.exists(folder):
            folder=folder+'_%d' % (n)
            os.makedirs(folder)
        else:
            os.makedirs(folder)

        total=len(fileSeq)
        for count,imgFile in enumerate(fileSeq,start=1):
        ### DONT CHANGE THIS FORMATTING, interactive progress bar depends on it.
            sys.stdout.write("INFO: copying file %d of %d of source %d of %d - %s\n" % (count,total,n,totalSources,imgFile))
            try:
                os.link(imgFile,os.path.join(folder,os.path.basename(fixName(imgFile))))
            except:
                print "FILE SKIPPED"
                pass
    sys.stdout.flush()



def shot_from_nuke_path(str_path):
    rval = ""
    lst_path = str_path.split('/')
    re_pattern = r'^[A-Z]{3}[0-9]{4}$'
    for path_component in lst_path:
        mo = re.search(re_pattern, path_component)
        if not mo == None:
            rval = path_component
    return rval


def cdl_file_from_nuke_path(str_path):
    rval = ""
    shot = shot_from_nuke_path(str_path)
    lst_path = str_path.split('/')
    re_pattern = r'^[A-Z]{3}[0-9]{4}$'
    path_idx = 0
    for path_component in lst_path:
        path_idx += 1
        mo = re.search(re_pattern, path_component)
        if not mo == None:
            break
    return_path_lst = lst_path[0:path_idx]
    return_path_lst.extend(['data', 'cdl', '%s.cdl' % shot])
    rval = '/'.join(return_path_lst)
    if sys.platform == "win32":
        if "/Volumes/monovfx" in rval:
            rval = rval.replace("/Volumes/monovfx", "Y:")
    return rval


def createSubmissionXML(scriptFile,deliverTo):

		# dont change these names! submission scripts depend on it.
		new_submission = etree.Element('ShotPKGSubmission')
		sht_se = etree.SubElement(new_submission, 'Shot')
		sht_se.text = os.path.basename(scriptFile)



		# write out xml file to disk
		xml_filepath=os.path.join(deliverTo,shot_from_nuke_path(scriptFile)+'_pkg.xml')
		prettyxml = minidom.parseString(etree.tostring(new_submission)).toprettyxml(indent="  ")
		xml_ds = open(xml_filepath, 'w')
		xml_ds.write(prettyxml)
		xml_ds.close()


def package_execute_threaded(s_nuke_script_path):
    # hard coded Nuke executable path, because we're classy like that
    progress_bar = nuke.ProgressTask("Packaging Script")
    progress_bar.setMessage("Initializing...")
    progress_bar.setProgress(0)


    s_nuke_exe_path = nuke.env['ExecutablePath']  # "/Applications/Nuke9.0v4/Nuke9.0v4.app/Contents/MacOS/Nuke9.0v4"
    s_pyscript = "/Volumes/monovfx/inhouse/zmonolith/SHARED/lib/nuke/nuke_pipeline/package_script.py"

    s_cmd = "%s -i -V 2 -t %s %s" % (s_nuke_exe_path, s_pyscript, s_nuke_script_path)
    s_err_ar = []
    f_progress = 0.0
    print "INFO: Beginning: %s" % s_cmd
    proc = subprocess.Popen(s_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while proc.poll() is None:
        try:
            s_out = proc.stdout.readline()
            print s_out.rstrip()
            s_err_ar.append(s_out.rstrip())
            if not s_out.find("INFO: copying file") == -1:
                s_line_ar = s_out.split(" ")
                (f_frame_cur, f_frame_tot, f_source_cur, f_source_tot) = (
                float(s_line_ar[3]), float(s_line_ar[5]), float(s_line_ar[8]), float(s_line_ar[10]))
                f_progress = ((f_frame_cur / f_frame_tot) * (1 / f_source_tot)) + ((f_source_cur - 1) / f_source_tot)
                progress_bar.setMessage("Copying: %s" % s_line_ar[-1])
                progress_bar.setProgress(int(f_progress * 100))
        except IOError:
            print "IOError Caught!"
            var = traceback.format_exc()
            print var
    if proc.returncode != 0:
        s_errmsg = ""
        s_err = '\n'.join(s_err_ar)
        if s_err.find("FOUNDRY LICENSE ERROR REPORT") != -1:
            s_errmsg = "Unable to obtain a license for Nuke! Package execution fails, will not proceed!"
        else:
            s_errmsg = "An unknown error has occurred. Please check the STDERR log above for more information."
        nuke.critical(s_errmsg)
    else:
        print "INFO: Successfully completed script packaging."


# add this one to menu.py
def menu_package_script():
    nuke.scriptSave()
    s_script_name = "%s" % nuke.scriptName()
    threading.Thread(target=package_execute_threaded, args=[s_script_name]).start()



def packageScript(scriptFile):
	#print "INFO: Packaging %s" %(nuke.root().name())


	deliverTo=get_delivery_directory(scriptFile)
	##deliverTo="/tmp/tst/"
	folders=setupOutputFolder(scriptFile,deliverTo)


	fileList=processScript(scriptFile,folders)
	fileList.append(cdl_file_from_nuke_path(scriptFile))

	copyFiles(fileList,folders)

	createSubmissionXML(scriptFile,deliverTo)

if __name__ == "__main__":

	packageScript(sys.argv[1])

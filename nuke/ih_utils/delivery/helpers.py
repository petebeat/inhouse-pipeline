import nuke
import csv
import glob
import os
import datetime
import shutil


from color.helpers import getCCCID

def get_presets():
    '''searches the delivery presets folder and returns a list of the gizmo names'''
    presetpath=os.environ['IH_DELIVERY_PRESETS']
    search=os.path.join(presetpath,'*.gizmo')
    presets=glob.glob(search)
    out=[os.path.splitext(os.path.basename(path))[0] for path in presets]
    print 'FOUND PRESETS: %s' %out
    return out


def get_delivery_directory():
    calc_folder = ""


    delivery_folder=os.environ['IH_SHOW_OUTPUT_FOLDER']
    print delivery_folder

    if os.path.exists(delivery_folder):
        tday = datetime.date.today().strftime(os.environ['IH_DELIVERY_FOLDER_STRING'])
        matching_folders = glob.glob(os.path.join(delivery_folder, "%s*"%tday))
        dest_folder = ""
        max_dir = -1
        dest_folder=""
        alpha='bcdefghijklmnopqrstuvxyz'
        if len(matching_folders) == 0:
            calc_folder = os.path.join(delivery_folder, "%s"%tday)
            noxl =""
        else:
            for suspect_folder in matching_folders:
                csv_spreadsheet = glob.glob(os.path.join(suspect_folder, "*.csv"))
                excel_spreadsheet = glob.glob(os.path.join(suspect_folder, "*.xls*"))
                if len(excel_spreadsheet) == 0 and len(csv_spreadsheet) == 0:
                    dest_folder = suspect_folder

                else:
                    dir_number = alpha.find(os.path.basename(suspect_folder)[-1])
                    if dir_number > max_dir:
                        max_dir = dir_number
            if dest_folder != "":
                calc_folder = os.path.normpath(dest_folder)
            else:
                calc_folder = os.path.normpath(os.path.join(delivery_folder, "%s%s"%(tday, alpha[max_dir+1])))
        return calc_folder



def copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2):

    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)

        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore, copy_function)
            else:
                copy_function(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            print srcname, dstname, str(why)
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError as why:

        errors.extend((src, dst, str(why)))
    if errors:
        raise Exception(errors)

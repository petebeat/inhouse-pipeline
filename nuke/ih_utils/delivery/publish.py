#!/usr/bin/python

# designed to receive a directory path from stdin, and create a conflagration-specific
# delivery package. reads all of the XML files within a directory, creates a CSV, and an
# ALE. Prints the name of the delivery file to stdout.

import sys
import os
import glob
import xml.etree.ElementTree as ET
import pprint
import datetime
import csv
import copy
import shutil
import smtplib

# mime/multipart stuff
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate



class ALEWriter():

    ale_fh = None
    header_list = None

    def __init__(self, input_filehandle):
        self.ale_fh = input_filehandle

    # takes an array containing the names of the column headings.
    # example: column_header_list = ['Name', 'Tracks', 'Start', 'End', 'Tape', 'ASC_SOP', 'ASC_SAT', 'frame_range']
    # write_header(column_header_list)
    def write_header(self, column_headers):
        self.header_list = column_headers
        header_string = '\t'.join(self.header_list)
        ale_header = """Heading
FIELD_DELIM	TABS
VIDEO_FORMAT	1080
TAPE	MLIH_AVID
FPS	24

Column
%s

Data
"""%(header_string)
        self.ale_fh.write(ale_header)
        return

    # takes an array of arrays. the master array contains a list of arrays, which represent individual rows in
    # the table. the individual rows contain values that match the headers provided to the write_header method.
    def write_data(self, row_data_list):
        for row in row_data_list:
            row_match_list = []
            for col_hdr in self.header_list:
                row_match_list.append(row[col_hdr])
            self.ale_fh.write('\t'.join(row_match_list))
            self.ale_fh.write('\n')
        return

##USES GLOBALS FROM TOP
def send_email(delivery_directory, file_list,attachments):

    DISTRO_LIST_TO=os.environ['IH_EMAIL_DISTRO_LIST_TO'].split(',')
    DISTRO_LIST_CC=os.environ['IH_EMAIL_DISTRO_LIST_CC'].split(',')
    MAIL_FROM=os.environ['IH_EMAIL_MAIL_FROM']
    MAIL_FROM_ADDRESS=os.environ['IH_EMAIL_MAIL_FROM_ADDRESS']
    MAIL_USERNAME=os.environ['IH_EMAIL_MAIL_USERNAME']
    MAIL_PASSWORD=os.environ['IH_EMAIL_MAIL_PASSWORD']
    MAIL_SMTP_SERVER=os.environ['IH_EMAIL_MAIL_SMTP_SERVER']

    formatted_list= "\r\n".join(file_list)

    msg="Hello Team,\n\
\n\
The following shots are ready in %s:\n\
\n\
%s\n\
\n\
Enjoy!\n\
\n\n" %(delivery_directory, formatted_list)
    print msg
    email = "\r\n".join([
        "From: %s"% MAIL_FROM,
        "To: %s" %", ".join(DISTRO_LIST_TO),
        "Cc: %s"%", ".join(DISTRO_LIST_CC),
        "Subject: In-house delivery: %s" %os.path.split(delivery_directory)[-1]
        ,
        msg
    ])

    mime_msg = MIMEMultipart()
    mime_msg['from'] = MAIL_FROM
    mime_msg['to'] = COMMASPACE.join(DISTRO_LIST_TO)
    mime_msg['cc'] = COMMASPACE.join(DISTRO_LIST_CC)
    mime_msg['subject'] = "In-house delivery: %s" %os.path.split(delivery_directory)[-1]
    mime_msg.attach(MIMEText(msg))

    for f in attachments or []:
        with open(f, "rb") as fil:
            mime_msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % os.path.basename(f),
                Name=os.path.basename(f)
            ))

    fromaddr=MAIL_FROM_ADDRESS
    toaddrs=DISTRO_LIST_CC + DISTRO_LIST_TO
    print toaddrs


    # The actual mail send
    server = smtplib.SMTP(MAIL_SMTP_SERVER)
    server.starttls()
    server.login(MAIL_USERNAME,MAIL_PASSWORD)
    server.sendmail(fromaddr, toaddrs, mime_msg.as_string())
    server.quit()

    return email


def publish(delivery_folder):
    headers=os.environ['IH_DELIVERY_CSV_HEADERS'].split(',')

    delivery_folder_name=os.path.basename(os.path.dirname(delivery_folder))

    output_file=os.path.join(delivery_folder,"%s.csv"%delivery_folder_name)
    file_list=[]

    subs=glob.glob('%s*.txt'%delivery_folder)

    with open(output_file, 'wb') as outcsv:
        writer = csv.DictWriter(outcsv,fieldnames=headers,extrasaction='ignore')
        writer.writeheader()
        for sub in subs:
            with open(sub) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    file_list.append(row['Filename']+'.'+row['Format'])
                    writer.writerow(row)

    hidden_xml_dir = os.path.join(delivery_folder, ".delivery")
    if not os.path.exists(hidden_xml_dir):
        os.makedirs(hidden_xml_dir)

    for sub in subs:
        shutil.move(sub, os.path.join(hidden_xml_dir, os.path.basename(sub)))

    return send_email(delivery_folder,file_list,[output_file])





if sys.platform == "Darwin":
    import Tkinter as tk
    import tkFileDialog



    if __name__ == "__main__":
        root = tk.Tk()
        root.withdraw()
        file_path = tkFileDialog.askdirectory()
        if file_path:
            deliver(file_path)

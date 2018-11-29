# inhouse-pipeline
a basic nuke pipeline for feature film inhouse vfx work


This pipeline is pretty bare bones and was setup specifically for the needs of inhouse artists working either on a shared server, or locally on their own machines, to automate the process of delivering shots back to production while applying the color, slates, burnins, and providing subforms and submission emails.

When this pipeline was in use the ingest and nuke script creation was handled with nuke studio, so there is nothing much for ingest here. (I do have a seperate ingest sorting tool, but its not up yet) There are a few things in the /bash folder that are command line scripts mostly to help with doing cdl stuff and converting them into formats that nuke can use.

The entire goal of this project was to make a system that was both super flexible for various formats and delivery specs and very fast to setup. Usually requiring little or no changes to python code to impliment for any given delivery/show spec. Ideally also the whole thing can be spun up in about a day or less (depending on complexity).

I've tried to include some documentation here and there, and hopefully ill get around to filling in more, but if you want to attempt to use the pipeline let me know and i'm pretty happy to give some pointers.

here is a quick guide to setting up the pipeline... more info is availible in the various readme's inside the repo as well.


# Pipeline config steps
## Get pipeline installed
### 1.Copy _pipeline folder to local or remote location in your project folder. Specific location doesn’t matter.
### 2.Install code to point to pipeline in ~/.nuke/init.py
Sample code can be found in _pipeline/nuke/_shot/sample_init.py
The important 3 lines are the three os.environs at the top of that file. 
If everybody working on the show is going to have the same filepaths to a central server (ie all on osx mounting at /Volumes/XXX/) you can use just a single show_config. If you need to support a mixed environment, or local show folders, you can point the ‘CONFIG_PATH’ to different configs per person, or per os type.
If this worked when you launch nuke you should see messages printed into the console or script editor about show pipeline stuff being loaded.
## Setup show_config.cfg
Almost everything in show config is optional, because it all gets used mostly only in the delivery templates what you set here or not mostly only matters for what you need to use. Its helpful to note that you can use the %(name)s syntax for the .cfg file to reference other entries. Only ones in the DEFAULT section are accessable from everywhere but internal to a [section] you can use them.
### 1.set the DEFAULT section to point to the root of your show
-Root_folder is a good place to put the path to your shots directory
If you need to define a seperate server location for each artist, its possible here. (this gets used or not down below in the delivery section)

### 2.Set the [show] section
this section is just here to provide a place for things that needed to vary more than the more shot tree related paths below. Ideally this is where most of the show specific stuff goes.
### 3.Set the [raw_path] section
This is where you define all the paths for the whole show.
If there is a path that you need to care about that isnt in here, define it.
All of these with { } keys will get filled in based on the regex variables extracted from the nuke script name and put into environmental variables. In the nuke scripts they will be defined as IH_PATH_{NAME} and in the delivery system they will be in IH_DELIVERY_{NAME}. To use them in nuke just do the tcl expression [getenv IH_PATH_{NAME}] in say a writenode file knob. 
### 4.Setup the [re] section
Use regex101 to create a regex that can extract whatever variables from the nuke script name you need to fill in the { } keys you want to use in the raw_path section
### 5.Setup the [delivery] section
* Make presets point to the folder where you want to keep your delivery preset gizmos
* Update csv_headers to be the columns you want, in the order you want, in the sub forms.
* Font and font_bold are there for cross platform, you may not need them.
* set the folder_string to define what format your packages come in 
### 6.Setup the [email] section
Should be pretty explanitory… its the to, cc and froms for the submission emails and the smtp settings for an email server.
## Edit / Setup delivery templates
Use previous gizmos as an example.
* To develop add an existing delivery gizmo to the folder and run it in a nuke script that is in the proper pipeline location. This will set the IH_DELIVERY_ environment variables with the values from the raw_path config. You can use them to test the delivery preset and export it as a gizmo back to the delivery gizmo folder when you are done.
* Use the pipeline nodes to handle things like importing cdls, or moving finished renders to delivery folders, or exporting csv files.
## Setup Show_luts
If you dont want to use the viewer luts… comment out int addPluginPath(‘color’) line from the init.py file in _pipeline/nuke
Otherwise, edit the show_luts.gizmo from the nuke/_show folder. Each entry in the dropdown select will become a different viewer option


# You are done!


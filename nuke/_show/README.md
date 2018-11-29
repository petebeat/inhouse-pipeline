This _show folder is a template for all of the show specific configurations needed for this pipeline.

there are 4 things to setup for every show. This folder has samples of each.

1. __Artist's init.py__

  this is the individual init.py that lives on each artists workstation in their .nuke folder. This file sets the env variables
  and nuke path that loads the pipeline code and points to the show config. After setting this up it needs to be installed to each artist.
  
2. __Show_luts.gizmo__

  this is a nuke .gizmo file that defines the options availible in the nuke viewer lut menu. you can control what the options and their names are by changing the values of the select knob on the gizmo. inside the gizmo is a switch that is expression linked to flip between whatever image path you need for the various options. Be careful about updating the CDL portion of this, it is tied into some additional code in the color module that sets the CCCID.
  
3. __Delivery.gizmo(s)__

  all gizmos in the delivery gizmo folder (path is customizable in the .cfg) will be used as deliver options in the show menu. these gizmos can also contain 'pipeline nodes' that can do things like copy files, and write csv's for subforms. They mostly use environmental variables set from the show_config to define things like where to render. The gizmo's themselves have a few required knobs that are hooked into the delivery system code, but if you start from one of the samples you should be good to go. Hopefully i'll put together a more comprehensive explination of the delivery system at some point that explains better how to setup these gizmos.
  
4. __show_config.cfg__

This file is the heart of the configuration, it controls the settings for several things...
*the show regex. used to parse the shotnames and filenames for the pipeline and render systems
*all the required pipeline show paths. like the path to the delivery templates and the delivery destination.
*any optional paths that would be useful to either the delivery system or artists.
*the csv headers for subforms
*the delivery package date format
*the stmp email settings for automatically sending publish emails

some descriptions of the options are availible in the sample config provided.. yeah i know it needs way more.

the name of this file is definable in the aritst init.py, and there is nothing stopping you from having more than one per show. indeed you can have one per artist if each artist is working off their own storage with different file paths.
  

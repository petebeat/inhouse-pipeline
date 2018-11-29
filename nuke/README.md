This documentation is going to be far from complete... but here is a quick overview of what this pipeline gives you...

it has these modules

-___show__
  this pipeline tries to consolidate all of the show specific setup and configuration as much as possible into a single folder. This is to streamline new show setup and reduce code changes for show specific things (ie delivery settings). a sample of this folder is provided here. check out its readme for more info.
  
-__color__
  this module is mostly concered with providing show specific viewer process options in addition to the default srgb/rec709.
  the show specific color is all configured through a _show gizmo called Show_luts.gizmo
  
-__gizmos__
  this module just provides the existing luma dynamic gizmo loader, configured to work based on the show config path. any gizmos placed in any folder inside the luma folder will be dynamically added to the nuke session on load
  
-__ih_config__
  this module handles the loading of the show config files and the setting of the relevant environmental variables as defined by the show config.
  
-__ih_utils__
  this module contains the delivery system and a utilities folder with some generic helper utilities. The delivery system really needs its own whole doc. but the main thing in there to care about is the __pipeline_nodes.py__ that file defines the functions that are called by all of the Pipeline_ nodes in the delivery gizmos.

import nuke
from nukescripts.panels import PythonPanel as PP
import copy
import os
from ih_config import manager as cfg_manager
import helpers
import re

class SubmitPanel(PP):
    """automatically populates python panel with options from node"""
    def __init__(self,node):
        super(SubmitPanel, self).__init__(node['name'].getValue())
        self.node=node
        self.src_knobs=getUserKnobs(node)
        for knob in self.src_knobs[1:]:
            c=knob.Class()
            k=getattr(nuke,c)
            self.k=k(knob.name(),label=knob.label(),)
            self.k.setValue(knob.getValue())

            if knob.getFlag(nuke.STARTLINE):
              self.k.setFlag(nuke.STARTLINE)
            else:
              self.k.clearFlag(nuke.STARTLINE)
            self.addKnob(self.k)


    def finishModalDialog(self,result):
        super(SubmitPanel,self).finishModalDialog(result)
        if result:

            for src_knob in self.src_knobs[1:]:
                src_knob.setValue(self.knobs()[src_knob.name()].getValue())


        return result


def getUserKnobs(node):
    in_user_tab = False
    user_knobs = []
    for n in range(node.numKnobs()):
          cur_knob = node.knob(n)
          is_tab = isinstance(cur_knob, nuke.Tab_Knob)

          # Track is-in-tab state
          if is_tab and cur_knob.name() == "User": # Tab name to remove
              in_user_tab = True
          elif is_tab and in_user_tab:
              in_user_tab = False

          # Collect up knobs to remove later
          if in_user_tab:
              user_knobs.append(cur_knob)
    return user_knobs

def execute_preset(node,startNode='Input1'):
  ''' takes the export gizmo and renders/runs all the nodes'''

  def build_list(node):
    '''recurse through the node tree and build the list of exports that need to be run'''
    for n in node.dependent(nuke.INPUTS):

        if 'Write' == n.Class() or 'Pipeline' in n.name():
            #if not node['disable'].getValue():
            execute_list.append(n)
        build_list(n)


  def execute_node(node):


    if not node['disable'].getValue():

      if node.Class()=='Write':
        nuke.execute(node,int(node['first'].getValue()),
                            int(node['last'].getValue()))


      else:
          try:
            node['execute'].execute()
          except KeyError as e:
            nuke.message('Error: %s' % e)

  start=node.node(startNode)
  execute_list = []
  maxtries=1
  print "Build Execute list"
  while len(execute_list) == 0 and maxtries < 5:
    build_list(start)
    maxtries+=1
  print "Execute List took %d tries" % maxtries



  task = nuke.ProgressTask("Running: %s Preset" %node.name())
  
  print execute_list
  task.setProgress(0)
  taskCount=len(execute_list)
  for count,n in enumerate(execute_list):

      print n.name()
      task.setMessage(n['label'].getValue())
      try:
          execute_node(n)
      except:
          task.setProgress(100)
          nuke.message('ERROR: DELIVERY FAILED, check error log for any info')

          return
      task.setProgress(int(100 * (count / float(taskCount))))
  task.setProgress(100)


def populate_data(node):
  '''populates the preset with the extracted data and some standards like first and last frame'''
  input_node=node.dependencies(nuke.INPUTS)[0]

  input_path=input_node['file'].getEvaluatedValue()


  try:
    node['in_frame'].setValue(node.upstreamFrameRange(0).first())
    node['out_frame'].setValue(node.upstreamFrameRange(0).last())
    node['filepath'].setValue(input_path)
    node['delivery_path'].setValue(helpers.get_delivery_directory())



    match = re.search(os.environ['IH_RE_FULLREZ'],input_path)

    if match:

        shot_info=match.groupdict()

        print "FOUND INFO FOR SHOT %s: INIT DELIVERY ENV" % shot_info['fullname']
        for key,value in shot_info.iteritems():
            try:
                node[key].setValue(value)
            except NameError:
                pass

        cfg_manager.populate_paths(shot_info,'IH_DELIVERY_%s')

    else:
      nuke.message("Error: The Selected Source Does Not Appear To Be A Valid Shot")

  except NameError as e:
    nuke.message('This Preset Gizmo is missing a required Knob: %s' %e)

def populate_mattes(node):
    '''this is a hopefully temporary glue function to make the mattes delivery work

        it adds generates the mattes path based on the values of the matte gizmo
    '''
    matte_path=os.environ['IH_DELIVERY_MATTES']
    m_id=node['matte_file_id'].getValue()
    m_label1=node['matte1_label'].getValue()
    m_label2=node['matte2_label'].getValue()
    m_label3=node['matte3_label'].getValue()
    m_label4=node['matte4_label'].getValue()

    rez=node['rez'].getValue()
    fullname=node['fullname'].getValue()
    l=[m_label1,m_label2,m_label3,m_label4]

    labels='_'.join([a for a in l if a])
    matte_basepath='%s/multimattes/matte%i/%s_matte_%s.####.dpx' %(rez,m_id,fullname,labels)
    print matte_path
    print matte_basepath
    os.environ['IH_DELIVERY_MATTE_PATH']=os.path.join(matte_path,matte_basepath)
    node['mattepath'].setValue(os.path.join(matte_path,matte_basepath))


def deliver(preset, silent=False):
  '''runs the delivery procedure'''
  print 'Running %s' % preset


  try:
    node= nuke.selectedNode()
    os.environ['IH_SHOW_CODENAME']
  except KeyError:
    cfg_manager.loadConfig()
  except ValueError:
    nuke.message('select a node to deliver')
    return


  preset_gizmo=nuke.createNode(preset)
  preset_node=preset_gizmo.makeGroup()
  nuke.delete(preset_gizmo)

  preset_node.connectInput(0,node)
  populate_data(preset_node)

  if not silent:
      pnl=SubmitPanel(preset_node)
      if not pnl.showModalDialog():
        print "ABORT SUBMISSION"
        return

  execute_preset(preset_node)

  nuke.delete(preset_node)

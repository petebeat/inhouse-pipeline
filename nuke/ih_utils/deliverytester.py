import nuke
import nukescripts
import copy

class SubmitPanel(nukescripts.PythonPanel):
	"""automatically populates python panel with options from node"""
	def __init__(self,node):
		super(SubmitPanel, self).__init__('YoHoHo')
		self.node=node
		self.src_knobs=getUserKnobs(node)
		for knob in self.src_knobs[1:]:
			c=knob.Class()
			k=getattr(nuke,c)
			self.k=k(knob.name(),label=knob.label(),value=knob.getValue())
			
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


def testpanel():
	pnl=SubmitPanel(nuke.selectedNodes()[0])
	print 'mdal'
	print pnl.showModalDialog()



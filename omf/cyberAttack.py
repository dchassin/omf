from __future__ import print_function
class AlertAgent(object):
	__slots__ = 'agentName', 'alertTime'
	# e.g. "2000-00-03 12:00:00"
	
	def __init__(self, agentName, alertTime):
		self.agentName = agentName
		self.alertTime = alertTime

	def readStep(self, time):
		if time == self.alertTime:
			print('!!!!!Alerting because it is now ', self.alertTime, '!!!!!!!')
			return [{'cmd':'readClock'}]
		return []

	def writeStep(self, time, rezList):
		return []

class ReadAttackAgent(object):
	__slots__ = 'agentName', 'attackTime', 'obNameToAttack', 'obPropToAttack'
	# e.g. "2000-01-03 12:00:00", "tm_1", "measured_power"
	
	def __init__(self, agentName, attackTime, obNameToAttack, obPropToAttack):
		self.agentName = agentName
		self.attackTime = attackTime
		self.obNameToAttack = obNameToAttack
		self.obPropToAttack = obPropToAttack

	def readStep(self, time):
		if time == self.attackTime:
			return [{'cmd':'read','obName':self.obNameToAttack,'propName':self.obPropToAttack}]
		return []

	def writeStep(self, time, rezList):
		return []

class ReadMultAttackAgent(object):
	__slots__ = 'agentName', 'attackTime', 'obNameToAttack', 'obPropsToAttack'
	# e.g. "2000-01-03 12:00:00", "tm_1", ["measured_power","measured_real_energy"]
	# Agent has ability to return different read commands for multiple properties of an object in a time step

	def __init__(self, agentName, attackTime, obNameToAttack, obPropsToAttack):
		self.agentName = agentName
		self.attackTime = attackTime
		self.obNameToAttack = obNameToAttack
		self.obPropsToAttack = obPropsToAttack

	def readStep(self, time):
		if time == self.attackTime:
			readReqs = []
			for obProp in self.obPropsToAttack:
				readReqs.append({'cmd':'read','obName':self.obNameToAttack,'propName':obProp})
			return readReqs
		return []

	def writeStep(self, time, rezList):
		return []

class ReadIntervalAttackAgent(object):
	__slots__ = 'agentName', 'attackStartTime', 'attackEndTime', 'obNameToAttack', 'obPropToAttack'
	# e.g. "2000-01-02 08:00:00", "2000-01-03 08:00:00", "tm_1", "measured_real_energy"
	# reads the same object and property for each step between the given interval (attackStartTime and attackEndTime)
	
	def __init__(self, agentName, attackStartTime, attackEndTime, obNameToAttack, obPropToAttack):
		self.agentName = agentName
		self.attackStartTime = attackStartTime
		self.attackEndTime = attackEndTime
		self.obNameToAttack = obNameToAttack
		self.obPropToAttack = obPropToAttack

	def readStep(self, time):
		if time >= self.attackStartTime and time <= self.attackEndTime:
			return [{'cmd':'read','obName':self.obNameToAttack,'propName':self.obPropToAttack}]
		return []

	def writeStep(self, time, rezList):
		return []

class WriteAttackAgent(object):
	__slots__ = 'agentName', 'attackTime', 'obNameToAttack', 'obPropToAttack', 'propTarget'
	# e.g. e.g. "2000-01-02 16:00:00", "tm_1", "measured_real_energy", "0.0"

	def __init__(self, agentName, attackTime, obNameToAttack, obPropToAttack, propTarget):
		self.agentName = agentName
		self.attackTime = attackTime
		self.obNameToAttack = obNameToAttack
		self.obPropToAttack = obPropToAttack
		self.propTarget = propTarget

	def readStep(self, time):
		return [] # Doesn't need to read.

	def writeStep(self, time, rezList):
		if time == self.attackTime:
			#print '!!!!! Just changed the', self.obPropToAttack, 'of', self.obNameToAttack,'to',self.propTarget,'!!!!!!!!!'
			return [{'cmd':'write','obName':self.obNameToAttack,'propName':self.obPropToAttack,'value':self.propTarget}]	
		return []

class WriteMultAttackAgent(object):
	__slots__ = 'agentName', 'attackTime', 'obNameToAttack', 'obPropsAndTargets'
	# e.g. e.g. "agent1", "2000-01-02 16:00:00", "tm_1", [{"obPropToAttack":"measured_real_energy", "value":"0.0"}, {"obPropToAttack":"measured_power", "value":"0.0"}]

	def __init__(self, agentName, attackTime, obNameToAttack, obPropsAndTargets):
		self.agentName = agentName
		self.attackTime = attackTime
		self.obNameToAttack = obNameToAttack
		self.obPropsAndTargets = obPropsAndTargets

	def readStep(self, time):
		return [] # Doesn't need to read.

	def writeStep(self, time, rezList):
		if time == self.attackTime:
			writeReqs = []
			for obPropAndTarget in self.obPropsAndTargets:
				obProp = obPropAndTarget.get('obPropToAttack')
				propTarget = obPropAndTarget.get('value')
				writeReqs.append({'cmd':'write','obName':self.obNameToAttack,'propName':obProp,'value':propTarget})
			return writeReqs
		return []

class WriteIntervalAttackAgent(object):
	__slots__ = 'agentName', 'attackStartTime', 'attackEndTime', 'obNameToAttack', 'obPropToAttack', 'propTarget'
	# e.g. e.g. "2000-01-02 16:00:00", "tm_1", "measured_real_energy", "0.0"

	def __init__(self, agentName, attackStartTime, attackEndTime, obNameToAttack, obPropToAttack, propTarget):
		self.agentName = agentName
		self.attackStartTime = attackStartTime
		self.attackEndTime = attackEndTime
		self.obNameToAttack = obNameToAttack
		self.obPropToAttack = obPropToAttack
		self.propTarget = propTarget

	def readStep(self, time):
		return [] # Doesn't need to read.

	def writeStep(self, time, rezList):
		if time >= self.attackStartTime and time <= self.attackEndTime:
			#print '!!!!! Just changed the', self.obPropToAttack, 'of', self.obNameToAttack,'to',self.propTarget,'!!!!!!!!!'
			return [{'cmd':'write','obName':self.obNameToAttack,'propName':self.obPropToAttack,'value':self.propTarget}]	
		return []

class DefendByValueAgent(object):
	__slots__ = 'agentName', 'obNameToDefend', 'obPropToDefend', 'propTarget'
	# e.g. 'DefendByValueAgent1', "Test_inverter_1", "V_Out", "3.0"

	def __init__(self, agentName, obNameToDefend, obPropToDefend, propTarget):
		self.agentName = agentName
		self.obNameToDefend = obNameToDefend
		self.obPropToDefend = obPropToDefend
		self.propTarget = propTarget

	def readStep(self, time):
		return [{'cmd':'read','obName':self.obNameToDefend,'propName':self.obPropToDefend}]

	def writeStep(self, time, rezList):
		for rez in rezList:
			if (rez.get('obName') == self.obNameToDefend) and (rez.get('propName') == self.obPropToDefend):
				if rez.get('value') != self.propTarget:
					return [{'cmd':'write','obName':self.obNameToDefend,'propName':self.obPropToDefend,'value':self.propTarget}]
		return []

class CopycatAgent(object):
	__slots__ = 'agentName', 'attackTime', 'obNameToCopy', 'obPropToCopy', 'obDetailsToChange'
	# e.g. 'copycat1', 'solar_1', 'V_Out', [{'obNameToPaste':'solar_2', 'obPropToPaste': 'V_Out'}]

	def __init__(self, agentName, attackTime, obNameToCopy, obPropToCopy, obDetailsToChange):
		self.agentName = agentName
		self.attackTime = attackTime
		self.obNameToCopy = obNameToCopy
		self.obPropToCopy = obPropToCopy
		self.obDetailsToChange = obDetailsToChange

	def readStep(self, time):
		if time == self.attackTime:
			return [{'cmd':'read','obName':self.obNameToCopy,'propName':self.obPropToCopy}]
		return []

	def writeStep(self, time, rezList):
		if time == self.attackTime:
			for rez in rezList:
				if (rez.get('obName') == self.obNameToCopy) and (rez.get('propName') == self.obPropToCopy):
					writeReqs = []
					for obNameAndProp in self.obDetailsToChange:
						obNameToPaste = obNameAndProp.get('obNameToPaste')
						obPropToPaste = obNameAndProp.get('obPropToPaste')
						writeReqs.append({'cmd':'write','obName':obNameToPaste,'propName':obPropToPaste,'value':rez.get('value')})
					return writeReqs
		return []
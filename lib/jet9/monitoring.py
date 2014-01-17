"""
Jet9 Cluster monitoring routines
"""

import os
import logging

LOG = logging.getLogger("jet9." + __name__)

class ClusterMonitorEvent(object):
	"""Monitoring event class"""

	def __init__(self, desc):
		self.desc = desc
		self.callback = None
		self.params = {}

	def set_desc(self, desc):
		"""Set description (short name) for event"""

		self.desc = desc

	def set_callback(self, callback):
		"""Set event's callback:
		callback exec: callback(nodename)
		"""
		self.callback = callback
		
	def set_param(self, env, val):
		"""Set condition parameters for event filtering"""

		self.params[env] = val
	
	def get_params(self):
		"""Get parameters dict"""

		return self.params

class ClusterMonitor(object):
	"""Cluster monitoring class"""

	def __init__(self):
		self.events = []
		pass

	def add_event(self, event):
		"""Add event to queue monitoring"""

		return self.events.append(event)
	
	def execute(self):
		"""Process monitoring exec"""

		if os.environ.has_key("CRM_notify_node") == False:
			return None

		LOG.debug("%s %s %s %s %s %s %s %s" % tuple(map(lambda x: os.environ[x], """CRM_notify_recipient
CRM_notify_node
CRM_notify_rsc
CRM_notify_task
CRM_notify_desc
CRM_notify_rc
CRM_notify_target_rc
CRM_notify_status""".split("\n"))))
		
		node = os.environ["CRM_notify_node"]

		for event in self.events:
			found = 1
			for (env, val) in event.get_params().items():
				if os.environ[env] != val:
					found = 0
					break

			if found == 0:
				continue

			LOG.info("Event '%s' found on node %s" % (event.desc, node, ))

			event.callback(node)
		
		return True


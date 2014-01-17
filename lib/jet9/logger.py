"""
Jet9 logging routines
"""

import logging
import logging.handlers

class Jet9SysLogHandler(logging.handlers.SysLogHandler):
	def emit(self, record):
		"""
		Emit a record.

		The record is formatted, and then sent to the syslog server. If
		exception information is present, it is NOT sent to the server.
		"""
		msg = self.format(record)
		msg = self.log_format_string % (
			self.encodePriority(self.facility,
					self.mapPriority(record.levelname)),
					msg)
		if type(msg) is unicode:
			msg = msg.encode('utf-8')
		try:
			if self.unixsocket:
				try:
					self.socket.send(msg)
				except socket.error:
					self._connect_unixsocket(self.address)
					self.socket.send(msg)
			else:
				self.socket.sendto(msg, self.address)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

def setup_log(log_level=logging.INFO):
	"""Sets up logging."""

	log = logging.getLogger("jet9")
	log.setLevel(log_level)
	log.propagate = False

	# Choosing the log formatting -->
	log_format_syslog = "%(levelname)s: %(filename)s[%(process)s]: %(message)s"

	# syslog handler setup
	handler_syslog = None
	handler_syslog = Jet9SysLogHandler(address = '/dev/log', facility=Jet9SysLogHandler.LOG_LOCAL4)
	handler_syslog.setFormatter(logging.Formatter(log_format_syslog))
	log.addHandler(handler_syslog)


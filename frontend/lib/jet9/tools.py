import sys
import yaml

class P(object):
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	#WARNING = '\033[93m'
	_WARNING = '\033[95m'
	_FAIL = '\033[91m'
	ENDC = '\033[0m'

	QUIET = 0
	FAIL = 1
	ERROR = 1 << 1
	WARNING = 1 << 2
	INFO = 1 << 3
	DEBUG = 1 << 4

	LOGLEVEL = INFO

	def info(self, msg):
		if self.LOGLEVEL >= self.INFO:
			print msg

	def warn(self, msg):
		if self.LOGLEVEL >= self.WARNING:
			print >>sys.stderr, self._WARNING + msg + self.ENDC

	def error(self, msg):
		if self.LOGLEVEL >= self.ERROR:
			print >>sys.stderr, self._FAIL + msg + self.ENDC
		
	def fail(self, msg, exit_code=1):
		if self.LOGLEVEL >= self.FAIL:
			print >>sys.stderr, self._FAIL + msg + self.ENDC
			sys.exit(exit_code)

p = P()

def read_conf(fname, _fail=True):
    try:
        f = open(fname)
    except Exception as e:
        if _fail == True:
            p.fail("%s file not found: %s" % (fname, str(e), ))
        else:
            return {}
    else:
        conf = yaml.load(f)
        f.close()
        if conf is None:
            return {}
        return conf

def save_conf(fname, data):
    try:
        f = open(fname, "w")
    except Exception as e:
        p.fail("Can't save config: %s" % (fname, str(e), ))
    else:
        f.write(yaml.dump(data, default_flow_style=False))
        f.close()

def read_file(fname):
    fn = None
    try:
        fn = open(fname, "r")
    except Exception as e:
        p.fail("ERROR: Can't open file %s : %s" % (fname, str(e), ))

    content = fn.readlines()
    fn.close()
    return "".join(content)

def save_file(fname, data):
    fn = None
    try:
        fn = open(fname, "w")
    except Exception as e:
        p.fail("ERROR: Can't write file %s : %s" % (fname, str(e), ))

    fn.write(data)
    fn.close()

def dict_merge(a, b):
    from copy import deepcopy
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def merge_config(c1, c2):
    return dict(dict_merge(c1, c2))  

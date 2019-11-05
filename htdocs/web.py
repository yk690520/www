import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0,"%s/%s" % (os.path.dirname(__file__),"www"))

from www import app as application
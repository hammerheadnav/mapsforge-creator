import sys
import getopt

#from osmread import parse_file, Relation
import osmium as o

# Global vars
osm_file = None

class NetworkCounter(o.SimpleHandler):

  def __init__(self):
    super(NetworkCounter, self).__init__()
    self.icn = 0
    self.ncn = 0
    self.rcn = 0
    self.lcn = 0

  def way(self, w):
    if 'icn' in w.tags:
      self.icn = self.icn + 1
    if 'ncn' in w.tags:
      self.ncn = self.ncn + 1
    if 'rcn' in w.tags:
      self.rcn = self.rcn + 1
    if 'lcn' in w.tags:
      self.lcn = self.lcn + 1

def check_args(argv):

  global osm_file
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i::", ["input_file="])
  except getopt.GetoptError:
      print("""Program Usage: network_counts.py -i input_file""")
      print("""Example: network_counts.py -i germany.osm.pbf""")
      sys.exit(2)

  for opt, arg in opts:
    if opt in ("-i", "--input_file"):
      osm_file = arg


#this is the entry point to the program
if __name__ == "__main__":

  check_args(sys.argv[1:])
  print('osm file = ' + osm_file)

  h = NetworkCounter()
  h.apply_file(osm_file)
  print('icn count = %d' % h.icn)
  print('ncn count = %d' % h.ncn)
  print('rcn count = %d' % h.rcn)
  print('lcn count = %d' % h.lcn)


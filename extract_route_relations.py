import sys
import getopt

# Use py osmium to parse and write OSM files
import osmium as o

# Global vars
osm_file = None
out_file = None
ncn = []
rcn = []
icn = []
lcn = []

class RouteNetworkHandler(o.SimpleHandler):

  def __init__(self):
    super(RouteNetworkHandler, self).__init__()

  def relation(self, r):
    if 'type' in r.tags and r.tags['type'] =='route':
      if 'network' in r.tags:
        if r.tags['network'] == 'icn':
          for member in r.members:
            icn.append(member.ref)
        elif r.tags['network'] == 'ncn':
          for member in r.members:
            ncn.append(member.ref)
        elif r.tags['network'] == 'rcn':
          for member in r.members:
            rcn.append(member.ref)
        elif r.tags['network'] == 'lcn':
          for member in r.members:
            lcn.append(member.ref)

class Convert(o.SimpleHandler):

  def __init__(self, writer):
    super(Convert, self).__init__()
    self.writer = writer
    self.icn = 0
    self.ncn = 0
    self.rcn = 0
    self.lcn = 0

  def node(self, n):
    self.writer.add_node(n)

  def add_route_network(self, w):
    # Add a tag if way id is in a network list
    newtags = []
    if (w.id in icn):
      newtags.append(('icn', 'yes'))
      self.icn = self.icn + 1
    if (w.id in ncn):
      newtags.append(('ncn', 'yes'))
      self.ncn = self.ncn + 1
    if (w.id in rcn):
      newtags.append(('rcn', 'yes'))
      self.rcn = self.rcn + 1
    if (w.id in lcn):
      newtags.append(('lcn', 'yes'))
      self.lcn = self.lcn + 1

    if (len(newtags) == 0):
      return w

    for tag in w.tags:
      newtags.append(tag)
    return w.replace(tags=newtags)

  def way(self, w):
    self.writer.add_way(self.add_route_network(w))

  def relation(self, r):
    self.writer.add_relation(r)

def parse_relations():
  # Parse relations to form list of ways for each bicycle route network type
  h = RouteNetworkHandler()
  h.apply_file(osm_file)

def check_args(argv):

  global osm_file
  global out_file
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input_file=", "output_file"])
  except getopt.GetoptError:
      print("""Program Usage: extract_route_relations.py -i input_file -o output_file""")
      print("""Example: extract_route_relations.py -i germany.osm.pbf -o germany_new.osm.pbf""")
      sys.exit(2)

  for opt, arg in opts:
    if opt in ("-i", "--input_file"):
      osm_file = arg
    if opt in ("-o", "--output_file"):
      out_file = arg


# MAIN the entry point to the program
if __name__ == "__main__":

  check_args(sys.argv[1:])
  print('osm file = ' + osm_file)

  parse_relations()
  icn.sort()
  ncn.sort()
  rcn.sort()
  lcn.sort()

  # Use PyOsmium to rewrite the pbf file with network tags added to matching ways
  writer = o.SimpleWriter(out_file)
  handler = Convert(writer)
  handler.apply_file(osm_file)

  # Print counts of each cycling network
  print('icn count= %d' % handler.icn)
  print('ncn count= %d' % handler.ncn)
  print('rcn count= %d' % handler.rcn)
  print('lcn count= %d' % handler.lcn)

  writer.close()


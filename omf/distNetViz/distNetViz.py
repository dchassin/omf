'''
Load an OMF feeder in to the new viewer. 

TASKS
XXX We should support feeders that have no layouts. We should do that by doing the force-layout from feeder.py.
XXX Put everything in one html.
XXX Make the output cross-platform.
XXX Work with both .omd and .glm files.
XXX Make the script take arguments from the command line.
XXX Make a Platypus app.
XXX How to allow force layout in Platypus app? Default to it if there is no lat/lon data.
'''

import tempfile, shutil, os, fileinput, json, networkx as nx, platform, omf.feeder as feeder, webbrowser, sys

def main():
	SOURCE_DIR = './'

	# HACK: make sure we have our homebrew binaries available.
	os.environ['PATH'] += os.pathsep + '/usr/local/bin'

	# Handle the command line arguments.
	argCount = len(sys.argv)
	errorMessage = 'Incorrect inputs. Usage: distNetViz -f <Path_to_feeder.glm or .omd>'
	if argCount == 1:
		# print 'Running tests. Normal usage: distNetViz -f <Path_to_feeder.glm or .omd>'
		# FEEDER_PATH = 'DEC Robinsonville Debugged.omd'
		FEEDER_PATH = '../static/publicFeeders/Simple Market System.omd'
		DO_FORCE_LAYOUT = True
	elif argCount == 2:
		DO_FORCE_LAYOUT = False
		FEEDER_PATH = sys.argv[1]
	elif argCount == 3:
		if sys.argv[1] == '-f':
			DO_FORCE_LAYOUT = True
		else:
			print errorMessage
		FEEDER_PATH = sys.argv[2]
	elif argCount > 3:
		print errorMessage

	# Load in the feeder.
	with open(FEEDER_PATH,'r') as feedFile:
		if FEEDER_PATH.endswith('.omd'):
			thisFeed = json.load(feedFile)
		elif FEEDER_PATH.endswith('.glm'):
			thisFeed = {'tree':feeder.parse(FEEDER_PATH, filePath=True)}
		tree = thisFeed['tree']

	# If there is zero lat/lon info, do force layout by default.
	latLonCount = 0
	for key in tree:
		for subKey in ['latitude', 'longitude']:
			if subKey in tree[key]:
				latLonCount += 1
	if latLonCount == 0:
		DO_FORCE_LAYOUT = True

	# Force layout of feeders with no lat/lon information so we can actually see what's there.
	if DO_FORCE_LAYOUT:
		print "Force laying out the graph..."
		# Use graphviz to lay out the graph.
		inGraph = feeder.treeToNxGraph(tree)
		# HACK: work on a new graph without attributes because graphViz tries to read attrs.
		cleanG = nx.Graph(inGraph.edges())
		# HACK2: might miss nodes without edges without the following.
		cleanG.add_nodes_from(inGraph)
		pos = nx.nx_agraph.graphviz_layout(cleanG, prog='neato')
		# # Charting the feeder in matplotlib:
		# feeder.latLonNxGraph(inGraph, labels=False, neatoLayout=True, showPlot=True)
		# Insert the latlons.
		for key in tree:
			obName = tree[key].get('name','')
			thisPos = pos.get(obName, None)
			if thisPos != None:
				tree[key]['longitude'] = thisPos[0]
				tree[key]['latitude'] = thisPos[1]

	# Set up temp directory and copy the feeder and viewer in to it.
	tempDir = tempfile.mkdtemp()
	shutil.copy(SOURCE_DIR + '/distNetViz.html', tempDir + '/viewer.html')
	shutil.copy(SOURCE_DIR + '/svg-pan-zoom.js', tempDir + '/svg-pan-zoom.js')


	# Grab the library we need.
	with open(SOURCE_DIR + 'svg-pan-zoom.js','r') as pzFile:
		pzData = pzFile.read()

	# Rewrite the load lines in viewer.html
	# Note: you can't juse open the file in r+ mode because, based on the way the file is mapped to memory, you can only overwrite a line with another of exactly the same length.
	for line in fileinput.input(tempDir + '/viewer.html', inplace=1):
		if line.lstrip().startswith("<script id='feederLoadScript''>"):
			print "" # Remove the existing load.
		elif line.lstrip().startswith("<script id='feederInsert'>"):
			print "<script id='feederInsert'>\ntestFeeder=" + json.dumps(thisFeed, indent=4) # load up the new feeder.
		elif line.lstrip().startswith("<script id='panZoomInsert'>"):
			print "<script id='panZoomInsert'>\n" + pzData # load up the new feeder.
		else:
			print line.rstrip()

	# webbrowser.open_new("file://" + tempDir + '/viewer.html')
	os.system('open -a "Google Chrome" ' + '"file://' + tempDir + '/viewer.html"')

if __name__ == '__main__':
	main()
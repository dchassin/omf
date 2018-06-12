import opendssdirect as dss
import networkx as nx
import matplotlib.pyplot as plt
import pip


def calculateGraph(df, phase=1):
	graph = nx.Graph()
	data = df[['Bus1', 'Bus2']].to_dict(orient="index")
	for key in data:
		voltage_line = data[key]
		graph.add_edge(voltage_line["Bus1"].split(".")[0], voltage_line["Bus2"].split(".")[0])
	positions = {}
	for name in dss.Circuit.AllBusNames():
		dss.Circuit.SetActiveBus(name)
		if phase in dss.Bus.Nodes():
			index = dss.Bus.Nodes().index(phase)
			re, im = dss.Bus.PuVoltage()[index:index+2]
			voltage = abs(complex(re, im))
			distance = dss.Bus.Distance()
			positions[dss.Bus.Name()] = (distance, voltage)
	return graph, positions

def plotGraph():
	lines = dss.utils.lines_to_dataframe()
	graph, position = calculateGraph(lines)
	fig, ax = plt.subplots(1, 1, figsize=(16, 10))
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	nx.draw_networkx_nodes(graph, position, labels={x: x for x in graph.nodes()})
	ax.set_xlabel('Distances [km]')
	ax.set_ylabel('Voltage [P.u]')
	ax.set_title('VOLTAGE PROFILE')
	plt.show()

if __name__ == "__main__":
	dss.run_command('Redirect ./short_circuit.dss')
	dss.run_command('New EnergyMeter.Main Line.650632 1')
	dss.run_command('Solv ./short_circuit.dss')
	plotGraph()
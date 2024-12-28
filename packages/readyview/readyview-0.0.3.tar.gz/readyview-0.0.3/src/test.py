import readyview

dash = readyview.Dashboard("PijBDVbmF3S7nc6bUePE","rv-prod-AlH6Sx7wlKS78aDFSXtwYKnUteVhu7bU3QDf6exH")
switches = dash.switch.get_switches()

for switch in switches:
	dev = dash.switch.get_device(switch['id'])
	if dev['status'] == "Online":
		print(f"calling {dev['mac_address']}")
		print(dash.switch.get_ports(dev['mac_address']))
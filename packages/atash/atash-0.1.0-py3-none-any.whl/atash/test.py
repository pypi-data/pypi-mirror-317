from atash import connect_to_openeo, load_map

# Connect to OpenEO
connection = connect_to_openeo()

# Load and display the map
map_widget = load_map()
map_widget

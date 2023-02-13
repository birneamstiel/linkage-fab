from linkage_graph.linkage_configuration import LinkageConfiguration
from parse import parse_solvespace_file
from export import render_fabrication_layout


# Parse solve space file and create an intermediate linkage graph representation
linkage_configuration = parse_solvespace_file("sample/indepth_assignment_linkages_saxena.slvs")

# Render linkage configuration as ready to cut svg file
render_fabrication_layout(linkage_configuration)



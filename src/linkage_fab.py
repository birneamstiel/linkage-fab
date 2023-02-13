import argparse

from parse import parse_solvespace_file
from export import render_fabrication_layout

parser = argparse.ArgumentParser(description='LinkageFab: Convert SolveSpace linkages for fabrication')

parser.add_argument('input_file', type=str,
                    help='A file containing a linkage representation. Currently supported: .slvs')
parser.add_argument('--output', type=str,
                    help='Output file name.')

args = parser.parse_args()

# Parse solve space file and create an intermediate linkage graph representation
# linkage_configuration = parse_solvespace_file("sample/indepth_assignment_linkages_saxena.slvs")
linkage_configuration = parse_solvespace_file(args.input_file)

# Render linkage configuration as ready to cut svg file
render_fabrication_layout(linkage_configuration, args.output)



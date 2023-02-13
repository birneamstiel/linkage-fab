from xml.dom import minidom
import io
from shapely.geometry import Polygon
from shapely import affinity

from linkage_graph.linkage_link import ConfigurationSpace
from linkage_graph.linkage_configuration import LinkageConfiguration
import util.geometry as utils
from util.custom_affinity import get_translate_matrix


def render_fabrication_layout(linkage_configuration, output_file_name=None):
    """Creates a svg representation of the given linkage configuration for fabrication. """

    output_file_name = "linkage.svg" if output_file_name is None else output_file_name

    layout_links(linkage_configuration.links)
    
    fabrication_layout = create_svg(linkage_configuration, ConfigurationSpace.fabrication)
    styled_svg = style_svg(fabrication_layout)
    # Make sure we use svg suffix
    file_name = output_file_name.split(".")[0] + ".svg"
    with open(output_file_name, "w") as svg_file:
        styled_svg.writexml(svg_file)

    assembly_manual = create_svg(
        linkage_configuration, ConfigurationSpace.assembled)
    styled_svg = style_svg(assembly_manual)
    assembly_manual_output_file = output_file_name.split(".")[0] + "_assembly_manual.svg"
    with open(assembly_manual_output_file, "w") as svg_file:
        styled_svg.writexml(svg_file)


def create_svg(linkage_configuration: LinkageConfiguration, space: ConfigurationSpace):
    svg_string = ""
    unionized_polygon = Polygon()
    svg_string = ""
    for link in linkage_configuration.links:
        polygon = link.as_polygon(space)
        unionized_polygon = unionized_polygon.union(polygon)

        svg_string += polygon.svg()
        svg_string += "\n"
        positions = link.get_label_positions(space)
        hub_a_label = '<text x="{}" y="{}" > {} </text>'.format(
            positions[0].x, positions[0].y, link.hub_a.get_id())
        svg_string += hub_a_label
        svg_string += "\n"
        hub_b_label = '<text x="{}" y="{}" > {} </text>'.format(
            positions[1].x, positions[1].y, link.hub_b.get_id())
        svg_string += hub_b_label
        svg_string += "\n"

    bounds = unionized_polygon.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    svg_string = '<svg width="{}mm" height="{}mm" viewBox="{} {} {} {}" > \n <g transform = "scale(1,1)">'.format(
        width, height, bounds[0], bounds[1], width, height) + svg_string
    svg_string += '</g>'
    svg_string += "</svg>"
    return svg_string

def style_svg(svg: str) -> minidom.Document:
    svg = minidom.parse(io.StringIO(svg))
    paths = svg.getElementsByTagName("path")
    for path in paths:
        path.setAttribute("fill", "none")
        path.setAttribute("stroke", "#FF0000")
        path.setAttribute("stroke-width", "0.2")
        path.setAttribute("opacity", "1.0")

    labels = svg.getElementsByTagName("text")
    for label in labels:
        label.setAttribute("font-size", "5")
        label.setAttribute("fill", "#0000FF")
    return svg

def layout_links(links: set[Polygon], sheet: tuple = (1000, 1000)):
    """ Calculate transforms for every link to position them next to each other. """
    width = 0
    height = 0
    maxHeight = 0
    padding = 5
    sheet_width = sheet[1]
    sheet_padding = 10

    # layout parts by moving them next to each other
    for link in links:
        polygon = link.as_polygon(space=ConfigurationSpace.primitive)

        position = (0, 0)
        aabb = polygon.bounds
        aabbWidth = aabb[2] - aabb[0]
        aabbHeight = aabb[3] - aabb[1]

        position = (width + padding + aabbWidth / 2,
                    height - padding - aabbHeight / 2)
        maxHeight = max(aabbHeight + padding, maxHeight)
        width += aabbWidth + padding

        #  Overflow, go to next row
        if width >= sheet_width:
            width = sheet_padding - padding
            height -= maxHeight

        positioning_matrix = get_translate_matrix(
            polygon, xoff=position[0], yoff=position[1])
        link.set_fabrication_transform(
            utils.shapely_to_4x4_matrix(positioning_matrix))
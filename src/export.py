from xml.dom import minidom
import io
from shapely.geometry import Polygon
from shapely import affinity

from linkage_graph.linkage_link import ConfigurationSpace
import util.geometry as utils
from util.custom_affinity import get_translate_matrix


def render_fabrication_layout(linkage_configuration, output_file_name="linkage.svg") -> list[Polygon]:
    """ ... """
    output = ""
    unionized_polygon = Polygon()
    output = ""
    for link in linkage_configuration.links:
        polygon = link.as_polygon(ConfigurationSpace.fabrication)
        unionized_polygon = unionized_polygon.union(polygon)

        output += polygon.svg()
        output += "\n"
        hub_a_position = link.get_hub_a_position(
            ConfigurationSpace.fabrication)
        hub_a_label = '<text x="{}" y="{}" > {} </text>'.format(
            hub_a_position.x, hub_a_position.y, link.hub_a.get_id())
        output += hub_a_label
        output += "\n"
        hub_b_position = link.get_hub_b_position(
            ConfigurationSpace.fabrication)
        hub_b_label = '<text x="{}" y="{}" > {} </text>'.format(
            hub_b_position.x, hub_b_position.y, link.hub_b.get_id())
        output += hub_b_label
        output += "\n"

    bounds = unionized_polygon.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    output = '<svg width="{}mm" height="{}mm" viewBox="{} {} {} {}" > \n <g transform = "scale(1,1)">'.format(
        width, height, bounds[0], bounds[1], width, height) + output
    output += '</g>'
    output += "</svg>"

    svg = minidom.parse(io.StringIO(output))
    paths = svg.getElementsByTagName("path")
    for path in paths:
        path.setAttribute("fill", "none")
        path.setAttribute("stroke", "#FF0000")
        path.setAttribute("stroke-width", "0.2")
        path.setAttribute("opacity", "1.0")

    with open(output_file_name, "w") as svg_file:
        svg.writexml(svg_file)

def layout_links(links: set[Polygon], sheet: tuple = (1000, 1000)):
    """ Calculate transforms for every link to position them next to each other. """
    width = 0
    height = 0
    maxHeight = 0
    padding = 5
    sheet_width = sheet[1]
    sheet_padding = 10

    layed_out_parts = []

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
        layed_out_parts.append(affinity.affine_transform(
            polygon, positioning_matrix))
        link.set_fabrication_transform(
            utils.shapely_to_4x4_matrix(positioning_matrix))
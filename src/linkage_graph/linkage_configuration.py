from typing import Set, List

from linkage_graph.linkage_link import LinkageLink
from linkage_graph.linkage_hub import LinkageHub
import util.geometry as utils

class LinkageConfiguration:
    """ ... """

    def __init__(self, hubs: Set[LinkageHub], links: List[LinkageLink]):
        """ ... """

        self.hubs = hubs
        self.links = links

    @staticmethod
    def from_line_segments(line_segments):
        """ ... """
        hubs = set([])
        links = []

        for line_segment in line_segments:
            pointA = [line_segment[0][0], line_segment[0][1]]
            pointB = [line_segment[1][0], line_segment[1][1]]

            hubA = next((h for h in hubs if utils.pointsEqual(h.position, pointA)), LinkageHub(pointA))
            hubB = next((h for h in hubs if utils.pointsEqual(h.position, pointB)), LinkageHub(pointB))
            hubs.add(hubA)
            hubs.add(hubB)

            link = LinkageLink(hubA, hubB)
            links.append(link)

        return LinkageConfiguration(hubs, links)

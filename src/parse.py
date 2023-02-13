from linkage_graph.linkage_configuration import LinkageConfiguration
from slvstopy import Slvstopy

def parse_solvespace_file(file_name: str) -> LinkageConfiguration:
    """Reads a solve space file containing a linkage and creates a
    LinkageConfiguration according to the contained graph structure.
    """
    system_factory = Slvstopy(file_name)
    system, entities = system_factory.generate_system()

    for key, entity in entities.items():
        print(entity)
        print(system.params(entity.params))

    entity_list = list(entities.values())

    line_segments = []

    for index, entity in enumerate(entity_list):
        if (entity.is_line_2d()):
            # within the entity list, apparently every line segments follows its two defining points
            p1 = system.params(entity_list[index-2].params)
            p2 = system.params(entity_list[index-1].params)
            line_segments.append([p1, p2])

    return LinkageConfiguration.from_line_segments(line_segments)
    

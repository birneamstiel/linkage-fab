from shapely.geometry import LineString, Polygon, Point
from enum import Enum
from shapely import affinity
import numpy as np

from linkage_graph.linkage_hub import LinkageHub
import util.geometry as utils
from util.custom_affinity import get_rotate_matrix, get_translate_matrix, get_scale_matrix

ConfigurationSpace = Enum('ConfigurationSpace', 'assembled primitive fabrication')

class LinkageLink:
    """ Representing a rigid link as part of a linkage system """

    def __init__(self, hub_a: LinkageHub, hub_b: LinkageHub):
        """ Creat a new link by specifying its two hubs (coordinates in assembled space). """

        self.hub_a = hub_a
        self.hub_b = hub_b
        
        self.fabrication_transform = np.identity(4)


    def set_fabrication_transform(self, transform_matrix: np.ndarray):
        """ Set the links transform for the fabrication state. Matrix should assume link being in primitive space. """
        
        if transform_matrix.shape != (4,4):
            raise ValueError("Expected transforms format: 4x4 matrix")

        self.fabrication_transform = transform_matrix

    def get_hub_a_position(self, space=ConfigurationSpace.assembled):
        assembled_position = self.hub_a.position
        
        if space is ConfigurationSpace.assembled:
            return assembled_position
        
        primitive_transform = self._get_primitive_transform()

        if space is ConfigurationSpace.primitive:
            return affinity.affine_transform(Point(self.hub_a.position), utils.matrix_to_shapely(primitive_transform))
        elif space is ConfigurationSpace.fabrication:
            transform = self.fabrication_transform @ primitive_transform
            return affinity.affine_transform(Point(self.hub_a.position), utils.matrix_to_shapely(transform))

    def get_hub_b_position(self, space=ConfigurationSpace.assembled):
        assembled_position = self.hub_b.position

        if space is ConfigurationSpace.assembled:
            return assembled_position

        primitive_transform = self._get_primitive_transform()

        if space is ConfigurationSpace.primitive:
            return affinity.affine_transform(Point(self.hub_b.position), utils.matrix_to_shapely(primitive_transform))
        elif space is ConfigurationSpace.fabrication:
            transform = self.fabrication_transform @ primitive_transform
            return affinity.affine_transform(Point(self.hub_b.position), utils.matrix_to_shapely(transform))


    def as_polygon(self, space=ConfigurationSpace.assembled, linkage_radius=7.5, joint_radius = 1) -> Polygon:
        """Creates a polygon representation of this link.
        
        Different spaces are supported, either:
         assembled space: where links are rendered as they were created, within a connected configuration
         primitive space: where links are consistenlty aligned with the y-axis and centered within the origin
         fabrication space: where links are positioned according to a fabrication transform (see set_fabrication_transform)
        """
        link_polygon = self._create_geometry(linkage_radius, joint_radius)

        if space is ConfigurationSpace.assembled:
            return link_polygon

        primitive_transform = self._get_primitive_transform()
        if space is ConfigurationSpace.primitive:
            return affinity.affine_transform(link_polygon, utils.matrix_to_shapely(primitive_transform))
        elif space is ConfigurationSpace.fabrication:
            transform = self.fabrication_transform @ primitive_transform
            return affinity.affine_transform(link_polygon, utils.matrix_to_shapely(transform))


        return link_polygon

    def get_id(self) -> str:
        return '{}|{}'.format(self.hub_a.get_id(), self.hub_b.get_id())

    def _create_geometry(self, linkage_radius=7.5, joint_radius= 1):
        line = LineString([self.hub_a.position, self.hub_b.position])

        hub_a_polygon = Point(self.hub_a.position).buffer(joint_radius)
        hub_b_polygon = Point(self.hub_b.position).buffer(joint_radius)
        link_polygon = line.buffer(linkage_radius)
        link_polygon = link_polygon.difference(hub_a_polygon)
        link_polygon = link_polygon.difference(hub_b_polygon)
        return link_polygon

    def _get_primitive_transform(self) -> np.ndarray:
        """Calculates a transform matrix moving this links polygon into primitive space, 
        i.e. centers it within the origin, aligns the rotated bounding box 
        with the coordinate axis and rotates the longest side to be parallel with the y axis.
        """
        original_polygon = self._create_geometry()
        # 1. Mirror y axis
        # y axis in svg space is mirrored
        mirror_matrix = get_scale_matrix(
            original_polygon, yfact=-1, origin=(0, 0))
        polygon = affinity.affine_transform(
            original_polygon, mirror_matrix)

        mirror_transforms = utils.shapely_to_4x4_matrix(mirror_matrix)

        aabb_center_x, aabb_center_y = utils.center_for_bounds(polygon.bounds)

        # 2. Move bounds center into origin
        centering_matrix = get_translate_matrix(
            polygon, xoff=-aabb_center_x, yoff=-aabb_center_y)
        polygon = affinity.affine_transform(
            polygon, centering_matrix)
        centering_transforms = utils.shapely_to_4x4_matrix(centering_matrix)

        # 3. Align with coordinate axis
        rotated_bounds = polygon.minimum_rotated_rectangle
        rotated_bounds.exterior.coords[0]
        rect_vector_a = [rotated_bounds.exterior.coords[1][0] - rotated_bounds.exterior.coords[0]
                          [0], (rotated_bounds.exterior.coords[1][1] - rotated_bounds.exterior.coords[0][1])]
        # has to be mirrored as well
        rect_vector_a[1] *= -1

        x_angle = utils.angle_between(rect_vector_a, [1, 0])
        if x_angle > 90:
            x_angle = utils.angle_between(rect_vector_a, [-1, 0])

        # When reference vector lays in first and third quadrant, we need to rotate clockwise to align with the x axis (= negagive angle), otherwise
        # we are rotating counter clockwise (= positive angle)
        if (rect_vector_a[0] > 0 and rect_vector_a[1] > 0) or rect_vector_a[0] < 0 and rect_vector_a[1] < 0:
            x_angle = -x_angle

        centering_rotation_matrix = get_rotate_matrix(
            polygon, x_angle)
        polygon = affinity.affine_transform(
            polygon, centering_rotation_matrix)
        centering_rotation_transforms = utils.shapely_to_4x4_matrix(
            centering_rotation_matrix)

        # 4. Make sure the longest side of the polygon's aabb is along the y axis (for consistency) 
        aabb = affinity.affine_transform(original_polygon, utils.matrix_to_shapely(
            centering_rotation_transforms @ centering_transforms @ mirror_transforms)).bounds
        aabbWidth = aabb[2] - aabb[0]
        aabbHeight = aabb[3] - aabb[1]

        orientation_transforms = np.identity((4))
        if aabbWidth > aabbHeight:
            orientation_matrix = get_rotate_matrix(polygon, 90)
            polygon = affinity.affine_transform(
                polygon, orientation_matrix)
            orientation_transforms = utils.shapely_to_4x4_matrix(
                orientation_matrix)

        return orientation_transforms @ centering_rotation_transforms @ centering_transforms @ mirror_transforms


"""Affinity transform helpers adjusted to return a matrix without applying. 
Adjusted from https://raw.githubusercontent.com/shapely/shapely/main/shapely/affinity.py
"""

from math import cos, pi, sin

__all__ = ["affine_transform", "rotate", "scale", "skew", "translate"]

def interpret_origin(geom, origin, ndim):
    """Returns interpreted coordinate tuple for origin parameter.

    This is a helper function for other transform functions.

    The point of origin can be a keyword 'center' for the 2D bounding box
    center, 'centroid' for the geometry's 2D centroid, a Point object or a
    coordinate tuple (x0, y0, z0).
    """
    # get coordinate tuple from 'origin' from keyword or Point type
    if origin == "center":
        # bounding box center
        minx, miny, maxx, maxy = geom.bounds
        origin = ((maxx + minx) / 2.0, (maxy + miny) / 2.0)
    elif origin == "centroid":
        origin = geom.centroid.coords[0]
    elif isinstance(origin, str):
        raise ValueError(f"'origin' keyword {origin!r} is not recognized")
    elif getattr(origin, "geom_type", None) == "Point":
        origin = origin.coords[0]

    # origin should now be tuple-like
    if len(origin) not in (2, 3):
        raise ValueError(
            "Expected number of items in 'origin' to be " "either 2 or 3")
    if ndim == 2:
        return origin[0:2]
    else:  # 3D coordinate
        if len(origin) == 2:
            return origin + (0.0,)
        else:
            return origin


def get_rotate_matrix(geom, angle, origin="center", use_radians=False):
    r"""Returns a rotated geometry on a 2D plane.

    The angle of rotation can be specified in either degrees (default) or
    radians by setting ``use_radians=True``. Positive angles are
    counter-clockwise and negative are clockwise rotations.

    The point of origin can be a keyword 'center' for the bounding box
    center (default), 'centroid' for the geometry's centroid, a Point object
    or a coordinate tuple (x0, y0).

    The affine transformation matrix for 2D rotation is:

      / cos(r) -sin(r) xoff \
      | sin(r)  cos(r) yoff |
      \   0       0      1  /

    where the offsets are calculated from the origin Point(x0, y0):

        xoff = x0 - x0 * cos(r) + y0 * sin(r)
        yoff = y0 - x0 * sin(r) - y0 * cos(r)
    """
    if geom.is_empty:
        return geom
    if not use_radians:  # convert from degrees
        angle = angle * pi / 180.0
    cosp = cos(angle)
    sinp = sin(angle)
    if abs(cosp) < 2.5e-16:
        cosp = 0.0
    if abs(sinp) < 2.5e-16:
        sinp = 0.0
    x0, y0 = interpret_origin(geom, origin, 2)

    # fmt: off
    matrix = (cosp, -sinp, 0.0,
              sinp, cosp, 0.0,
              0.0, 0.0, 1.0,
              x0 - x0 * cosp + y0 * sinp, y0 - x0 * sinp - y0 * cosp, 0.0)
    # fmt: on
    return matrix


def get_translate_matrix(geom, xoff=0.0, yoff=0.0, zoff=0.0):
    r"""Returns a translated geometry shifted by offsets along each dimension.

    The general 3D affine transformation matrix for translation is:

        / 1  0  0 xoff \
        | 0  1  0 yoff |
        | 0  0  1 zoff |
        \ 0  0  0   1  /
    """
    if geom.is_empty:
        return geom

    # fmt: off
    matrix = (1.0, 0.0, 0.0,
              0.0, 1.0, 0.0,
              0.0, 0.0, 1.0,
              xoff, yoff, zoff)
    # fmt: on
    return matrix


def get_scale_matrix(geom, xfact=1.0, yfact=1.0, zfact=1.0, origin='center'):
    r"""Returns a scaled geometry, scaled by factors along each dimension.

    The point of origin can be a keyword 'center' for the 2D bounding box
    center (default), 'centroid' for the geometry's 2D centroid, a Point
    object or a coordinate tuple (x0, y0, z0).

    Negative scale factors will mirror or reflect coordinates.

    The general 3D affine transformation matrix for scaling is:

        / xfact  0    0   xoff \ 
        |   0  yfact  0   yoff |
        |   0    0  zfact zoff |
        \   0    0    0     1  /

    where the offsets are calculated from the origin Point(x0, y0, z0):

        xoff = x0 - x0 * xfact
        yoff = y0 - y0 * yfact
        zoff = z0 - z0 * zfact
    """
    if geom.is_empty:
        return geom
    x0, y0, z0 = interpret_origin(geom, origin, 3)

    matrix = (xfact, 0.0, 0.0,
              0.0, yfact, 0.0,
              0.0, 0.0, zfact,
              x0 - x0 * xfact, y0 - y0 * yfact, z0 - z0 * zfact)
    return matrix

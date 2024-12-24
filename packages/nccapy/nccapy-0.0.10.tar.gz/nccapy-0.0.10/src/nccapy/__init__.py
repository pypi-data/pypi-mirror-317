"""
nccapy module

This module is used in the NCCA Python programming courses for more details see here
https://nccastaff.bournemouth.ac.uk/jmacey/

Available submodules
--------------------
Math
    This contains simple Vec3,Vec4,Mat3,Mat4 and Transform classes for 3D math.
Geo
    Provides a Simple Mesh type class for creating and loading Obj files
Image
    Provides classes for simple images and RGBA color values allowing the setting and getting of pixels

Classes
-------
Vec3
    A class for 3D vectors.
Vec4
    A class for 4D vectors.
Mat3
    A class for 3x3 matrices.
Mat4
    A class for 4x4 matrices.
Transform
    A class for transformations.
Obj
    A class for 3D objects.
Timer
    A class for timing operations.
Image
    A class for images.
RGBA
    A class for RGBA color values.
"""

from nccapy.Math import Vec3, Vec4, Mat3, Mat4, Transform
from nccapy.Geo import Obj
from nccapy.Image import Image, RGBA, Canvas

__all__ = ["Vec3", "Vec4", "Mat3", "Mat4", "Transform", "Obj", "Image", "RGBA", "Canvas"]

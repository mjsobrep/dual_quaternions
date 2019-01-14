"""
A module to hold and work with dual quaternions.
"""

# The MIT License (MIT)
#
# Copyright (c) 2016 GTRC.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import division
import math
from quaternions import Quaternion


class DualQuaternion(object):
    """
    A class to handle dual quaternions. These are used to express rotation and
    translation in one mathematical construct.

    Attributes:
        real: A Quaternion to hold the real (rotation) portion of the dual
              quaternion
        dual: A Quaternion to hold the dual (translation) portion of the dual
              quaternion
    """

    def __init__(self, real, dual):
        """Construct a dual quaternion

        Args:
            real (Quaternion): The real (rotation) portion of the dual
                               quaternion
            dual (Quaternion): The dual (translation) portion of the dual
                               quaternion
        """
        self.dual = dual
        self.real = real.unit()

    def dot(self, other):
        """ Take the dot product of two dual quaternions. This is simply the
        dot product of the two real components

        Args:
            other (DualQuaternion): The other dual quaternion with which to
                                    compute the dot product

        Returns: A number, the dot product of the two arguments.

        """
        return self.real.dot(other.real)

    def __mul__(self, other):
        """ Multiply the caller (left hand side) by the argument (right hand
        side). If the dual quaternion is being multiplied by a float or int, it
        will simply be scaled

        Args:
            other (DualQuaternion, float, int):

        Returns:
            The resulting dual quaternion
        """
        if isinstance(other, (float, int)):
            return DualQuaternion(self.real*other, self.dual*other)
        elif isinstance(other, DualQuaternion):
            return DualQuaternion(self.real*other.real,
                                  self.dual*other.real + self.real*other.dual)
            # Really not sure that the order here is right
        else:
            raise TypeError("Only supports Dual Quaternion, float, and int")

    def normalize(self):
        """Normalize the quaternion. This will ensure that the rotational
        portion of the quaternion has a norm of one and will scale the dual
        part by the same amount required to scale the real part.

        Returns:
            The caller, normalized
        """
        norm = self.real.dot(self.real)
        return DualQuaternion(self.real/norm, self.dual/norm)

    def __add__(self, other):
        """Add the two dual quaternions together. This is simple addition of
        the real parts and dual parts seperately.

        Args:
            other (DualQuaternion): The dual quaternion to add the caller to

        Returns:
            The sum
        """
        return DualQuaternion(self.real + other.real, self.dual + other.dual)

    def conjugate_reverse(self):
        """ Return the conjugate of the caller

        Multiple definitions possible:
        ------------------------------
        Given a dual quaternion Q, the conjugate of Q can be defined as:
            - DualQuaternion(Q.real.conjugate(), Q.dual.conjugate())
                - use to reverse order of multiplication
            - DualQuaternion(Q.real, -Q.dual)
            - DualQuaternion(Q.real.conjugate(), -Q.dual.conjugate())
                - use to translate points with sandwidch multiplication

        Using type 3 from:
        http://what-when-how.com/advanced-methods-in-computer-graphics/
        quaternions-advanced-methods-in-computer-graphics-part-6/

        Returns:
            The conjugate of the caller
        """
        return DualQuaternion(self.real.conjugate(), self.dual.conjugate())

    def conjugate_transform(self):
        """ Return the conjugate of the caller

        Multiple definitions possible:
        ------------------------------
        Given a dual quaternion Q, the conjugate of Q can be defined as:
            - DualQuaternion(Q.real.conjugate(), Q.dual.conjugate())
                - use to reverse order of multiplication
            - DualQuaternion(Q.real, -Q.dual)
            - DualQuaternion(Q.real.conjugate(), -Q.dual.conjugate())
                - use to translate points with sandwidch multiplication

        Using type 3 from:
        http://what-when-how.com/advanced-methods-in-computer-graphics/
        quaternions-advanced-methods-in-computer-graphics-part-6/

        Returns:
            The conjugate of the caller
        """
        return DualQuaternion(self.real.conjugate(), -self.dual.conjugate())

    def get_translation(self):
        """Return the translation component of the dual quaternion

        Returns:
            The translation component of the caller
        """

        vals = (self.dual*2)*self.real.conjugate()
        return [vals.x, vals.y, vals.z]

    def get_transformation_matrix(self):
        """Return the homogeneous transformation matrix

        Returns:
            The homogeneous transformation matrix as a list of 4 lists of 4
            members each.
        """
        transormation_matrix = [[0]*4]*4
        rot_matx = self.real.get_rotation_matrix()
        translation = self.get_translation()
        for i in range(3):
            transormation_matrix[i][3] = translation[i]
            for j in range(3):
                transormation_matrix[i][j] = rot_matx[i][j]

        transormation_matrix[3][3] = 1

    def almost_equal(self, other, delta=.00000001):
        """Determines whether a dual quaternion is approximately equal to
        another using a naive comparison of the 8 values w, x, y, z for real
        and dual components

        Args:
            other (DualQuaternion): The DualQuaternion to compare to
            delta (float): The threshold for equality

        Returns:

        """
        return (self.real.almost_equal(other.real, delta) and
                self.dual.almost_equal(other.dual, delta))

    def __str__(self):
        """Return a string representation of the dual quaternion

        Returns:
            String representation of the dual quaternion
        """
        return("Real:\t"+str(self.real)+"\t\tDual:\t"+str(self.dual))

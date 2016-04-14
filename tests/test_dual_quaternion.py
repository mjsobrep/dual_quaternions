"""
Tests for dual quaternion class
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
from unittest import TestCase
from dual_quaternions import DualQuaternion
from quaternions import Quaternion
from random import Random


class TestQuaternion(TestCase):
    def setUp(self):
        random = Random(100)
        N = 50*(4+3)
        int_vals = [random.randint(-1000, 1000) for _ in range(N//2)]
        float_vals = [random.uniform(-1000, 1000) for _ in range(N // 2)]
        val_list = int_vals + float_vals
        random.shuffle(val_list)
        self.all = [
            DualQuaternion(Quaternion(val_list[7*n], val_list[7*n+1],
                                      val_list[7*n+2], val_list[7*n+3]),
                           Quaternion.from_translation(
                               [val_list[7*n+4], val_list[7*n+5],
                                val_list[7*n+6]])) for n in range(N//7)]
        self.p = self.all[:N//2]
        self.q = self.all[N//2:]

    def test_conjugate_1(self):
        """(AC)*=C*A*"""
        for q in self.q:
            for p in self.p:
                (q*p).conjugate().almost_equal(p.conjugate()*q.conjugate())

    def test_conjugate_2(self):
        """AA*=(1,0):A=normalize(A')"""
        for q in self.all:
            print (str(q.conjugate())+"\n"+str(q)+"\n"+str(q*q.conjugate())+"\n\n")
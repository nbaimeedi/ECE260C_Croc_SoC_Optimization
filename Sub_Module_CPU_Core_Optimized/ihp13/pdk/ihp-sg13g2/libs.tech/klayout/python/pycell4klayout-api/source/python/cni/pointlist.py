########################################################################
#
# Copyright 2024 IHP PDK Authors
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.gnu.org/licenses/gpl-3.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

from __future__ import annotations

from cni.point import *
from cni.ulist import *

class PointList(ulist[Point]):

    def __init__(self, items = None) -> None:
        super().__init__(items)

    def compress(self, isClose = True) -> PointList:
        """
        Compresses this PointList, by removing any extra (coincident and/or collinear) points from
        this PointList. The optional isClosed parameter is used to indicate whether this set of
        points is meant to represent a closed shape or not. If all points are collinear, then the
        first and last points will be the result of compressing this PointList. If the first and
        last points are coincident, then only the first point is returned

        :param isClose: Whether represented shape is closed
        :type isClose: boolean
        :return: see description above
        :rtype: PointList
        """

        if len(self) < 3:
            return self

        if self[0] == self[-1]:
            firstPointList = []
            firstPointList.append(self[0])
            self = firstPointList
            return self

        pairUniqueList = []
        [pairUniqueList.append(value) for index, value in enumerate(self) if index == 0 or value != self[index-1]]

        nonColinearList = []
        for index, value in enumerate(pairUniqueList):
            if index == 0 or index == len(pairUniqueList)-1:
                nonColinearList.append(value)
            else:
                if not Point.areColinearPoints(pairUniqueList[index-1], value, pairUniqueList[index+1]):
                    nonColinearList.append(value)

        self = nonColinearList
        return self

    def containsPoint(self, point: Point) -> bool:
        # Jordan point in polygon test
        numVertices = len(self)
        x, y = point.x, point.y
        isInside = False

        p1 = self[0]

        for i in range(1, numVertices + 1):
            p2 = self[i % numVertices]

            if y > min(p1.y, p2.y):
                if y <= max(p1.y, p2.y):
                    if x <= max(p1.x, p2.x):
                        x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                        if p1.x == p2.x or x <= x_intersection:
                            isInside = not isInside

            p1 = p2

        return isInside

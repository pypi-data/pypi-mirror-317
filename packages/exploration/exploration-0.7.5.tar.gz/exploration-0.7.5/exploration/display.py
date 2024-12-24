"""
- Authors: Peter Mawhorter, Tiffany Lin, & Presha Goel
- Consulted:
- Date: 2022-4-15
- Purpose: Code to support visualizing decision graphs and explorations.

Defines functions for graph layout and drawing for
`exploration.core.DecisionGraph` objects. See the `explorationViewer`
module for more info on how these are used. This module computes layout
positions, but actually displaying the graphs is done via HTML.

TODO: Anchor-free localization implementation?
"""

from typing import (
    Dict, Tuple, Literal, TypeAlias, Sequence, Optional, Set, Union, List
)

import math

import networkx as nx

from . import base
from . import core
from . import analysis

BlockPosition: 'TypeAlias' = Tuple[int, int, int]
"""
A type alias: block positions indicate the x/y coordinates of the
north-west corner of a node, as well as its side length in grid units
(all nodes are assumed to be square).
"""


BlockLayout: 'TypeAlias' = Dict[base.DecisionID, BlockPosition]
"""
A type alias: block layouts map each decision in a particular graph to a
block position which indicates both position and size in a unit grid.
"""


def roomSize(connections: int) -> int:
    """
    For a room with the given number of connections, returns the side
    length of the smallest square which can accommodate that many
    connections. Note that outgoing/incoming reciprocal pairs to/from a
    single destination should only count as one connection, because they
    don't need more than one space on the room perimeter. Even with zero
    connections, we still return 1 as the room size.
    """
    if connections == 0:
        return 1
    return 1 + (connections - 1) // 4


def expandBlocks(layout: BlockLayout) -> None:
    """
    Modifies the given block layout by adding extra space between each
    positioned node: it triples the coordinates of each node, and then
    shifts them south and east by 1 unit each, by maintaining the nodes
    at their original sizes, TODO...
    """
    # TODO


#def blockLayoutFor(region: core.DecisionGraph) -> BlockLayout:
#    """
#    Computes a unit-grid position and size for each room in an
#    `exploration.core.DecisionGraph`, laying out the rooms as
#    non-overlapping square blocks. In many cases, connections will be
#    stretched across empty space, but no explicit space is reserved for
#    connections.
#    """
#    # TODO

GraphLayoutMethod: 'TypeAlias' = Literal["stacked", "square"]
"""
The options for layouts of a decision graph. They are:

- 'stacked': Assigns *all* nodes to position (0, 0). Use this if you want
    to generate an empty layout that you plan to modify. Doesn't require
    any attributes.
- 'square': Takes the square root of the number of decisions, then places
    them in order into a square with that side length (rounded up). This
    is a very simple but also terrible algorithm. Doesn't require any
    attributes.
- 'line': Lays out the decisions in a straight line. Doesn't require any
    attributes.
"""

def assignPositions(
    decisions: Sequence[base.DecisionID],
    attributes: Optional[Dict[base.DecisionID, dict]] = None,
    method: GraphLayoutMethod = "square"
) -> base.Layout:
    """
    Given a sequence of decision IDs, plus optionally a dictionary
    mapping those IDs to attribute dictionaries, computes a layout for
    the decisions according to the specified method, returning a
    dictionary mapping each decision ID to its position in the layout.

    Different layout methods may required different attributes to be
    available.
    """
    if method == "stacked":
        return {d: (0, 0) for d in decisions}  #  all nodes at (0, 0)
    elif method == "square":
        return assignSquarePositions(decisions)
    elif method == "line":
        return assignLinePositions(decisions)
    else:
        raise ValueError(f"Invalid layout method {method!r}.")


def assignSquarePositions(
    decisions: Sequence[base.DecisionID]
) -> base.Layout:
    """
    Creates and returns a dictionary of positions for the given sequence
    of decisions using the 'square' layout: it arranges them into a big
    square.
    """
    result = {}
    # Figure out side length of the square that will fit them all
    side = math.ceil((len(decisions)**0.5))
    # Put 'em in a square
    for i, d in enumerate(decisions):
        result[d] = (i % side, i // side)
    return result


def assignLinePositions(
    decisions: Sequence[base.DecisionID]
) -> base.Layout:
    """
    Creates and returns a dictionary of positions for the given sequence
    of decisions using the 'line' layout: it arranges them into a
    straight horizontal line.
    """
    result = {}
    # Put 'em in a line
    for i, d in enumerate(decisions):
        result[d] = (float(i), 0.0)
    return result


def setFinalPositions(
    exploration: core.DiscreteExploration,
    method: GraphLayoutMethod = "square"
) -> None:
    """
    Adds a "finalPositions" attribute to the given exploration which
    contains a dictionary mapping decision IDs to `Position`s. Every
    decision that ever existed over the course of the exploration is
    assigned a position.
    """
    exploration.layouts["final"] = assignPositions(
        exploration.allDecisions(),
        method=method
    )

def setPathPositions(exploration: core.DiscreteExploration) -> None:
    """
    Adds a "pathPositions" attribute to the given exploration which
    contains a dictionary mapping decision IDs to `Position`s. This
    includes every visited decision and all of their neighbors, but does
    NOT include decisions which were never visited and are not neighbors
    of a visited decision.
    """
    # Lay out visited decisions in a line:
    onPath = exploration.allVisitedDecisions()
    result = assignLinePositions(onPath)
    # Get the final graph to add neighbors from
    finalGraph = exploration.getSituation().graph
    # Track already-accounted-for neighbors
    seen: Set[base.DecisionID] = set()
    # Add neighbors to our layout
    for decision in onPath:
        # copy x of this decision
        x = result[decision][0]
        # Track y coordinates going down below the line
        y = -1.0
        try:
            neighbors = finalGraph.destinationsFrom(decision)
        except core.MissingDecisionError:
            continue
            # decision on path may have been merged or deleted by end of
            # exploration. We don't want to get neighbors in the step the
            # node was visited, because it's likely many of those will
            # have been explored by the time we get to the final graph,
            # and we also don't want to include any merged/deleted
            # neighbors in our graph, despite the fact we're including
            # merged or deleted path nodes.
        # TODO: Sort these by step added?
        for dID in neighbors.values():
            # We only include all neighbors which are not elsewhere on
            # the path. It's possible some of these may be confirmed, but
            # that's fine, they were not active at any step.
            if dID not in onPath:
                result[dID] = (x, y)
                y -= 1.0  # next node will be lower down

    exploration.layouts["path"] = result


#---------------#
# Baryeccentric #
#---------------#

Number: 'TypeAlias' = Union[int, float]
"""
For arguments that can be either an integer or a float.
"""


# Testing support functions
def pz(n: Number) -> Number:
    """
    Converts -0.0 to 0.0 and leaves all other numbers alone.
    """
    if n == -0.0:
        return 0.0
    else:
        return n


def rt(t: base.LayoutPosition) -> base.LayoutPosition:
    """
    Rounds off both parts of a 2-element tuple to 6 decimal places, and
    then also converts -0.0 to +0.0 in either position.
    """
    return (
        pz(round(t[0], 6)),
        pz(round(t[1], 6))
    )


def rtl(tl: Sequence[base.LayoutPosition]) -> List[base.LayoutPosition]:
    """
    Applies `rt` to a sequence of positions, returning a list.
    """
    return [rt(t) for t in tl]


def distance(a: base.LayoutPosition, b: base.LayoutPosition) -> float:
    """
    Calculates the distance between two points, using the distance
    formula in 2 dimensions. For example:

    >>> distance((0, 0), (0, 3))
    3.0
    >>> distance((0, 0), (3, 0))
    3.0
    >>> distance((0, 0), (3, 4))
    5.0
    """
    x1, y1 = a
    x2, y2 = b

    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5


def mid(
    a: base.LayoutPosition,
    b: base.LayoutPosition
) -> base.LayoutPosition:
    """
    Returns the midpoint between two points. For example:

    >>> rt(mid((0, 0), (1, 0)))
    (0.5, 0.0)
    >>> rt(mid((0, 0), (3, 8)))
    (1.5, 4.0)
    >>> rt(mid((3, -3), (-3, 3)))
    (0.0, 0.0)
    """
    x1, y1 = a
    x2, y2 = b

    return ((x1 + x2) / 2, (y1 + y2) / 2)


def vAdd(
    a: base.LayoutPosition,
    b: base.LayoutPosition
) -> base.LayoutPosition:
    """
    Returns the vector addition result for two layout positions.
    For example:

    >>> vAdd((0.0, 0.0), (1.0, 1.0))
    (1.0, 1.0)
    >>> vAdd((1.0, 1.0), (0.0, 0.0))
    (1.0, 1.0)
    >>> vAdd((1.0, 1.0), (2.0, -3.0))
    (3.0, -2.0)
    >>> vAdd((1.0, 1.0), (1.0, 1.0))
    (2.0, 2.0)
    """
    x1, y1 = a
    x2, y2 = b

    return (x1 + x2, y1 + y2)


def vSub(
    a: base.LayoutPosition,
    b: base.LayoutPosition
) -> base.LayoutPosition:
    """
    Returns the vector between points a and b (from b to a, which is
    also a - b in vector math). For example:

    >>> vSub((1.0, 1.0), (0.0, 0.0))
    (1.0, 1.0)
    >>> vSub((2.0, -3.0), (1.0, 1.0))
    (1.0, -4.0)
    >>> vSub((1.0, 1.0), (1.0, 1.0))
    (0.0, 0.0)
    """
    x1, y1 = a
    x2, y2 = b

    return (x1 - x2, y1 - y2)

def norm(v: base.LayoutPosition) -> base.LayoutPosition:
    """
    Normalizes the given vector, returning a vector in the same direction
    whose length is 1. Returns the zero-vector if given the zero-vector,
    which is the only case where the length of the result is not 1.

    For example:

    >>> norm((0, 0))
    (0.0, 0.0)
    >>> norm((2, 0))
    (1.0, 0.0)
    >>> norm((102, 0))
    (1.0, 0.0)
    >>> norm((0, -3))
    (0.0, -1.0)
    """
    length = distance((0, 0), v)
    if length == 0:
        return (0.0, 0.0)
    else:
        return (v[0] / length, v[1] / length)


def isATriangle(x: Number, y: Number, z: Number) -> bool:
    """
    Checks whether three side lengths can form a triangle. For example:

    >>> isATriangle(3, 4, 5)
    True
    >>> isATriangle(1, 1, 1)
    True
    >>> isATriangle(100, 99, 1)
    False
    >>> isATriangle(100, 99, 2)
    True
    >>> isATriangle(2, 100, 99)
    True
    >>> isATriangle(99, 2, 100)
    True
    >>> isATriangle(3, 2, 10)
    False
    >>> isATriangle(5, 1, 1)
    False
    >>> isATriangle(9, 18.01, 9)
    False
    """
    return ((x + y > z) and (y + z > x) and (z + x > y))


def scaleBy(
    vector: base.LayoutPosition,
    scale: Number
) -> base.LayoutPosition:
    """
    Scales the given vector by the specified scale.
    Examples:

    >>> rt(scaleBy((1.0, 0.0), 3))
    (3.0, 0.0)
    >>> rt(scaleBy((3.0, 4.0), 10))
    (30.0, 40.0)
    >>> rt(scaleBy((6.0, 8.0), 5))
    (30.0, 40.0)
    >>> rt(scaleBy((0.0, 2.0), -2))
    (0.0, -4.0)
    >>> rt(scaleBy((0.0, 0.0), 1000))
    (0.0, 0.0)
    """
    x, y = vector
    return (x * scale, y * scale)


def scaleTo(
    vector: base.LayoutPosition,
    length: Number
) -> base.LayoutPosition:
    """
    Scales the given vector to the specified length. Note that if the
    vector is (0, 0), it will remain (0, 0) so the result won't actually
    have the specified length in that one case. Examples:

    >>> rt(scaleTo((1, 0), 3))
    (3.0, 0.0)
    >>> rt(scaleTo((3, 4), 10))
    (6.0, 8.0)
    >>> rt(scaleTo((6, 8), 5))
    (3.0, 4.0)
    >>> rt(scaleTo((0, 2), -2))
    (0.0, -2.0)
    >>> rt(scaleTo((0, 0), 1000))
    (0.0, 0.0)
    """
    lengthNow = distance((0, 0), vector)
    if lengthNow == 0:
        return (0.0, 0.0)
    else:
        x, y = vector
        return (
            (x / lengthNow) * length,
            (y / lengthNow) * length
        )


def circleIntersections(
    a: base.LayoutPosition,
    b: base.LayoutPosition,
    aRadius: Number,
    bRadius: Number
) -> List[base.LayoutPosition]:
    """
    Calculates the intersection point(s) between two circles centered at
    points `a` and `b` with the given radii. Returns a list of 0, 1, or 2
    positions depending on the relationship between the circles. Note
    that if two circles are the same circle, it should in theory return a
    list of infinite positions; in that case we return a list with four
    positions that are the places where horizontal and vertical lines
    through the shared center intersect the shared circle. Examples:

    >>> rtl(circleIntersections((0, 0), (2, 0), 1, 1))  # single point
    [(1.0, 0.0)]
    >>> rtl(circleIntersections((0, 0), (0, 2), 1, 1))  # single point
    [(0.0, 1.0)]
    >>> rtl(circleIntersections((0, 0), (6, 8), 5, 5))  # two 3/4/5 triangles
    [(3.0, 4.0)]
    >>> rtl(circleIntersections((0, 0), (2, 0), 1.5, 1.5))  # two points
    [(1.0, -1.118034), (1.0, 1.118034)]
    >>> rtl(circleIntersections((0, 0), (0, 0), 2, 3))  # no points
    []
    >>> rtl(circleIntersections((0, 0), (2, 0), 0.5, 0.5))  # no points
    []
    >>> rtl(circleIntersections((-3, 4), (3, 4), 5, 5))  # two 3/4/5 triangles
    [(0.0, 0.0), (0.0, 8.0)]
    >>> rtl(circleIntersections((-4, -3), (4, -3), 5, 5))  # two 3/4/5 triangles
    [(0.0, -6.0), (0.0, 0.0)]
    >>> rtl(circleIntersections((0.0, 0.0), (0.0, 0.0), 5, 5))  # infinity
    [(5.0, 0.0), (0.0, -5.0), (-5.0, 0.0), (0.0, 5.0)]
    """
    x1, y1 = a
    x2, y2 = b

    d = distance(a, b)

    # If the circles are too far apart or if the distance between their
    # centers is so small compared to the difference between their radii
    # that one is entirely inside the other, there are no points of
    # intersection.
    if d > aRadius + bRadius or d < abs(aRadius - bRadius):
        return []
    elif aRadius + bRadius == d:  # one point of intersection
        vec = scaleTo((x2 - x1, y2 - y1), aRadius)
        return [ (x1 + vec[0], y1 + vec[1]) ]
    elif x1 == x2 and y1 == y2 and aRadius == bRadius:  # same circle
        return [  # clockwise from 3 o'clock if +y is up and +x is right
            (x1 + aRadius, y1),
            (x1, y1 - aRadius),
            (x1 - aRadius, y1),
            (x1, y1 + aRadius)
        ]

    # Otherwise we have 2 points of intersection
    # TODO: Explain this math a bit...
    a = (aRadius**2 - bRadius**2 + d**2) / (2 * d)
    h = (aRadius**2 - a**2)**0.5

    x0 = x1 + a * (x2 - x1) / d
    y0 = y1 + a * (y2 - y1) / d

    x3 = x0 + h * (y2 - y1) / d
    y3 = y0 - h * (x2 - x1) / d

    x4 = x0 - h * (y2 - y1) / d
    y4 = y0 + h * (x2 - x1) / d

    return [(x3, y3), (x4, y4)]


def bestFitIntersection(
    a: base.LayoutPosition,
    b: base.LayoutPosition,
    aRad: Number,
    bRad: Number
):
    """
    Given two circles which may or may not intersect (specified as
    centers `a` and `b` plus respective radii), returns a point that's 
    on the line through their centers that's on the shortest segment of
    that line which connects one circle to the other (this may or may
    not be between the two centers if one circle encircles the other).

    The point is placed along that segment so that its distance from
    circle a divided by its distance from circle b is proportional to
    the radius of circle a divided by the radius of circle b (it ends up
    closer to the smaller circle).

    If the two circles have the same center, we return a point that has
    the same y-coordinate as that center, and of the two equally valid
    points of that nature, we return the one with the greater
    x-coordinate.

    Some examples:
    >>> rt(bestFitIntersection((0, 0), (100, 0), 180, 40))
    (147.272727, 0.0)
    >>> rt(bestFitIntersection((0, 0), (50, 87), 60, 78))
    (21.73913, 37.826087)
    >>> rt(bestFitIntersection((100, 0), (50, 87), 70, 78))
    (76.351351, 41.148649)

    >>> rt(bestFitIntersection((0, 0), (8, 6), 5, 5))  # circles touch
    (4.0, 3.0)
    >>> rt(bestFitIntersection((0, 0), (12, 9), 10, 5))  # circles touch
    (8.0, 6.0)
    >>> rt(bestFitIntersection((-20, -20), (-30, 20), 10, 10))  # r1 == r2
    (-25.0, 0.0)
    >>> rt(bestFitIntersection((-30, 20), (-20, -20), 10, 10))  # other order
    (-25.0, 0.0)
    >>> rt(bestFitIntersection((0, 0), (0, 0), 12, 24))  # same center
    (16.0, 0.0)
    >>> # we arbitrarily pick a point horizontal from the center
    >>> # note that (-16.0, 0.0) is equally valid but we pick the option
    >>> # with the higher x-coordinate
    >>> rt(bestFitIntersection((0, 0), (0, 0), 24, 12))  # works same other way
    (16.0, 0.0)
    >>> rt(bestFitIntersection((0, 0), (0, 0), 10, 10))  # same circle
    (10.0, 0.0)
    >>> rt(bestFitIntersection((0, 0), (0, 0), 0, 0))  # zero-radius same center
    (0.0, 0.0)
    >>> rt(bestFitIntersection((0, 0), (2, 0), 0, 0))  # zero-radius diff center
    (1.0, 0.0)
    >>> rt(bestFitIntersection((2, 0), (0, 0), 0, 0))  # other direction
    (1.0, 0.0)
    >>> rt(bestFitIntersection((0, 0), (2, 0), 1, 0))  # single zero-radius
    (2.0, 0.0)
    """
    import sys
    dist = distance(a, b)
    vect = norm(vSub(b, a))
    if vect == (0.0, 0.0):  # same center
        vect = (1.0, 0.0)  # horizontal

    # Find all four points at which the line between a and b intersects
    # the a and b circles:
    aVec = scaleBy(vect, aRad)
    aLow = vSub(a, aVec)
    aHigh = vAdd(a, aVec)
    bVec = scaleBy(vect, bRad)
    bLow = vSub(b, bVec)
    bHigh = vAdd(b, bVec)

    # Now find which pair of one point from A and one from B is closest
    # There's probably a more mathy way to do this, but this is simple to
    # reason about.
    closest = None
    bestDist = None
    for (p1, p2) in [
        (aHigh, bHigh),
        (aHigh, bLow),
        (aLow, bHigh),
        (aLow, bLow),
    ]:
        pointSep = distance(p1, p2)
        # Note strict < here biases towards earlier pairs in the order
        # above, such that 'high' points beat low ones on ties
        if closest is None or pointSep < bestDist:
            closest = (p1, p2)
            bestDist = pointSep

    # Now find a point between the two closest points-on-circle where the
    # proportion between distances to each matches the ratio of the radii
    # of the circles:
    onA, onB = closest
    between = vSub(onB, onA)
    if between == (0.0, 0.0):  # same point, so return it
        return onA
    dirBetween = norm(between)
    distBetween = distance(onA, onB)
    if aRad + bRad == 0:  # both zero-radius; return average of the two
        return ((onA[0] + onB[0]) / 2, (onA[1] + onB[1]) / 2)
    howFarAlong = aRad / (aRad + bRad)
    return vAdd(onA, scaleBy(dirBetween, howFarAlong * distBetween))


def baryeccentricPosition(
    a: base.LayoutPosition,
    b: base.LayoutPosition,
    c: base.LayoutPosition,
    distA: Number,
    distB: Number,
    distC: Number
):
    """
    Returns a "baryeccentric" position given three reference points and
    three numbers indicating distances to each of them. If the distances
    are in agreement and together specify a particular point within (or
    outside of) the reference triangle, we return that point. If the
    two or more of the distances are too short to touch each other, we
    compromise at a position most consistent with them, and if the
    distances are too long we also compromise.

    For best results, you should ensure that the reference points make a
    triangle rather than a line or point.

    We find a compromise by treating each reference point + distance as a
    circle. We first compute the intersection points between each pair of
    circles, resulting in 0-4 intersection points per pair (see
    `circleIntersection`). For pairs with no intersection, we use
    `bestFitIntersection` to come up with a single "intersection" point.
    Now for pairs with 2+ intersection points, we pick the single
    intersection point whose distance to the third point is most
    consistent with the measured third distance. This leaves us with 3
    intersection points: one for each pair of reference points. We
    average these three points to come up with the final result.

    TODO: consider the perfectly-overlapping circles case a bit more...

    Some examples:

    >>> baryeccentricPosition((0, 0), (6, 8), (6, 0), 5, 5, 5)
    (3.0, 4.0)
    >>> baryeccentricPosition((0, 0), (-6, 8), (-6, 0), 5, 5, 5)
    (-3.0, 4.0)
    >>> baryeccentricPosition((0, 0), (-6, -8), (-6, 0), 5, 5, 5)
    (-3.0, -4.0)
    >>> baryeccentricPosition((0, 0), (3.0, 4.0), (3.0, 0), 5, 0, 4)
    (3.0, 4.0)
    >>> baryeccentricPosition((0, 0), (3.0, 4.0), (3.0, 0), 0, 5, 3)
    (0.0, 0.0)
    >>> baryeccentricPosition((0, 0), (3.0, 4.0), (3.0, 0), 3, 4, 0)
    (3.0, 0.0)
    >>> rt(baryeccentricPosition((-8, 6), (8, 6), (0, -10), 10, 10, 10))
    (0.0, 0.0)
    >>> rt(baryeccentricPosition((-8, 6), (8, 6), (0, -12), 10, 10, 0))
    (0.0, -8.0)
    >>> rt(baryeccentricPosition((-8, -6), (0, 12), (8, -6), 10, 0, 10))
    (0.0, 8.0)
    >>> rt(baryeccentricPosition((0, 12), (-8, -6), (8, -6), 0, 10, 10))
    (0.0, 8.0)
    >>> rt(baryeccentricPosition((-4, 3), (4, 3), (0, -5), 5, 5, 0))
    (0.0, -3.333333)
    >>> rt(baryeccentricPosition((-1, 0), (1, 0), (0, -1), 1, 1, 1))
    (0.0, 0.0)
    >>> rt(baryeccentricPosition(
    ...     (-25.3, 45.8), (12.4, -24.3), (35.9, 58.2),
    ...     61.2, 35.5, 28.4
    ... ))
    (27.693092, 20.240286)
    >>> rt(baryeccentricPosition(
    ...     (-25.3, 45.8), (12.4, -24.3), (35.9, 58.2),
    ...     102.5, 12.8, 89.4
    ... ))
    (28.437607, -32.62218)

    Edge case examples:

    >>> baryeccentricPosition((0, 0), (0, 0), (0, 0), 5, 5, 5)
    (5.0, 0.0)
    >>> baryeccentricPosition((0, 0), (0, 0), (0, 0), 0, 0, 0)
    (0.0, 0.0)
    """
    # TODO: Should we print a warning if the points aren't a triangle?

    # First, find intersection point(s) for each pair
    abPoints = circleIntersections(a, b, distA, distB)
    acPoints = circleIntersections(a, c, distA, distC)
    bcPoints = circleIntersections(b, c, distB, distC)

    # if circles don't touch, add an estimated point
    if len(abPoints) == 0:
        abPoints = [bestFitIntersection(a, b, distA, distB)]
    if len(acPoints) == 0:
        acPoints = [bestFitIntersection(a, c, distA, distC)]
    if len(bcPoints) == 0:
        bcPoints = [bestFitIntersection(b, c, distB, distC)]

    # If circles touch a multiple places, narrow that down to one by
    # figuring out which is most consistent with the third distance
    if len(abPoints) == 1:
        abPoint = abPoints[0]
    else:  # must be > 1 point per above
        assert len(abPoints) > 1
        abPoint = None
        bestError = None
        for p in abPoints:
            thirdDist = distance(p, c)
            error = abs(thirdDist - distC)
            if abPoint is None or error < bestError:
                abPoint = p
                bestError = error

    if len(acPoints) == 1:
        acPoint = acPoints[0]
    else:  # must be > 1 point per above
        assert len(acPoints) > 1
        acPoint = None
        bestError = None
        for p in acPoints:
            thirdDist = distance(p, b)
            error = abs(thirdDist - distB)
            if acPoint is None or error < bestError:
                acPoint = p
                bestError = error

    if len(bcPoints) == 1:
        bcPoint = bcPoints[0]
    else:  # must be > 1 point per above
        assert len(bcPoints) > 1
        bcPoint = None
        bestError = None
        for p in bcPoints:
            thirdDist = distance(p, a)
            error = abs(thirdDist - distA)
            if bcPoint is None or error < bestError:
                bcPoint = p
                bestError = error

    # At this point, ab/ac/bc point variables should be assigned properly
    return (
        (abPoint[0] + acPoint[0] + bcPoint[0]) / 3,
        (abPoint[1] + acPoint[1] + bcPoint[1]) / 3,
    )


def baryeccentricLayout(
    exploration: core.DiscreteExploration,
    specifiedNodes: Optional[base.Layout] = None
) -> base.Layout:
    """
    Computes a baryeccentric coordinate layout for all decisions in the
    final step of the given exploration, using the specified positions
    of a few nodes given in `specifiedNodes`. `specifiedNodes` should
    specify positions for at least 3 decisions, and those positions must
    form a triangle, not a line or point. If `specifiedNodes` does not
    contain enough decisions (or if it's not provided), decisions will
    be added to it as follows:

    - If it's empty, add the node with the lowest id at position (0, 0).
    - If it's got only one decision or we just added one node, add the
        node that's furthest from that node in terms of hop distance.
        We'll position this second node at the same y-coordinate as the
        first, but with an x-coordinate equal to the hop distance between
        it and the first node. If multiple nodes are tied for furthest,
        add the one with the lowest id.
    - If it's got only two decisions or we just added one or two, add the
        node whose sum of hop distances to the two already selected is
        largest. We position this third node such that the hop distances
        to each of the already-placed nodes are respected and it forms a
        triangle, or if that's not possible due to those distances being
        too short, we position it partway between them proportional to
        those two distances with an artificial offset perpendicular to
        the line between the two other points. Ties are broken towards
        nodes with a shorter max hop distance to either of the two
        already-placed nodes, and then towards lower node IDs.

    If the number of nodes in the entire graph is 1 or 2, we return a
    layout positioning the first node at (0, 0) and (if it exists) the
    second node at (1, 0).

    Some examples:

    # TODO
    >> baryeccentricLayout(TODO)
    """
    hops = analysis.shortestHopPaths(
        exploration,
        lambda src, transition, dst, graph: (
            'journey' not in graph.transitionTags(src, transition)
        )
    )
    # Now we can use `analysis.hopDistnace` given `hops` plus two
    # decision IDs to get the hop distance between any two decisions.

    # Create empty layout by default:
    if specifiedNodes is None:
        specifiedNodes = {}

    # Select at least 3 specific nodes
    if len(specifiedNodes) < 3:
        finalGraph = exploration[-1].graph
        allDecisions = sorted(finalGraph)

        # Bail out if we have fewer than 3 total decisions
        if len(allDecisions) < 3:
            result = {}
            result[allDecisions[0]] = (0.0, 0.0)
            if len(allDecisions) > 1:
                result[allDecisions[1]] = (1.0, 0.0)
            return result

        # Add a decision at (0, 0) if we didn't have any specified
        if len(specifiedNodes) < 1:
            # Find largest weakly connected component:
            bigCC = max(nx.weakly_connected_components(finalGraph), key=len)
            # Use an arbitrary node from that component
            specifiedNodes[list(bigCC)[0]] = (0.0, 0.0)

        assert len(specifiedNodes) >= 1

        # If 1 specified or just added, add furthest-away decision
        if len(specifiedNodes) < 2:
            first = list(specifiedNodes)[0]
            best = None
            bestDist = None
            # Find furthest connected node
            for dID in allDecisions:
                if dID == first:
                    # Skip node that we already assigned
                    continue
                dist = analysis.hopDistance(hops, dID, first)
                # Note > here breaks ties towards lower IDs
                if dist is not None and (bestDist is None or dist > bestDist):
                    best = dID
                    bestDist = dist
            # if no nodes are connected, we've got a big problem, but
            # we'll push on by selecting the node with the second-lowest
            # node ID.
            if best is None:
                # Find first un-specified node ID:
                second = None
                for second in allDecisions:
                    dFirst = analysis.hopDistance(hops, second, first)
                    if (
                         second not in specifiedNodes
                     and dFirst is not None
                    ):
                        # second will remain at this value after loop
                        break
                else:  # if we never hit break
                    for second in allDecisions:
                        if second not in specifiedNodes:
                            # second will remain at this value after loop
                            break
                assert second is not None
                # Just put it at (1, 0) since hops aren't informative
                specifiedNodes[second] = (1.0, 0.0)
            else:
                assert best != first
                firstPos = specifiedNodes[first]
                # Same y-value as first one, with x-dist as hop dist
                specifiedNodes[best] = (firstPos[0] + bestDist, firstPos[1])

        assert len(specifiedNodes) >= 2

        # If only two specified (and or one or two just added) we look
        # for the node with best combined distance to those two,
        # breaking ties towards smaller max-distance to either and then
        # towards smaller ID values.
        if len(specifiedNodes) < 3:
            first, second = list(specifiedNodes)[:2]
            best = None
            bestCombined = None
            bestLonger = None
            bestDists = None
            for dID in allDecisions:
                if dID in specifiedNodes:
                    # Skip already-placed nodes
                    continue
                distA = analysis.hopDistance(hops, dID, first)
                distB = analysis.hopDistance(hops, dID, second)
                if distA is None or distB is None:
                    # Note: *shouldn't* be possible for only one to be
                    # None, but we don't take chances here
                    continue
                combined = distA + distB
                longer = max(distA, distB)
                if (
                    # first one
                    best is None
                    # better combined distance (further away)
                 or combined > bestCombined
                    # tied combined and better max distance (more evenly
                    # placed between at *shorter* max dist)
                 or (
                        combined == bestCombined
                    and longer < bestLonger
                        # Note strict < here breaks ties towards lower IDs
                    )
                ):
                    best = dID
                    bestCombined = combined
                    bestLonger = longer
                    bestDists = (distA, distB)

            firstPos = specifiedNodes[first]
            secondPos = specifiedNodes[second]

            abDist = analysis.hopDistance(hops, first, second)
            # Could happen if only two nodes are connected, for example
            if best is None or sum(bestDists) < abDist:
                # Just put it artificially between them
                vect = (
                    secondPos[0] - firstPos[0],
                    secondPos[1] - firstPos[1]
                )
                # perpendicular vector
                ortho = (vect[1], -vect[0])
                # Just use first decision that's not already specified
                if best is not None:
                    third = best
                else:
                    third = None
                    for third in allDecisions:
                        thirdHopsA = analysis.hopDistance(hops, first, third)
                        thirdHopsB = analysis.hopDistance(hops, second, third)
                        if (
                             third not in specifiedNodes
                         and thirdHopsA is not None
                         and thirdHopsB is not None
                        ):
                            # third will remain on this node
                            break
                    else:  # if we never hit the break
                        for third in allDecisions:
                            if third not in specifiedNodes:
                                # third will remain on this node
                                break
                    assert third is not None
                assert third != first
                assert third != second
                # Offset orthogonally by half the distance between
                specifiedNodes[third] = (
                    firstPos[0] + vect[0]/2 + ortho[0]/2,
                    firstPos[1] + vect[1]/2 + ortho[0]/2
                )
            else:
                # Position the best candidate to form a triangle where
                # distances are proportional; we know distances are long
                # enough to make a triangle
                distA = analysis.hopDistance(hops, dID, first)
                candidates = circleIntersections(
                    firstPos,
                    secondPos,
                    *bestDists
                )
                if len(candidates) == 0:
                    where = bestFitIntersection(
                        first,
                        second,
                        distA,
                        distB
                    )
                else:
                    where = candidates[0]
                assert best != first
                assert best != second
                specifiedNodes[best] = where

            assert len(specifiedNodes) >= 3

    # TODO: Don't just use first 3 here...
    # Grab first 3 decision IDs from layout
    a, b, c = list(specifiedNodes.keys())[:3]
    # Get their positions
    aPos = specifiedNodes[a]
    bPos = specifiedNodes[b]
    cPos = specifiedNodes[c]
    # create initial result using just specified positions
    result = {
        a: aPos,
        b: bPos,
        c: cPos
    }
    # Now we need to compute positions of each other node...
    # We use `exploration.allDecisions` as the set of nodes we want to
    # establish positions for, even though some of them may have been
    # deleted by the end and thus may not appear in our hops data.
    toLayOut = exploration.allDecisions()
    # value for default positions
    default = 1.0
    print("Using decisions:")
    print(a, exploration.latestDecisionInfo(a)["name"])
    print(b, exploration.latestDecisionInfo(b)["name"])
    print(c, exploration.latestDecisionInfo(c)["name"])
    for decision in toLayOut:
        aHops = analysis.hopDistance(hops, a, decision)
        bHops = analysis.hopDistance(hops, b, decision)
        cHops = analysis.hopDistance(hops, c, decision)

        # if hops is none for one, it should be none for all
        if aHops is None or bHops is None or cHops is None:
            # Put it at a default position on a parabola
            # TODO: Better default here?
            result[decision] = (default, default**1.1)
            default += 0.1
        else:
            assert aHops is not None
            assert bHops is not None
            assert cHops is not None

            # Place according to baryeccentric position
            result[decision] = baryeccentricPosition(
                aPos,
                bPos,
                cPos,
                aHops,
                bHops,
                cHops
            )

    # Return result at end...
    return result

def setBaryeccentricPositions(
    exploration: core.DiscreteExploration,
    method: GraphLayoutMethod = "square"
) -> None:
    """
    Adds a "baryeccentric" layout to the given exploration.
    """
    exploration.layouts["baryeccentric"] = baryeccentricLayout(
        exploration,
        {}
    )

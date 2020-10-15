class Node():
    """
    Node class, represents a point on the truss.

    ...

    Attributes
    ----------
    id : int
        Id of the node.
    x : float
        x coordinate.
    y : float
        y coordinate.
    z : float
        z coordinate.

    """

    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

class Node():
    """
    Node class, represents a point on the truss.

    ...

    Attributes
    ----------
    id : str
        Id of the node.
    index : int
        Index of the node.
    x : float
        x coordinate.
    y : float
        y coordinate.
    z : float
        z coordinate.

    """

    def __init__(self, id, index, x, y, z):
        self.id = id
        self.index = index
        self.x = x
        self.y = y
        self.z = z

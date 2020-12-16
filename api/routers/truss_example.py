TrussExampleInput = {
    "matProp": [{
            "ele": "ele1",
            "E": 2000000,
            "A": 2
        }, {
            "ele": "ele2",
            "E": 2000000,
            "A": 2
        }, {
            "ele": "ele3",
            "E": 2000000,
            "A": 1
        }, {
            "ele": "ele4",
            "E": 2000000,
            "A": 1
        },
    ],
    "nodalCoords": [{
            "id": "node1",
            "x": 0,
            "y": 0,
            "z": 0
        }, {
            "id": "node2",
            "x": 100,
            "y": 0,
            "z": 0
        }, {
            "id": "node3",
            "x": 50,
            "y": 50,
            "z": 0
        }, {
            "id": "node4",
            "x": 200,
            "y": 100,
            "z": 0
        },
    ],
    "connectivity": [{
            "id": "ele1",
            "i": "node1",
            "j": "node3"
        }, {
            "id": "ele2",
            "i": "node3",
            "j": "node2"
        }, {
            "id": "ele3",
            "i": "node3",
            "j": "node4"
        }, {
            "id": "ele4",
            "i": "node2",
            "j": "node4"
        },
    ],
    "forceVector": [{
            "node": "node4",
            "u1": 0,
            "u2": -1000,
            "u3": 0
        },
    ],
    "boundaryConditions": [{
            "node": "node1",
            "u1": True,
            "u2": True,
            "u3": True
        }, {
            "node": "node2",
            "u1": True,
            "u2": True,
            "u3": True
        }, {
            "node": "node3",
            "u1": False,
            "u2": False,
            "u3": True
        }, {
            "node": "node4",
            "u1": False,
            "u2": False,
            "u3": True
        },
    ],
    "stresses": []
}

TrussExampleOutput = {
    "matProp": [{
            "ele": "ele1",
            "E": 2000000,
            "A": 2
        }, {
            "ele": "ele2",
            "E": 2000000,
            "A": 2
        }, {
            "ele": "ele3",
            "E": 2000000,
            "A": 1
        }, {
            "ele": "ele4",
            "E": 2000000,
            "A": 1
        },
    ],
    "nodalCoords": [{
            "id": "node1",
            "x": 0,
            "y": 0,
            "z": 0
        }, {
            "id": "node2",
            "x": 100,
            "y": 0,
            "z": 0
        }, {
            "id": "node3",
            "x": 50.0265165042945,
            "y": 50.00883883476483,
            "z": 0
        }, {
            "id": "node4",
            "x": 200.34790254476266,
            "y": 99.43996542088136,
            "z": 0
        },
    ],
    "connectivity": [{
            "id": "ele1",
            "i": "node1",
            "j": "node3"
        }, {
            "id": "ele2",
            "i": "node3",
            "j": "node2"
        }, {
            "id": "ele3",
            "i": "node3",
            "j": "node4"
        }, {
            "id": "ele4",
            "i": "node2",
            "j": "node4"
        },
    ],
    "forceVector": [{
            "node": "node4",
            "u1": 0,
            "u2": -1000,
            "u3": 0
        },
    ],
    "boundaryConditions": [{
            "node": "node1",
            "u1": True,
            "u2": True,
            "u3": True
        }, {
            "node": "node2",
            "u1": True,
            "u2": True,
            "u3": True
        }, {
            "node": "node3",
            "u1": False,
            "u2": False,
            "u3": True
        }, {
            "node": "node4",
            "u1": False,
            "u2": False,
            "u3": True
        },
    ],
    "stresses": [{
            "ele": "ele1",
            "vm": 707.1067811865494
        }, {
            "ele": "ele2",
            "vm": -353.5533905932747
        }, {
            "ele": "ele3",
            "vm": 1581.138830084193
        }, {
            "ele": "ele4",
            "vm": -2121.320343559646
        },
    ]
}

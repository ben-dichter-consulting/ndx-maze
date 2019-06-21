from ndx_maze import Environment, PointNode, SegmentNode, PolygonNode, Edge

from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime
from numpy.testing import assert_array_equal

sleep_box_polygon_coords = [[1.1, 0.7], [1.1, 1.4], [1.95, 1.4], [1.95, 0.7]]

wtrackA_segments = {'left_arm': [[1.4, 0.73], [1.99, 0.77]],
                    'left_branch': [[1.99, 0.77], [1.97, 1.15]],
                    'middle_arm': [[1.38, 1.1], [1.97, 1.15]],
                    'right_branch': [[1.97, 1.15], [1.95, 1.5]],
                    'right_arm': [[1.37, 1.4], [1.95, 1.5]]}

wtrackA_reward_wells = {'left_reward_well': [1.4, 0.73],
                        'middle_reward_well': [1.38, 1.1],
                        'right_reward_well': [1.37, 1.4]}

edge_pairs = [('left_arm', 'left_branch'),
              ('left_branch', 'middle_arm'),
              ('middle_arm', 'right_branch'),
              ('right_branch', 'right_arm'),
              ('left_branch', 'right_branch'),
              ('right_branch', 'right_reward_well'),
              ('left_branch', 'left_reward_well'),
              ('middle_branch', 'middle_reward_well')]

segments = [SegmentNode(name=key, coords=val)
            for key, val in wtrackA_segments.items()]

points = [PointNode(name=key, coords=[val])
          for key, val in wtrackA_reward_wells.items()]

w_maze = Environment(
    name='w_maze',
    edges=[Edge(name=n[0] + '<->' + n[1], edge_nodes=n) for n in edge_pairs],
    nodes=segments+points)

sleep_box = Environment(
    name='sleep_box',
    nodes=[
        PolygonNode(
            name='sleep_box',
            coords=sleep_box_polygon_coords
        )
    ]
)

session_start_time = datetime.now().astimezone()
nwb = NWBFile('session_description', 'identifier', session_start_time)

behavior_module = nwb.create_processing_module('behavior', 'behavior module')
behavior_module.add(w_maze)
behavior_module.add(sleep_box)

with NWBHDF5IO('test_maze.nwb', 'w') as io:
    io.write(nwb)

with NWBHDF5IO('test_maze.nwb', 'r') as io:
    nwb2 = io.read()
    assert_array_equal(nwb2.processing['behavior'].
                       data_interfaces['w_maze'].
                       nodes['left_arm'].coords[:],
                       w_maze.nodes['left_arm'].coords[:])

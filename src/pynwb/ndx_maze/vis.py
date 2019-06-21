import matplotlib.pyplot as plt
import numpy as np

from ndx_maze import Environment, PointNode, SegmentNode, PolygonNode, Node


def show_node(node: Node, ax=None):
    if isinstance(node, PointNode):
        show_point_node(node, ax=ax)
    elif isinstance(node, SegmentNode):
        show_segment_node(node, ax=ax)
    elif isinstance(node, PolygonNode):
        show_polygon_node(node, ax=ax)


def show_segment_node(segment_node: SegmentNode, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    coords = np.array(segment_node.coords)
    ax.plot(coords[:, 0], coords[:, 1], 'k-')


def show_point_node(point_node: PointNode, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    coords = np.array(point_node.coords)
    ax.plot(coords[0, 0], coords[0, 1], 'o')


def show_polygon_node(polygon_node: PolygonNode, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    coords = np.array(polygon_node.coords)
    coords = np.vstack((coords, coords[0, :]))
    ax.plot(coords[:, 0], coords[:, 1], 'k-')

    if hasattr(polygon_node, 'inner_coords'):
        coords = np.array(polygon_node.inner_coords)
        coords = np.vstack((coords, coords[0, :]))
        ax.plot(coords[:, 0], coords[:, 1], 'k-')


def show_environment(environment: Environment, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    for node in environment.nodes.values():
        show_node(node, ax=ax)
    ax.set_xlabel('meters')
    ax.set_ylabel('meters')
    return ax.figure


neurodata_type_vis_dict = {Environment: show_environment}

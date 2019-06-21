import os
from pynwb import load_namespaces, get_class
from os import path

from pynwb.file import MultiContainerInterface
from pynwb import register_class
from pynwb.file import LabMetaData

name = 'ndx-maze'

here = path.abspath(path.dirname(__file__))
ns_path = os.path.join(here, 'spec', name + '.namespace.yaml')

load_namespaces(ns_path)


Node = get_class('Node', name)
Edge = get_class('Edge', name)
PointNode = get_class('PointNode', name)
SegmentNode = get_class('SegmentNode', name)
PolygonNode = get_class('PolygonNode', name)


@register_class('Environment', name)
class Environment(MultiContainerInterface):
    """
    Purpose:
        Topological graph representing connected components of a beahvioral Environment.

    Arguments:
        name (str): name of this Environment
        nodes (list): list of Node objects contained in this Environment
        edges (list): list of Edge objects contained in this Environment

    """

    __nwbfields__ = ('name', 'edges', 'nodes')

    __clsconf__ = [
        {
            'attr': 'edges',
            'type': Edge,
            'add': 'add_edge',
            'get': 'get_edge'
        },
        {
            'attr': 'nodes',
            'type': Node,
            'add': 'add_node',
            'get': 'get_node'
        }
    ]
    __help = 'info about an Environment'


@register_class('Environments', name)
class Environments(MultiContainerInterface, LabMetaData):
        """
        Purpose:
            Topological graph representing connected components of a behavioral Environment.

        Arguments:
            name (str): name of this Environment
            environments (list): list of Environment objects

        """

        __nwbfields__ = ('name', 'environments')

        __clsconf__ = [{
                'attr': 'environments',
                'type': Environment,
                'add': 'add_environment',
                'get': 'get_environment'
            }, ]
        __help = 'info about an Environment'


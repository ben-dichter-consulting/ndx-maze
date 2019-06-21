
from pynwb.spec import (
    NWBNamespaceBuilder,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBDatasetSpec
)

from export_spec import export_spec


def main():
    ns_builder = NWBNamespaceBuilder(doc='describe a maze of arbitrary shape',
                                     name='ndx-maze',
                                     version='0.1.0',
                                     author='Ben Dichter',
                                     contact='ben.dichter@gmail.com')

    node = NWBGroupSpec(neurodata_type_def='Node',
                        neurodata_type_inc='NWBDataInterface',
                        doc="Abstract representation for any kind of node in the topological graph We won't actually"
                            " implement abstract nodes. Rather this is a parent group from which our more specific "
                            "types of nodes will inherit. Note that NWB specifications have inheritance. The quantity "
                            "'*' means that we can have any number (0 or more) nodes.",
                        quantity='*',
                        attributes=[NWBAttributeSpec('name', 'the name of this node', 'text'),
                                    NWBAttributeSpec(name='help', doc='help doc', dtype='text',
                                                     value='Apparatus Node')])

    edge = NWBGroupSpec(neurodata_type_def='Edge',
                        neurodata_type_inc='NWBDataInterface',
                        doc="Edges between any two nodes in the graph. An edge's only dataset is the name (string) of "
                            "the two nodes that the edge connects Note that we don't actually include the nodes "
                            "themselves, just their names, in an edge.",
                        quantity='*',
                        datasets=[NWBDatasetSpec(doc='names of the nodes this edge connects',
                                                 name='edge_nodes',
                                                 dtype='text',
                                                 dims=['first_node_name|second_node_name'],
                                                 shape=[2])],
                        attributes=[
                            NWBAttributeSpec(name='help', doc='help doc', dtype='text', value='Apparatus Edge')])

    point_node = NWBGroupSpec(neurodata_type_def='PointNode',
                              neurodata_type_inc='Node',
                              doc='A node that represents a single 2D point in space (e.g. reward well, novel object'
                                  ' location)',
                              quantity='*',
                              datasets=[NWBDatasetSpec(doc='x/y coordinate of this 2D point',
                                                       name='coords',
                                                       dtype='float',
                                                       dims=['num_coords', 'x_vals|y_vals'],
                                                       shape=[1, 2])],
                              attributes=[
                                  NWBAttributeSpec(name='help', doc='help doc', dtype='text', value='Apparatus Point')])

    segment_node = NWBGroupSpec(neurodata_type_def='SegmentNode',
                                neurodata_type_inc='Node',
                                doc='A node that represents a linear segment in 2D space, defined by its start and end'
                                    ' points (e.g. a single arm of W-track maze)',
                                quantity='*',
                                datasets=[
                                    NWBDatasetSpec(doc='x/y coordinates of the start and end points of this segment',
                                                   name='coords',
                                                   dtype='float',
                                                   dims=['num_coords', 'x_vals|y_vals'],
                                                   shape=[None, 2])],
                                attributes=[NWBAttributeSpec(name='help', doc='help doc', dtype='text',
                                                             value='Apparatus Segment')])

    polygon_node = NWBGroupSpec(neurodata_type_def='PolygonNode',
                                neurodata_type_inc='Node',
                                doc='A node that represents a polygon area (e.g. open field, sleep box). A polygon is'
                                    ' defined by its external vertices and, optionally, by any interior points of '
                                    'interest (e.g. interior wells, objects)',
                                quantity='*',
                                datasets=[NWBDatasetSpec(doc='x/y coordinates of the exterior points of this polygon',
                                                         name='coords',
                                                         dtype='float',
                                                         dims=['num_coords', 'x_vals|y_vals'],
                                                         shape=[None, 2]),
                                          NWBDatasetSpec(doc='x/y coordinates of interior points inside this polygon',
                                                         name='interior_coords',
                                                         dtype='float',
                                                         quantity='?',
                                                         dims=['num_coords', 'x_vals|y_vals'],
                                                         shape=[None, 2])],
                                attributes=[NWBAttributeSpec(name='help', doc='help doc', dtype='text',
                                                             value='Apparatus Polygon')])

    environment = NWBGroupSpec(neurodata_type_def='Environment',
                               neurodata_type_inc='NWBDataInterface',
                               default_name='Environment',
                               doc='a graph of nodes and edges',
                               quantity='*',
                               groups=[
                                   NWBGroupSpec(neurodata_type_inc='Node',
                                                doc='nodes in the graph',
                                                quantity='*'),
                                   NWBGroupSpec(neurodata_type_inc='Edge',
                                                doc='edges in the graph',
                                                quantity='*')
                               ],
                               attributes=[NWBAttributeSpec(name='name', doc='the name of this apparatus', dtype='text'),
                                           NWBAttributeSpec(name='help', doc='help doc', dtype='text',
                                                            value='Behavioral Apparatus')])

    new_data_types = [node, edge, point_node, segment_node, polygon_node, environment]

    # TODO: include the types that are used and their namespaces (where to find them)
    ns_builder.include_type('NWBDataInterface', namespace='core')

    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    main()

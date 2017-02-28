#!/usr/bin/env python

from yaml import load, Loader, dump
from argparse import ArgumentParser
import graphviz as gv
from os.path import basename

from IncludeGraph import IncludeGraph

include_graph = IncludeGraph()

call_graph_flag = False
call_graph = gv.Digraph(format='svg')
call_graph.body.extend(['rankdir=LR', 'size="8,5"'])
call_list = []

def include_constructor(loader, node):
    v = unfold_yaml(node.value)

    return v

def include_raw_constructor(loader, node):

    include_graph.add_node(node.value)
    include_graph.add_edge_from_last_node(node.value, 
                label='<<B>include-raw</B>>', color='include_raw_color')

    text = open(node.value, 'r').read()
    
    return text

def unfold_yaml(file_name):
    include_graph.add_node(file_name)
    include_graph.add_to_list(file_name)

    text = open(file_name, 'r') 
    initial_dict = load(text)

    if len(include_graph.include_list) >= 2:
        include_graph.pop_from_list()
        include_graph.add_edge_from_last_node(file_name, 
                label='<<B>include</B>>', color='include_color')
    return initial_dict

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--include-graph', default = include_graph.active)
    parser.add_argument('--call-graph', default = call_graph_flag)
    args = parser.parse_args()

    include_graph.active = args.include_graph
    call_graph_flag = args.call_graph

    Loader.add_constructor('!include:', include_constructor)
    Loader.add_constructor('!include-raw:', include_raw_constructor)
    Loader.add_constructor('!include', include_constructor)
    unfolded_yaml = unfold_yaml(args.file)
    #print(dump(unfolded_yaml, default_flow_style=False))

    if include_graph.active: 
        export_name = basename(args.file) + '_include'
        include_graph.render(export_name)

    if call_graph_flag:
        export_name = basename(args.file) + '_call'
        call_graph.render(export_name)

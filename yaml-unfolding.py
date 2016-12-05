#!/usr/bin/env python

from yaml import load, Loader, dump
from argparse import ArgumentParser
import graphviz as gv
from os.path import basename

include_graph_flag = True
include_graph = gv.Digraph(format='svg')
include_graph.body.extend(['rankdir=LR', 'size="8,5"'])
include_list = []

call_graph_flag = False
call_graph = gv.Digraph(format='svg')
call_graph.body.extend(['rankdir=LR', 'size="8,5"'])
call_list = []

def include_constructor(loader, node):
    return unfold_yaml(node.value)

def include_raw_constructor(loader, node):
    if include_graph_flag:
        include_graph.node(node.value)
        include_graph.edge(include_list[-1],node.value, label='include-raw')
    text = open(node.value, 'r').read()
    
    return text

def unfold_yaml(file_name):
    if include_graph_flag:
        include_graph.node(file_name)
        include_list.append(file_name)

    text = open(file_name, 'r') 
    initial_dict = load(text)

    if include_graph_flag and len(include_list) >= 2:
        include_list.pop()
        include_graph.edge(include_list[-1], file_name, label='include') 
    return initial_dict

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--include-graph', default = include_graph_flag)
    parser.add_argument('--call-graph', default = call_graph_flag)
    args = parser.parse_args()

    include_graph_flag = args.include-graph
    call_graph_flag = args.call-graph

    Loader.add_constructor('!include:', include_constructor)
    Loader.add_constructor('!include-raw:', include_raw_constructor)
    Loader.add_constructor('!include', include_constructor)
    unfolded_yaml = unfold_yaml(args.file)
    print(dump(unfolded_yaml, default_flow_style=False))

    if include_graph_flag: 
        export_name = basename(args.file) + '_include'
        include_graph.render(export_name)

    if call_graph_flag:
        

        export_name = basename(args.file) + '_call'
        call_graph.render(export_name)

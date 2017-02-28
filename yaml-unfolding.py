#!/usr/bin/env python

from yaml import load, Loader, dump
from argparse import ArgumentParser
import graphviz as gv
from os.path import basename
import os

from include_graph import IncludeGraph
from file_index import FileIndex

include_graph = IncludeGraph()

call_graph_flag = False
call_graph = gv.Digraph(format='svg')
call_graph.body.extend(['rankdir=LR', 'size="8,5"'])
call_list = []

file_indexer = None

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
    '''
    Unfolds file by given name

    Also adds all included files as nodes to include graph. To disable this,
    set include_graph.active = False before calling
    '''
    include_graph.add_node(file_name)
    include_graph.add_to_list(file_name)

    text = open(file_name, 'r') 
    initial_dict = load(text)

    if len(include_graph.include_list) >= 2:
        include_graph.pop_from_list()
        include_graph.add_edge_from_last_node(file_name, 
                label='<<B>include</B>>', color='include_color')
    return initial_dict

def get_calls(file_name):
    '''
    Reads file by given name and returns array of tuples in form
    (job_name, job_yaml) for all calls
    '''
    
    file_dict = unfold_yaml(file_name)

    return get_calls_from_dict(file_dict[0])

def get_yaml_from_name(name):
    '''
    Finds .yaml config by given name
    Slow version that will scan all files in the directory for each call
    '''

    return file_index.get_by_name(name)

def extract_call(call):
    call = call[0]
    project = call['project']
    file_yaml = get_yaml_from_name(project)
    return (call['project'], file_yaml)

def get_calls_from_dict(file_dict):

    calls = []

    if type(file_dict) == dict:
        for key in file_dict:
            if key == 'trigger-builds':
                calls.append(extract_call(file_dict['trigger-builds']))
            else:
                calls.extend(get_calls_from_dict(file_dict[key]))
    elif type(file_dict) == list:
        for value in file_dict:
            calls.extend(get_calls_from_dict(value))

    return calls
    

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

    # FIXME: Because we run script in root project, we also need to specify directory where all
    # configs are. Do we need another command line parameter for that, or can we infer it somehow?
    file_index = FileIndex(os.getcwd() + "/maxscale_jobs", unfold_yaml)

    unfolded_yaml = unfold_yaml(args.file)
    #print(dump(unfolded_yaml, default_flow_style=False))

    print(get_calls(args.file))

    if include_graph.active: 
        export_name = basename(args.file) + '_include'
        include_graph.render(export_name)

    if call_graph_flag:
        export_name = basename(args.file) + '_call'
        call_graph.render(export_name)

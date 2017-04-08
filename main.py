#!/usr/bin/env python

import argparse
from argparse import ArgumentParser

import os
from os.path import basename

import sys

from job_visualization import YamlUnfolder
from job_visualization import Analyzer
from job_visualization import FileIndex
from job_visualization import ConfigParser
from job_visualization import synonym_parser
from job_visualization import export_shell

if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--files', nargs='+', type=str, help='List of files that graphs will be build for. Every such file will be marked red on the resulting graph')
    parser.add_argument('--include-graph', dest='include_graph', action='store_true', help='Whether to build the include graph')
    parser.add_argument('--call-graph', dest='call_graph', action='store_true', help='Whether to build the call graph')
    parser.add_argument('--yaml-root', default='', help='Root directory that is used for resolving relative includes')
    parser.add_argument('--call-display', choices=['none', 'text', 'edge'], default='text', help='How to display information about calls in call graph')
    parser.add_argument('--rank-dir', choices=['left-right', 'up-down'], default='left-right', help='How to display a graph. If left-right is selected, all edges will be drawn from left to right. If up-down is selected, all edges will be drawn from up to bottom')
    parser.add_argument('--call-parameters', nargs='+', type=str, help='Call parameters to display on call edges')
    parser.add_argument('--legend', action='store_true', dest='legend', help='Whether to draw a legend or not')
    parser.add_argument('--config', default=ConfigParser.default_config, help='Path to file used as config. Every option from config is overriden if set from command line parameters')
    parser.add_argument('--synonyms', nargs='+', type=str, help='Sets of synonyms that should be considered the same. Every synonym set should be inside curly braces {}, every synonym inside set should be separated with comma')
    parser.add_argument('--name', default=None, type=str, help='Export name. Include graphs will contain _include suffix. Call graphs will contain _call suffix. If not set, export name will be derived from the first file passed to --files')
    parser.add_argument('--analysis', nargs='+', type=str, help='Analysis functions and arguments in the format "func1;arg1=5;arg2 func2;arg1;arg2=True func3"')
    parser.add_argument('--export-shell', default=None, help="Export all shell in .yml configs to the specified directory")

    parser.set_defaults(include_graph=False, call_graph=False, draw_legend=False, call_parameters=[], synonyms=[], call_order=False, analysis=[])

    args = parser.parse_args()

    config_parser = ConfigParser(args.config)

    if args.synonyms != []:
        args.synonyms = synonym_parser.parse_from_args(args.synonyms)

    args = config_parser.merge_args(args)

    yaml_root = args.yaml_root

    yaml_unfolder = YamlUnfolder(root=yaml_root, rank_dir=args.rank_dir)

    yaml_unfolder.include_graph.active = args.include_graph
    yaml_unfolder.call_graph.active = args.call_graph

    yaml_unfolder.include_graph.draw_legend = args.legend
    yaml_unfolder.call_graph.draw_legend = args.legend

    yaml_unfolder.call_graph.call_display = args.call_display
    yaml_unfolder.call_graph.call_parameters = set(args.call_parameters)

    files = args.files
    export_name = args.name

    if yaml_unfolder.include_graph.active: 
        for name in files:
            if os.path.isdir(name):
                continue

            yaml_unfolder.unfold_yaml(name, is_root=True)
            yaml_unfolder.reset()
        
        if export_name is None:
            include_export_name = basename(files[0]) + '_include'
        else:
            include_export_name = "{}_include".format(export_name)

        yaml_unfolder.include_graph.render(include_export_name)

        print("Generated include graph at {}.svg".format(include_export_name))

    if yaml_unfolder.call_graph.active:
        if export_name is None:
            call_export_name = basename(files[0]) + '_call'
        else:
            call_export_name = "{}_call".format(export_name)


        for name in files:
            if os.path.isdir(name):
                continue

            yaml_unfolder.call_graph.unfold_file(name)

        yaml_unfolder.call_graph.render(call_export_name)

        print("Generated call graph at {}.svg".format(call_export_name))

    # Creating analyzer takes a couple of seconds for building include and call graphs of whole project
    # No need to create analyzer if there is nothing to analyze
    if len(args.analysis) > 0:
        analyzer = Analyzer(root=yaml_root, arguments=args.analysis, synonyms=args.synonyms, file_index = yaml_unfolder.file_index)
        analyzer.run()
        analyzer.print_result()

        if not analyzer.is_ok():
            sys.exit(1)

    if args.export_shell is not None:
        file_index = yaml_unfolder.file_index

        export_shell(file_index, to_dir=args.export_shell)


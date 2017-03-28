#!/usr/bin/env python

from argparse import ArgumentParser
import os
from os.path import basename

from job_visualization import YamlUnfolder
from job_visualization import FileIndex
from job_visualization import ConfigParser
from job_visualization import synonym_parser

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True, type=str)
    parser.add_argument('--include-graph', dest='include_graph', action='store_true')
    parser.add_argument('--call-graph', dest='call_graph', action='store_true')
    parser.add_argument('--yaml-root', default='')
    parser.add_argument('--call-display', choices=['none', 'text', 'edge'], default='text')
    parser.add_argument('--rank-dir', choices=['left-right', 'up-down'], default='left-right')
    parser.add_argument('--call-parameters', nargs='+', type=str)
    parser.add_argument('--legend', action='store_true', dest='legend')
    parser.add_argument('--config', default=ConfigParser.default_config)
    parser.add_argument('--synonyms', nargs='+', type=str)
    parser.add_argument('--name', default=None, type=str)

    parser.set_defaults(include_graph=False, call_graph=False, draw_legend=False, call_parameters=[], synonyms=[], call_order=False)

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

    yaml_unfolder.synonyms = args.synonyms

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

#!/usr/bin/env python

from argparse import ArgumentParser
import os
from os.path import basename

from job_visualization import YamlUnfolder
from job_visualization import FileIndex

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True, type=str)
    parser.add_argument('--include-graph', dest='include_graph', action='store_true')
    parser.add_argument('--call-graph', dest='call_graph', action='store_true')
    parser.add_argument('--yaml-root', default='')
    parser.add_argument('--call-display', choices=['none', 'text', 'edge'], default='none')

    parser.set_defaults(include_graph=False, call_graph=False)

    args = parser.parse_args()

    yaml_root = args.yaml_root

    yaml_unfolder = YamlUnfolder(root=yaml_root)

    yaml_unfolder.include_graph.active = args.include_graph
    yaml_unfolder.call_graph.active = args.call_graph

    yaml_unfolder.call_graph.call_display = args.call_display

    files = args.files
    # main_file is the one we pass to include graph
    main_file = args.files[0]

    if yaml_unfolder.include_graph.active: 
        unfolded_yaml = yaml_unfolder.unfold_yaml(main_file, is_root=True)
        export_name = basename(args.files[0]) + '_include'
        yaml_unfolder.include_graph.render(export_name)

        print("Generated include graph at {}.svg".format(export_name))

    if yaml_unfolder.call_graph.active:
        export_name = basename(main_file) + '_call'

        for file_name in files:
            yaml_unfolder.call_graph.unfold_file(file_name)

        yaml_unfolder.call_graph.render(export_name)

        print("Generated call graph at {}.svg".format(export_name))

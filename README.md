# jenkins_job_builder_visualization

![include_graph_exmaple](https://raw.githubusercontent.com/OSLL/jenkins_job_builder_visualization/master/test.yml_include.png)

## Prerequisites
### Python 2
```
sudo pip install graphviz
```
### Python 3
```
sudo pip3 install graphviz
```

If you see this error
```
GraphViz's executables not found
```
try 
```
sudo apt-get install python3-pygraphviz
```

## Usage
Script that substitute ALL includes inside yaml and creates svg graph of includes. It generates two files (<yaml_base_name>_include, <yaml_base_name>_include.svg - graph image) + outputs substituted YAML.

## Examples

../yaml-unfolding/yaml-unfolding.py --file test.yml --include-graph True 

../yaml-unfolding/yaml-unfolding.py --file maxscale_jobs/run_test.yaml --include-graph True --yaml-root /maxscale_jobs

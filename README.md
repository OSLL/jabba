# jenkins_job_builder_visualization

![include_graph_example](https://raw.githubusercontent.com/OSLL/jenkins_job_builder_visualization/master/test.yml_include.png)

## Prerequisites

```
sudo apt-get install pygraphviz
```

### Python 2
```
sudo pip install graphviz pyyaml
```
### Python 3
```
sudo pip3 install graphviz pyyaml
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

### Include graph
../yaml_unfolding/main.py --files test/test_include_graph/test_data/test.yml --yaml-root -test/test_include_graph/test_data/ -include-graph

../yaml_unfolding/main.py --files maxscale_jobs/run_test.yaml --include-graph --yaml-root maxscale_jobs/

### Call graph
../yaml_unfolding/main.py --files maxscale_jobs/build_all.yaml maxscale_jobs/run_test.yaml --call-graph --yaml-root maxscale_jobs/

## Testing

To run all test, run the following commands
```
./run_test.sh
```

To add new tests, create new config files in test_data, then add it in test_*_graph.py.
When you first run tests, missing ref files will be generated and will be used as correct ref files in the next test runs. You can check ref files in `test_refs/` folder.

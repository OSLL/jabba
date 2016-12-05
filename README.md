# jenkins_job_builder_visualization

![include_graph_exmaple](https://raw.githubusercontent.com/OSLL/jenkins_job_builder_visualization/master/test.yml_include.png)


Script that substitute ALL includes inside yaml and creates svg graph of includes. It generates two files (<yaml_base_name>_include, <yaml_base_name>_include.svg - graph image) + outputs substituted YAML.

Examples:

../yaml-unfolding/yaml-unfolding.py --file test.yml

../yaml-unfolding/yaml-unfolding.py --file maxscale_jobs/run_test.yaml

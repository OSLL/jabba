#!/bin/bash

# Generate .rst files, ingoring test folder
sphinx-apidoc -f -o docs/ job_visualization/ job_visualization/test/

cd docs
make html

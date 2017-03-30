#!/bin/bash

# Generate .rst files, ingoring test folder
sphinx-apidoc -f -o doc/ job_visualization/ job_visualization/test/

cd doc
make html

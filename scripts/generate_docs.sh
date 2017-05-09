#!/bin/bash

# Generate .rst files, ingoring test folder
sphinx-apidoc -f -o doc/ jabba/ jabba/test/

cd doc
make html

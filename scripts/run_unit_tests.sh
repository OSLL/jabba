#!/bin/bash

echo -e "\e[93mRunning unit tests\e[0m"
cd job_visualization
python -m unittest discover --verbose
cd .. 

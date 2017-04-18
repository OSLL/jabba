#!/bin/bash

echo -e "\e[93mRunning unit tests\e[0m"
cd jabba
python -m unittest discover --verbose
cd .. 

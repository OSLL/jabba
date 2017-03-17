#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

echo -e "\e[93mRunning integration tests\e[0m"

./scripts/download_maxscale_jobs.sh

cwd=$(pwd)/

exit_code=0
total_OK=0
total_ER=0

while read command
do 
    cd /tmp/maxscale-jenkins-jobs
    echo running ${command}

    if !(eval "${cwd}${command}")
    then echo error; exit_code=1; total_ER=$(($total_ER+1))
    else total_OK=$(($total_OK+1)); echo "OK"; fi

    cd $cwd
done < <(cat "integration_tests_data/test_commands.txt")

echo -e "\e[92mAll tests done\e[0m"
echo $(($total_ER + $total_OK))" tests run"
echo $total_ER" errors"

exit $exit_code

#!/bin/bash

if [ ! -e "/tmp/maxscale-jenkins-jobs" ]; then
    echo -e "\e[92mCloning to /tmp/maxscale-jenkins-jobs\e[0m"
    cwd=$(pwd)

    {
        git clone git@github.com:mariadb-corporation/maxscale-jenkins-jobs.git /tmp/maxscale-jenkins-jobs
        cd /tmp/maxscale-jenkins-jobs/
        git checkout 89af41b82fa9b678bc305bb332df5bdd7b1359f9

        cd $cwd
        cp  integration_tests_data/.jjv_config.yml /tmp/maxscale-jenkins-jobs/.jjv_config.yml 
    } &> /dev/null

    cd $cwd
fi

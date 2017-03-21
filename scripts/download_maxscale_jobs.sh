#!/bin/bash

if [ ! -e "/tmp/maxscale-jenkins-jobs" ]; then
    echo -e "\e[92mCloning to /tmp/maxscale-jenkins-jobs\e[0m"
    cwd=$(pwd)

    {
        git clone git@github.com:mariadb-corporation/maxscale-jenkins-jobs.git /tmp/maxscale-jenkins-jobs
        cd /tmp/maxscale-jenkins-jobs/
        git checkout 2d47218a68899c814d0e83c181e239ba73f3dd7d
    } &> /dev/null

    cd $cwd
fi

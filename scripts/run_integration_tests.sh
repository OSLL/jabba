echo -e "\e[93mRunning integration tests\e[0m"

./scripts/download_maxscale_jobs.sh

cwd=$(pwd)/

cat "integration_tests_data/test_commands.txt" | while read command
do 
    cd /tmp/maxscale-jenkins-jobs
    echo running ${command}
    if !(eval "${cwd}${command}"); then echo error at ${command}; exit 1; fi
    cd $cwd
done


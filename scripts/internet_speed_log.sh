#!/usr/bin/env bash

# # install speedtest
# brew tap teamookla/speedtest
# brew update
# brew install speedtest
# brew install coreutils  # for gtimeout

# #!/usr/bin/env bash
# # have this running in the background
# header='"datetime","server name","server id","latency","jitter","packet loss","download","upload","download bytes","upload bytes","share url"'
# echo $header
# echo $header > ~/Documents/internet_speed.csv
max_seconds=120
while true; do
    datetime=$(date +"%Y-%m-%d %T")
    speedtest_result=$(gtimeout ${max_seconds} speedtest -f csv)
    if [[ $? == 124 ]]; then
        echo "speedtest took > ${max_seconds} seconds, trying again"
    else
        line="${datetime},${speedtest_result}"
        # echo ${line}
        echo ${line} >> ~/Documents/internet_speed.csv
    fi
done

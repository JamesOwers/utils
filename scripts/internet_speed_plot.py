#!/usr/bin/env python
from pathlib import Path

import fire
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
# max_seconds=120
# while true; do
#     datetime=$(date +"%Y-%m-%d %T")
#     speedtest_result=$(gtimeout ${max_seconds} speedtest -f csv)
#     if [[ $? == 124 ]]; then
#         echo "speedtest took > ${max_seconds} seconds, trying again"
#     else
#         line="${datetime},${speedtest_result}"
#         echo ${line}
#         echo ${line} >> ~/Documents/internet_speed.csv
#     fi
# done


def plot_internet_speed(from_date=None, to_date=None):
    path = Path("~", "Documents", "internet_speed.csv").expanduser()
    df = pd.read_csv(path, parse_dates=True, index_col="datetime")
    df.sort_index(inplace=True)
    if from_date is not None:
        df = df.loc[from_date:]
    if to_date is not None:
        df = df.loc[:to_date]

    for colname in ["download", "upload"]:
        plt.figure(figsize=(12, 4))
        mbps_colname = f"{colname}_mbps"
        df[mbps_colname] = df[colname] * 8 / 1000 / 1000
        rolling_mean = (
            df[mbps_colname].rolling("15min").mean().rename("15min_rolling_mean")
        )
        rolling_mean.plot(
            kind="line",
            color="k",
            linestyle="--",
            zorder=100,
            linewidth=3,
        )
        _ = sns.lineplot(
            x="datetime",
            y=mbps_colname,
            hue="server name",
            data=df.reset_index(),
            estimator=None,
            marker="o",
            alpha=.75,
            ax=plt.gca(),
        )
        _, y_max = plt.ylim()
        plt.ylim([0, y_max])
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        plt.title(f"{colname} speed (mbps)")
        plt.grid()
        plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fire.Fire(plot_internet_speed)

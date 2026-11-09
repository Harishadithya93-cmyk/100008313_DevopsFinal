import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BUCKET = 5  # seconds per row

df = pd.read_csv(
    "loadtest/results/results.csv",
    usecols=["metric_name", "timestamp", "metric_value"],
)
df = df[df.metric_name.isin(["http_req_duration", "http_req_failed", "http_reqs"])]
df["t"] = ((df.timestamp - df.timestamp.min()) // BUCKET) * BUCKET

dur = df[df.metric_name == "http_req_duration"].groupby("t").metric_value
table = pd.DataFrame({
    "p50_ms": dur.quantile(0.50),
    "p95_ms": dur.quantile(0.95),
    "p99_ms": dur.quantile(0.99),
})
table["error_rate_pct"] = df[df.metric_name == "http_req_failed"].groupby("t").metric_value.mean() * 100
table["req_per_s"] = df[df.metric_name == "http_reqs"].groupby("t").metric_value.sum() / BUCKET
table = table.round(1)
table.index.name = "seconds"

print(table.to_string())
table.to_csv("loadtest/results/timeseries.csv")

fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
table[["p50_ms", "p95_ms", "p99_ms"]].plot(ax=axes[0], title="Latency percentiles (ms)")
table["error_rate_pct"].plot(ax=axes[1], title="Error rate (%)", color="red")
table["req_per_s"].plot(ax=axes[2], title="Throughput (requests/s)", color="green")
axes[2].set_xlabel("Seconds since test start")
plt.tight_layout()
plt.savefig("loadtest/results/loadtest-chart.png", dpi=150)
print("Saved loadtest/results/loadtest-chart.png")
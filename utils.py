def calculate_cpu_usage(stats: dict):
    UsageDelta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    SystemDelta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    cpuPercent = (UsageDelta / SystemDelta) * (stats["cpu_stats"]["online_cpus"]) * 100
    percent = round(cpuPercent, 2)
    return percent


def calculate_network_bytes(d):
    networks = graceful_chain_get(d, "networks")
    if not networks:
        return 0, 0
    r = 0
    t = 0
    for if_name, data in networks.items():
        r += data["rx_bytes"]
        t += data["tx_bytes"]
    return r, t


def calculate_block_bytes(d):
    block_stats = graceful_chain_get(d, "blkio_stats")
    if not block_stats:
        return 0, 0
    r = 0
    w = 0
    for _ in block_stats["io_service_bytes_recursive"]:
        if _["op"] == "read":
            r += _["value"]
        elif _["op"] == "write":
            w += _["value"]
    return r, w


def graceful_chain_get(d, *args, default=None):
    t = d
    for a in args:
        try:
            t = t[a]
        except (KeyError, ValueError, TypeError, AttributeError):
            return default
    return t


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


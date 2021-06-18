import os
import sys
import platform
import psutil
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv("PORT")

def cpu_stats():
    psutil.cpu_percent()
    sleep(0.2)
    cpu_percent = psutil.cpu_percent()
    cpu_freqs = psutil.cpu_freq(percpu=True)
    avg_current = sum(x.current / len(cpu_freqs) for x in cpu_freqs)
    s = "<b>CPU</b>\n"
    s += f"{bar(cpu_percent, len=12)}\n"
    s += f"{psutil.cpu_count()} cores - {avg_current}Hz - {cpu_percent}%\n"
    return s

def mem_stats():
    mem = psutil.virtual_memory()
    s = "<b>MEMORY</b>\n"
    s += f"{bar(mem.percent, 12)}\n"
    s += f"{hrs(mem.total)} tot - {hrs(mem.used)} used\n"
    return s

def disk_stats():
    s = "<b>DISKS</b>\n"
    if sys.platform=="win32":
        for disk in psutil.disk_partitions():
            usage = psutil.disk_usage(disk.device)
            s += f"{bar(usage.percent, 12)}\n"
            s += f"{disk.device}: {hrs(usage.total)} tot - {hrs(usage.used)} used\n"
    else:
        usage = psutil.disk_usage("/")
        s += f"{bar(usage.percent, 12)}\n"
        s += f"/: {hrs(usage.total)} tot - {hrs(usage.used)} used\n"
    return s

def sens_stats():
    s = "<b>SENSORS</b>\n"
    if sys.platform=="win32":
        s += "not available on windows\n"
    else:
        for name, entries in psutil.sensors_temperatures().items():
            s += f" {name}:\n"
            for entry in entries:
                s += f"{bar(entry.current, 12)}\n"
                s += f"{entry.current} °C, high:{entry.high!=None}, crit:{entry.critical!=None}\n"
    return s

def main():
    print(PORT)

if __name__ == "__main__":
    main()
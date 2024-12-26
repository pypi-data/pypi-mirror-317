from datetime import datetime, timedelta
import time
import sys

def beijing_to_utc_time_str(beijing_time_str: str):
    # 将字符串转换为 datetime 对象
    beijing_time = datetime.strptime(beijing_time_str, '%Y-%m-%dT%H:%M:%S')

    # 北京时间转为 UTC 时间，减去8小时
    utc_time = beijing_time - timedelta(hours=8)

    # 转换为字符串表示
    utc_time_str = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return utc_time_str

def print_percentage(current, total, start_time):
    """计算进度与时间"""
    elapsed_time = time.time() - start_time

    progress = current / total

    if current > 0:
        estimated_total_time = elapsed_time / progress
        remaining_time = estimated_total_time - elapsed_time
    else:
        estimated_total_time = 0
        remaining_time = 0

    percent = (current / total) * 100
    sys.stdout.write(f"\rProgress: {percent:.2f}% | Elapsed: {
        elapsed_time/60:.1f} min | Remaining: {remaining_time/60:.1f} min")
    # sys.stdout.flush()

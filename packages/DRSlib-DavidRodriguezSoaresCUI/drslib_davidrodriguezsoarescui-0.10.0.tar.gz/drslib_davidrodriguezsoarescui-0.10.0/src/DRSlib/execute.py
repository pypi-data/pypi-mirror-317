# pylint: disable=broad-except
"""
Shell command execution
=======================

Sometimes we just want to execute a shell command and possibly
retrieve stdout/stderr, without hassle.
"""

import collections
import multiprocessing
import subprocess  # nosec
import sys
import threading
import time
from collections import deque
from multiprocessing.managers import DictProxy
from os import PathLike
from pathlib import Path
from typing import Dict, Sequence, Union

from .os_detect import Os
from .str_utils import ensure_quoted_on_space

DETECTED_OS = Os()
OS_IS_UNIX = (
    DETECTED_OS.linux or DETECTED_OS.cygwin or DETECTED_OS.mac or DETECTED_OS.wsl
)
COMMAND_TYPE = Union[
    Union[str, bytes, PathLike[str], PathLike[bytes]],
    Sequence[Union[str, bytes, PathLike[str], PathLike[bytes]]],
]


def execute(command: COMMAND_TYPE, shell: bool = False) -> Dict[str, str]:
    """Passes command to subprocess.Popen, retrieves stdout/stderr and performs
    error management.
    Returns a dictionnary containing stdX.
    Upon command failure, prints exception and returns empty dict."""

    try:
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
        ) as process:  # nosec
            # wait and retrieve stdout/err
            _stdout, _stderr = process.communicate()
            # handle text encoding issues and return stdX
            return {
                "stdout": _stdout.decode("utf8", errors="backslashreplace"),
                "stderr": _stderr.decode("utf8", errors="backslashreplace"),
            }
    except Exception as e:
        print(f"execute: Error while executing command '{command}' : {e}")  # type: ignore[str-bytes-safe]
        raise


def __cmd_is_sequence(command: COMMAND_TYPE) -> bool:
    """Needed for differentiated command manipulation"""
    return isinstance(command, collections.abc.Sequence) and not isinstance(
        command, str
    )


def command_to_string(command: COMMAND_TYPE) -> str:
    """Returns string representation for command"""
    if __cmd_is_sequence(command):
        return " ".join(
            ensure_quoted_on_space(x)
            for x in [c if isinstance(c, str) else str(c) for c in command]  # type: ignore[union-attr]
        )
    return command if isinstance(command, str) else str(command)


# The following code was adapted from https://github.com/manzik/cmdbench


def debug_execute(commands_list: COMMAND_TYPE):
    """Execute command and get resource usage statistics"""
    time_tmp_output_file = None
    _cmd: list = (
        list(commands_list) if __cmd_is_sequence(commands_list) else [commands_list]  # type: ignore[arg-type]
    )

    if DETECTED_OS.linux:
        # Preprocessing: Wrap the target command around the GNU Time command
        time_tmp_output_file = Path("./.time.tmp")
        _cmd = [
            "/usr/bin/time",
            "-o",
            time_tmp_output_file,
            "-v",
        ] + _cmd

    # START: Initialization

    # CPU
    cpu_times, disk_io_counters = None, None

    # Time series data
    # We don't need fast read access, we need fast insertion so we use deque
    sample_milliseconds: deque[float] = deque([])
    cpu_percentages: deque[float] = deque([])
    memory_values: deque[float] = deque([])

    manager = multiprocessing.Manager()
    shared_process_dict_template = {
        "target_process_pid": -1,
        "execution_start": -1,
        "sample_milliseconds": sample_milliseconds,
        "cpu_percentages": cpu_percentages,
        "memory_values": memory_values,
        "memory_max": 0,
        "memory_perprocess_max": 0,
        "disk_io_counters": disk_io_counters,
        "cpu_times": cpu_times,
    }
    shared_process_dict = manager.dict(shared_process_dict_template)

    # Subprocess: For time series measurements

    # We need a non-blocking method to capture essential info (disk usage, cpu times)
    # and non-essential time-series info in parallel.
    # So we use either multiprocessing or threading to achieve this

    # Linux: Processes are faster than threads
    # Windows: Both are as fast but processes take longer to start
    time_series_exec: multiprocessing.Process | threading.Thread
    if DETECTED_OS.linux:
        time_series_exec = multiprocessing.Process(
            target=collect_time_series, args=(shared_process_dict,)
        )
    else:
        time_series_exec = threading.Thread(
            target=collect_time_series, args=(shared_process_dict,)
        )
    time_series_exec.start()

    # Finally, run the command
    # Master process could be GNU Time running target command or the target command itself
    master_process = psutil.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    execution_start = time.time()

    # p is always the target process to monitor
    p = get_target_process(master_process)

    shared_process_dict["execution_start"] = execution_start
    shared_process_dict["target_process_pid"] = p.pid

    # Wait for process to finish (time_series_exec and fixed_data_exec will be processing it in parallel)
    outdata, errdata = master_process.communicate()
    stdout, stderr = outdata.decode(
        sys.stdout.encoding, errors="backslashreplace"
    ), errdata.decode(sys.stderr.encoding, errors="backslashreplace")

    exection_end = time.time()

    # Done with the master process, wait for the parallel (threads or processes) to finish up
    time_series_exec.join()

    # Collect data from other (threads or processes) and store them
    cpu_times: dict | None = shared_process_dict["cpu_times"]
    disk_io_counters = shared_process_dict["disk_io_counters"]

    memory_max = shared_process_dict["memory_max"]
    memory_perprocess_max = shared_process_dict["memory_perprocess_max"]

    sample_milliseconds = shared_process_dict["sample_milliseconds"]  # type: ignore[assignment]
    cpu_percentages = shared_process_dict["cpu_percentages"]  # type: ignore[assignment]
    memory_values = shared_process_dict["memory_values"]  # type: ignore[assignment]

    # Calculate and store proper values for cpu and disk
    # https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_times
    cpu_system_time: float
    cpu_user_time: float
    if cpu_times is None:
        # macOS and Windows where cpu_times always returns 0 for children's cpu usage
        # Then we have calculated this info ourselves in other threads (collect_time_series, specifically)
        # grab and use them
        assertTrue(
            DETECTED_OS.mac or DETECTED_OS.windows, "cpu_used should not be None"
        )
        cpu_user_time = shared_process_dict["children_user_cpu_time"]  # type: ignore[assignment]
        cpu_system_time = shared_process_dict["children_system_cpu_time"]  # type: ignore[assignment]
    else:
        cpu_user_time = cpu_times.user + cpu_times.children_user  # type: ignore[assignment]
        cpu_system_time = cpu_times.system + cpu_times.children_system  # type: ignore[assignment]

    cpu_total_time = cpu_user_time + cpu_system_time

    # Convert deques to numpy arrays
    # sample_milliseconds = np.array(sample_milliseconds)
    # cpu_percentages = np.array(cpu_percentages)
    # memory_values = np.array(memory_values)

    # Collect info from GNU Time if it's linux
    gnu_times_dict = read_gnu_time(time_tmp_output_file)

    resource_usages = {
        "psutil": {  # Data collected from psutil
            "cpu": {
                "total_time_s": cpu_total_time,
                "user_time_s": cpu_user_time,
                "system_time_s": cpu_system_time,
            },
            "memory": {
                "max": memory_max,
                "max_perprocess": memory_perprocess_max,
            },
            "process": {"execution_time_s": exection_end - execution_start},
        },
        "general": {  # Info independent from GNU Time and psutil
            "command": command_to_string(_cmd),
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": gnu_times_dict["Exit status"]
            if DETECTED_OS.linux
            else master_process.returncode,
        },
    }

    add_disk_usage(disk_io_counters, resource_usages)

    add_gnu_time_usage(gnu_times_dict, resource_usages)

    return resource_usages


def get_target_process(master_process: psutil.Popen) -> psutil.Popen | psutil.Process:
    """Linux-specific; Wait for time to load the target process, then proceed"""
    if DETECTED_OS.linux:
        # Only in linux, we target command will be GNU Time's child process
        # If we are using GNU Time and are on linux:
        # Wait for time to load the target process, then proceed

        # Wait for /usr/bin/time to start the target command
        while True:
            master_process_retcode = master_process.poll()
            if master_process_retcode is not None or not master_process.is_running():
                break

        time_children = master_process.children(recursive=False)
        if len(time_children) > 0 and time_children[0] is not None:
            return time_children[0]
        raise ValueError("Failed to get timing process")
    else:
        # On other platforms, the main process will be the target process itself
        return master_process


def add_gnu_time_usage(gnu_times_dict: dict, resource_usages: dict) -> None:
    """Adds gnu tume usage statistics to resource usage dictionnary"""

    if not DETECTED_OS.linux:
        return

    resource_usages["gnu_time"] = {
        "cpu": {
            "user_time": gnu_times_dict["User time (seconds)"],
            "system_time": gnu_times_dict["System time (seconds)"],
            "total_time": gnu_times_dict["User time (seconds)"]
            + gnu_times_dict["System time (seconds)"],
        },
        "memory": {
            "max_perprocess": gnu_times_dict["Maximum resident set size (kbytes)"]
            * 1024,
        },
        "disk": {
            # https://stackoverflow.com/a/42127533
            "file_system_inputs": gnu_times_dict["File system inputs"] * 512,
            "file_system_outputs": gnu_times_dict["File system outputs"] * 512,
        },
        "process": {
            "execution_time": gnu_times_dict[
                "Elapsed (wall clock) time (h:mm:ss or m:ss)"
            ]
        },
    }
    resource_usages["gnu_time_results"] = gnu_times_dict


def add_disk_usage(disk_io_counters, resource_usages) -> None:
    """Adds disk usage statistics to resource usage dictionnary"""

    if DETECTED_OS.mac or disk_io_counters is None:
        return

    io = {
        "read_bytes": disk_io_counters.read_bytes,
        "write_bytes": disk_io_counters.write_bytes,
        "read_count": disk_io_counters.read_count,
        "write_count": disk_io_counters.write_count,
    }
    if DETECTED_OS.linux:
        io["read_chars"] = disk_io_counters.read_chars
        io["write_chars"] = disk_io_counters.write_chars
    if DETECTED_OS.windows:
        io["other_count"] = disk_io_counters.other_count
        io["other_bytes"] = disk_io_counters.other_bytes

    resource_usages["psutil"]["disk"] = {"io_counters": io}


def read_gnu_time(
    time_tmp_output_file: Path | None,
) -> Dict[str, Union[int, float, str]]:
    """Read GNU Time command's output and returns it parsed into a python dictionary"""
    if not DETECTED_OS.linux:
        return {}
    if time_tmp_output_file is None or not time_tmp_output_file.exists():
        raise ValueError(
            f"Expected file {time_tmp_output_file} is None or doesn't exist"
        )

    gnu_times_lines = [
        line.strip()
        for line in time_tmp_output_file.read_text(encoding="utf8").splitlines()
    ]
    time_tmp_output_file.unlink()
    gnu_times_dict: Dict[str, str] = {}
    for gnu_times_line in gnu_times_lines:
        tokens = list(map(lambda token: token.strip(), gnu_times_line.rsplit(": ", 1)))
        if len(tokens) < 2:
            continue
        key = tokens[0]
        value = tokens[1].replace("?", "0")
        gnu_times_dict[key] = value

    # We need a conversion for elapsed time from time format to seconds
    gnu_time_elapsed_wall_clock_key = "Elapsed (wall clock) time (h:mm:ss or m:ss)"
    gnu_times_dict[gnu_time_elapsed_wall_clock_key] = str(
        get_sec(gnu_times_dict[gnu_time_elapsed_wall_clock_key])
    )

    # Convert all gnu time output's int values to int and float values to float
    gnu_times_converted = {}
    for key, value in gnu_times_dict.items():
        gnu_times_converted[key] = cast_number(value)

    # And another conversion for cpu utilization percentage string
    gnu_time_job_cpu_percent = "Percent of CPU this job got"
    gnu_times_converted[gnu_time_job_cpu_percent] = float(
        gnu_times_converted[gnu_time_job_cpu_percent].replace("%", "")  # type: ignore[union-attr]
    )

    return gnu_times_converted


def collect_time_series(shared_process_dict: DictProxy) -> None:
    """Collects time series into dict argument"""

    while shared_process_dict["target_process_pid"] == -1:
        pass

    p = psutil.Process(shared_process_dict["target_process_pid"])
    execution_start = shared_process_dict["execution_start"]
    sample_milliseconds = shared_process_dict["sample_milliseconds"]
    cpu_percentages = shared_process_dict["cpu_percentages"]
    memory_values = shared_process_dict["memory_values"]

    memory_perprocess_max = 0
    memory_max = 0

    # Children that we are processing
    # Set for faster "in" operation
    monitoring_process_children_set = set()
    # List for actual process access
    monitoring_process_children: list[psutil.Process] = []

    # If we were able to access the process info at least once without access denied error
    had_permission = False

    # For macOS and Windows. Will be used for final user and system cpu time calculation
    children_cpu_times: list[tuple[int, int, int, int]] = []

    while True:
        # retcode would be None while subprocess is running
        if not p.is_running():
            break

        try:
            time_from_monitoring_start = time.time() - execution_start

            cpu_percentage = p.cpu_percent()

            # http://grodola.blogspot.com/2016/02/psutil-4-real-process-memory-and-environ.html
            memory_usage_info = p.memory_info()
            memory_usage = memory_usage_info.rss
            memory_perprocess_max = max(memory_perprocess_max, memory_usage)

            current_children = p.children(recursive=True)
            for child in current_children:
                with child.oneshot():
                    child_memory_usage_info = child.memory_info()
                    child_memory_usage = child_memory_usage_info.rss

                    memory_usage += child_memory_usage

                    memory_perprocess_max = max(
                        memory_perprocess_max, child_memory_usage
                    )
                    # We need to get cpu_percentage() only for children existing for at list one iteration
                    # Calculate CPU usage for children we have been monitoring
                if child in monitoring_process_children_set:
                    child_index = monitoring_process_children.index(child)
                    target_child_process = monitoring_process_children[child_index]
                    if (
                        not DETECTED_OS.linux
                    ):  # psutil calculates children usage for us on linux. Otherwise we save the values ourselved
                        children_cpu_times[
                            child_index
                        ] = target_child_process.cpu_times()  # type: ignore[assignment]
                    child_cpu_usage = target_child_process.cpu_percent()
                    cpu_percentage += child_cpu_usage
                # Add children not already in our monitoring_process_children
                else:
                    monitoring_process_children_set.add(child)
                    monitoring_process_children.append(child)
                    children_cpu_times.append(
                        (0, 0, 0, 0)
                    )  # Placeholder; almost the same shape as psutil.pcputimes

            memory_max = max(memory_max, memory_usage)

            sample_milliseconds.append(time_from_monitoring_start)
            cpu_percentages.append(cpu_percentage)
            memory_values.append(memory_usage)

            had_permission = True

        except psutil.AccessDenied as access_denied_error:
            # Same reasoning as usage in the collect_fixed_data function
            if OS_IS_UNIX:
                if had_permission:
                    continue

            print("Root access is needed for monitoring the target command.")
            raise access_denied_error
        except psutil.NoSuchProcess:
            # The process might end while we are measuring resources
            pass
        except Exception as e:
            raise e

    # psutil calculates children usage for us on linux. Otherwise we calculate and pass it to the main thread.
    if not DETECTED_OS.linux:
        children_user_cpu_time = 0
        children_system_cpu_time = 0

        for cpu_time in children_cpu_times:
            children_user_cpu_time += cpu_time[0]
            children_system_cpu_time += cpu_time[1]

        shared_process_dict["children_user_cpu_time"] = children_user_cpu_time
        shared_process_dict["children_system_cpu_time"] = children_system_cpu_time

    shared_process_dict["memory_max"] = memory_max
    shared_process_dict["memory_perprocess_max"] = memory_perprocess_max

    shared_process_dict["sample_milliseconds"] = sample_milliseconds
    shared_process_dict["cpu_percentages"] = cpu_percentages
    shared_process_dict["memory_values"] = memory_values


def get_sec(time_str):
    """Conversion of time format (hh:mm:ss or mm:ss) to seconds"""
    secs = 0
    time_decimal = 0
    time_decimal_start_ind = -1
    if "." in time_str:
        time_decimal_start_ind = time_str.index(".")
    if time_decimal_start_ind > -1:
        time_decimal = float("0" + time_str[time_decimal_start_ind:])
    time_str = time_str[:time_decimal_start_ind]

    time_tokens = time_str.split(":")
    time_tokens.reverse()
    for token_ind, time_token in enumerate(time_tokens):
        secs += int(time_token) * 60**token_ind
    return secs + time_decimal

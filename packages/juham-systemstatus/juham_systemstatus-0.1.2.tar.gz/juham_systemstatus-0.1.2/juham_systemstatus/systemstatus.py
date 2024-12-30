from datetime import datetime, timedelta, timezone
import json
import psutil
import threading
from typing import Any, Optional, cast
from typing_extensions import override
from masterpiece.mqtt import MqttMsg, Mqtt
from masterpiece import MasterPieceThread
from juham.core import RThread
from juham.core.time import timestamp, epoc2utc


class SystemStatusThread(MasterPieceThread):
    """Asynchronous thread for acquiring system info. Currently fetches
    memory usage, disk usage, for each partition and CPU utilization, all in percentages.
    """

    # class attributes
    _systemstatus_topic: str = ""
    _interval: float = 60  # seconds
    _location = "unknown"

    def __init__(self, client: Optional[Mqtt] = None):
        """Construct with the given mqtt client. Acquires system metrics
        e.g. CPU load and space left on the device and publishes the data to
        systemstatus_topic.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client: Optional[Mqtt] = client

    def init(self, topic: str, interval: float, location: str) -> None:
        """Initialize the  data acquisition thread

        Args:
            topic (str): mqtt topic to publish the acquired system info
            interval (float): update interval in seconds
            location (str): geographic location
        """
        self._systemstatus_topic = topic
        self._interval = interval
        self._location = location

    def get_thread_counts(self) -> dict[str, int]:
        """Fetch the number of total, active and idle threads in the current process.

        Returns:
            Thread info (dict[str, int])
        """
        all_threads = threading.enumerate()
        total_threads = len(all_threads)
        active_threads = sum(1 for thread in all_threads if thread.is_alive())

        return {
            "total_threads": total_threads,
            "active_threads": active_threads,
            "idle_threads": total_threads - active_threads,
        }

    def get_system_info(self) -> dict[str, dict]:
        """Fetch system info e.g. CPU loads, thread count, disk and ram usage.

        Returns:
            Thread info (dict[str, dict])
        """
        cpus = psutil.cpu_percent(interval=1, percpu=True)  # List of CPU loads per core

        cpu_loads: dict[str, float] = {}
        i: int = 0
        for cpu in cpus:
            cpu_loads[f"cpu{i}"] = cpu
            i = i + i

        # Memory info
        memory = psutil.virtual_memory()  # Virtual memory details
        available_memory = memory.available  # Available memory in bytes
        total_memory = memory.total  # Total memory in bytes

        # Disk space info per partition
        partitions = psutil.disk_partitions()
        disk_info = {}
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "total": usage.total,
                    "free": usage.free,
                    "used": usage.used,
                    "percent": usage.percent,
                }
            except PermissionError:
                # Skip partitions that we don't have permission to access
                continue

        return {
            "cpu_loads": cpu_loads,
            "memory": {
                "avail_memory": available_memory,
                "total_memory": total_memory,
                "memory_usage": available_memory / total_memory * 100.0,
            },
            "disk_info": disk_info,
        }

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def update(self) -> bool:
        sysinfo: dict[str, dict] = self.get_system_info()
        sysinfo.update({"threads": self.get_thread_counts()})
        msg = json.dumps(sysinfo)
        self.publish(self._systemstatus_topic, msg, qos=1, retain=False)
        # self.debug(f"System status  published to {self._systemstatus_topic}")
        return True


class SystemStatus(RThread):
    """Constructs a data acquisition thread for reading system status
    info, e.g. available disk space and publishes the data to the systemstatus topic.

    """

    _SYSTEMSTATUS: str = "systemstatus"

    workerThreadId: str = SystemStatusThread.get_class_id()
    update_interval: float = 60
    topic = "system"
    location = "home"

    def __init__(self, name="systemstatus") -> None:
        """Constructs system status automation object for acquiring and publishing
        system info e.g. available memory and CPU loads.

        Args:
            name (str, optional): name of the object.
        """
        super().__init__(name)
        self.worker: Optional[SystemStatusThread] = None
        self.systemstatus_topic: str = self.make_topic_name(self.topic)
        self.debug(f"System status with name {name} created")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.systemstatus_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.systemstatus_topic:
            em = json.loads(msg.payload.decode())
            self.record(timestamp(), em)
        else:
            super().on_message(client, userdata, msg)

    def record(self, ts: float, info: dict[str, Any]) -> None:
        """Writes system info to the time series database

        Args:
            ts (float): utc time
            em (dict): energy meter message
        """

        cpu_loads: dict[str, float] = info["cpu_loads"]
        disk_info: dict[str, float] = info["disk_info"]
        memory: dict[str, int] = info["memory"]
        threads: dict[str, int] = info["threads"]

        try:
            self.write_point(
                "systemstatus",
                {"location": self.location, "category": "threads"},
                threads,
                epoc2utc(ts),
            )
        except Exception as e:
            self.error(f"Writing memory to influx failed {str(e)}")

        try:
            self.write_point(
                "systemstatus",
                {"location": self.location, "category": "memory"},
                memory,
                epoc2utc(ts),
            )
        except Exception as e:
            self.error(f"Writing memory to influx failed {str(e)}")

        try:
            self.write_point(
                "systemstatus",
                {"location": self.location, "category": "cpu"},
                cpu_loads,
                epoc2utc(ts),
            )
        except Exception as e:
            self.error(f"Writing cpu_loads to influx failed {str(e)}")

        try:
            value: Any
            for attr, value in disk_info.items():
                self.write_point(
                    "systemstatus",
                    {"location": self.location, "category": "disk"},
                    {"mountpoint": value["mountpoint"], "percent": value["percent"]},
                    epoc2utc(ts),
                )
        except Exception as e:
            self.error(f"Writing disk_info to influx failed {str(e)}")

    @override
    def run(self) -> None:
        # create, initialize and start the asynchronous thread for acquiring forecast

        self.worker = cast(
            SystemStatusThread, self.instantiate(SystemStatus.workerThreadId)
        )
        self.worker.init(
            self.systemstatus_topic,
            self.update_interval,
            self.location,
        )
        super().run()

    @override
    def to_dict(self) -> dict:
        data = super().to_dict()
        data[self._SYSTEMSTATUS] = {
            "topic": self.systemstatus_topic,
            "interval": self.update_interval,
        }
        return data

    @override
    def from_dict(self, data) -> None:
        super().from_dict(data)
        if self._SYSTEMSTATUS in data:
            for key, value in data[self._SYSTEMSTATUS].items():
                setattr(self, key, value)

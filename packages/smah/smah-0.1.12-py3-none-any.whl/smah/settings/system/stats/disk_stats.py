from .base_stats import BaseStats
import textwrap
import psutil
import datetime

class DiskStats(BaseStats):
    """
    Represents disk statistics.

    Attributes:
        time_stamp (datetime): The timestamp of the last update.
        total (float): The last recorded total disk space.
        available (float): The last recorded available disk space.
        used (float): The last recorded used disk space.
        percent (float): The last recorded disk usage percentage.
    """

    @staticmethod
    def disk_info(reading):
        """
        Retrieves disk information based on the specified reading type.

        Args:
            reading (str): The type of disk information to retrieve.

        Returns:
            float: The requested disk information.
        """

        try:
            if reading == "total":
                return round(psutil.disk_usage('/').total / (1024.0 ** 3), 2)
            elif reading == "free":
                return round(psutil.disk_usage('/').free / (1024.0 ** 3), 2)
            elif reading == "used":
                return round(psutil.disk_usage('/').used / (1024.0 ** 3), 2)
            elif reading == "percent":
                return round(psutil.disk_usage('/').percent, 2)
        except Exception as e:
            return None

    def __init__(self):
        """
        Initializes the DiskStats instance.
        """
        super().__init__()

        self.total = None
        self.free = None
        self.used = None
        self.percent = None

    def update(self):
        """
        Updates the disk statistics.
        """

        self.time_stamp = datetime.datetime.now()
        self.total = self.disk_info("total")
        self.free = self.disk_info("free")
        self.used = self.disk_info("used")
        self.percent = self.disk_info("percent")

    def readings(self, threshold=100):
        """
        Retrieves the current disk readings, updating if necessary.

        Args:
            threshold (int): The threshold in microseconds.

        Returns:
            dict: The current disk readings.
        """

        if self.stale(threshold):
            self.update()
        return {
            "time": self.time_stamp,
            "total": self.total,
            "free": self.free,
            "used": self.used,
            "percent": self.percent
        }

    def show(self, options=None):
        if self.stale():
            self.update()
        template = textwrap.dedent(
            """
            - time: {time}
            - total: {total}
            - free: {free}
            - used: {used}
            - percent: {percent}
            """
        ).strip().format(
            time=self.time_stamp,
            count=self.total,
            free=self.free,
            used=self.used,
            percent=self.percent
        )
        return template
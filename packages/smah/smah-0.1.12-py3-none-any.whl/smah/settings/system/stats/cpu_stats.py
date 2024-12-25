from .base_stats import BaseStats
import textwrap
import psutil
import datetime

class CpuStats(BaseStats):
    """
    Represents CPU statistics.

    Attributes:
        time_stamp (datetime): The timestamp of the last update.
        cpu_count (int): The last recorded CPU count.
        cpu_freq (float): The last recorded CPU frequency.
        cpu_percent (float): The last recorded CPU usage percentage.
    """

    @staticmethod
    def cpu_info(reading):
        """
        Retrieves CPU information based on the specified reading type.

        Args:
            reading (str): The type of CPU information to retrieve.

        Returns:
            int or float: The requested CPU information.
        """
        try:
            if reading == "count":
                return psutil.cpu_count(logical=True)
            elif reading == "freq.current":
                return round(psutil.cpu_freq().current, 2)
            elif reading == "percent":
                return round(psutil.cpu_percent(), 2)
        except:
            return None

    def __init__(self):
        """
        Initializes the CpuStats instance.
        """
        super().__init__()
        self.cpu_count = None
        self.cpu_freq = None
        self.cpu_percent = None

    def update(self):
        """
        Updates the CPU statistics.
        """
        self.time_stamp = datetime.datetime.now()
        self.cpu_count = self.cpu_info("count")
        self.cpu_freq = self.cpu_info("freq.current")
        self.cpu_percent = self.cpu_info("percent")

    def readings(self, threshold=100):
        """
        Retrieves the current CPU readings, updating if necessary.

        Args:
            threshold (int): The threshold in microseconds.

        Returns:
            dict: The current CPU readings.
        """
        if self.stale(threshold):
            self.update()
        return {
            "time": self.time_stamp,
            "cpu_count": self.cpu_count,
            "cpu_freq": self.cpu_freq,
            "cpu_percent": self.cpu_percent
        }

    def show(self, options = None):
        if self.stale():
            self.update()
        template = textwrap.dedent(
            """
            - time: {time}
            - count: {count}
            - freq: {freq}
            - percent: {percent}
            """
        ).format(
            time=self.time_stamp,
            count=self.cpu_count,
            freq=self.cpu_freq,
            percent=self.cpu_percent
        )

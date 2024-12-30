from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMBoolParameter
from WITecSDK.Modules.SlowTimeSeriesBase import SlowTimeSeriesBase, SlowTimeSeriesAdd52

class SlowTimeSeriesTimed(SlowTimeSeriesBase):
    """Class for a timed Slow Time Series"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._intervalCOM: COMFloatParameter = aGetParameter(self._parampath + "MeasurementInterval")
        self._timingModeCOM: COMBoolParameter = aGetParameter(self._parampath + "TimingMode")
        
    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float, interval: float):
        """Initializes a timed Slow Time Series with the necessary acquisition parameters.
        (If not used the setMeasurementModeToTimed method should be used.)"""
        super().Initialize(numberOfMeasurements, numberOfAccumulations, integrationTime)
        self.Interval = interval
        self.setMeasurementModeToTimed()

    @property
    def Interval(self) -> float:
        """Defines the Interval between the acquisitions in seconds"""
        return self._intervalCOM.Value
    
    @Interval.setter
    def Interval(self, interval: float):
        self._intervalCOM.Value = interval

    def setMeasurementModeToTimed(self):
        """Sets the measurement mode to Timed"""
        self._measurementModeCOM.Value = 1

    @property
    def TimingModeStartStart(self) -> bool:
        """Defines that timing mode is Start-Start. If False it will be Stop-Start"""
        return self._timingModeCOM.Value
    
    @TimingModeStartStart.setter
    def TimingModeStartStart(self, value: bool):
        self._timingModeCOM.Value = value


class SlowTimeSeriesTimed52(SlowTimeSeriesTimed, SlowTimeSeriesAdd52):
    """Extension of the SlowTimeSeriesTimed class for version 5.2 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self.__init52__(aGetParameter)
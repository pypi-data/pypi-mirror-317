from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter
from WITecSDK.Modules.SlowTimeSeriesBase import SlowTimeSeriesBase, SlowTimeSeriesAdd52
from WITecSDK.Modules.ActiveSequencer import ActiveSequencer
from asyncio import sleep

class SlowTimeSeriesManual(SlowTimeSeriesBase):
    """Class for a manually triggerd Slow Time Series"""

    def __init__(self, aGetParameter: Callable, aActiveSequencer: ActiveSequencer):
        super().__init__(aGetParameter)
        self.activeSequencer = aActiveSequencer
        self._nextMeasurementCOM: COMTriggerParameter = aGetParameter(self._parampath + "NextMeasurement")
        self._startSubSequenceCOM: COMTriggerParameter = aGetParameter(self._parampath + "SubSequence|StartSubSequence")
    
    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float):
        """Initializes a manually triggerd Slow Time Series with the necessary acquisition parameters.
        (If not used the setMeasurementModeToManual method should be used.)"""
        super().Initialize(numberOfMeasurements, numberOfAccumulations, integrationTime)
        self.setMeasurementModeToManual()

    def setMeasurementModeToManual(self):
        """Sets the measurement mode to manually triggered"""
        self._measurementModeCOM.Value = 0

    async def PerformNextMeasurement(self):
        """Coroutine that triggers the next acquisisition and waits until it finishes"""
        await self.waitForNextMeasurement()    
        self._nextMeasurementCOM.ExecuteTrigger()
        await self.waitForMeasurementStarted()
        await self.waitForNextMeasurement()

    async def PerformAutofocus(self):
        """Coroutine that triggers the spectral Autofocus and waits until it finishes"""
        await self.waitForNextMeasurement()
        self._startSubSequenceCOM.ExecuteTrigger()
        await self.waitForMeasurementStarted()
        await self.waitForNextMeasurement()

    async def waitForNextMeasurement(self):
        """Coroutine that waits until the current aquisition is finished"""
        while True:
            await sleep(0.2)
            currentActivity = self.activeSequencer.CurrentActivity
            if currentActivity == "Waiting for next Measurement":
                break
            elif currentActivity is None:
                break

    async def waitForMeasurementStarted(self):
        """Coroutine that waits until a measurement is running"""
        while True:
            await sleep(0.1)
            currentActivity = self.activeSequencer.CurrentActivity
            if currentActivity != "Waiting for next Measurement":
                break


class SlowTimeSeriesManual52(SlowTimeSeriesManual, SlowTimeSeriesAdd52):
    """Extension of the SlowTimeSeriesTimed class for version 5.2 and higher"""

    def __init__(self, aGetParameter: Callable, aActiveSequencer: ActiveSequencer):
        super().__init__(aGetParameter, aActiveSequencer)
        self.__init52__(aGetParameter)
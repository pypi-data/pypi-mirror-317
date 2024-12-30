"""Module containing the class for the Scan table (piezo stage)"""

from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMTriggerParameter, COMFloatStatusParameter
from WITecSDK.Modules.HelperStructs import XYPosition, XYZPosition, userparam, datachannelpath
from asyncio import sleep

parampath = userparam + "ScanTable|"

class ScanTable:
    """Implements the Scan table (piezo stage)"""

    def __init__(self, aGetParameter: Callable):
        self._positionXCOM: COMFloatParameter = aGetParameter(parampath + "PositionX")
        self._positionYCOM: COMFloatParameter = aGetParameter(parampath + "PositionY")
        self._positionZCOM: COMFloatParameter = aGetParameter(parampath + "PositionZ")
        self._moveToCenterCOM: COMTriggerParameter = aGetParameter(parampath + "MoveToCenter")
        self._xSensorCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "XSensor")
        self._ySensorCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "YSensor")
        self._zSensorCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "ZSensor")

    @property
    def PositionX(self) -> float:
        """Defines the piezo stage x coordinate"""
        return self._positionXCOM.Value
    
    @PositionX.setter
    def PositionX(self, posX: float):
        self._positionXCOM.Value = posX

    @property
    def PositionY(self) -> float:
        """Defines the piezo stage y coordinate"""
        return self._positionYCOM.Value
    
    @PositionY.setter
    def PositionY(self, posY: float):
        self._positionYCOM.Value = posY

    @property
    def PositionZ(self) -> float:
        """Defines the piezo stage z coordinate"""
        return self._positionZCOM.Value
    
    @PositionZ.setter
    def PositionZ(self, posZ: float):
        self._positionZCOM.Value = posZ

    def MoveToCenter(self):
        """Moves piezo stage to center position"""
        self._moveToCenterCOM.ExecuteTrigger()

    @property
    def CurrentPosition(self) -> XYZPosition:
        """Retrieves the current X, Y and Z sensor values"""
        return XYZPosition(self._xSensorCOM.Value, self._ySensorCOM.Value, self._zSensorCOM.Value)
    
    @property
    def PositionReached(self) -> bool:
        """Returns True if the sensor values are within a overall distance of 200 nm from the requested position"""
        return abs(XYZPosition(self.PositionX, self.PositionY, self.PositionZ) - self.CurrentPosition) <= 0.2
    
    async def AwaitMoveToPosition(self, xyz: XYZPosition):
        """Coroutine to move the stage to a given XYZ position and waits for its arrival"""
        self.PositionX = xyz.X
        self.PositionY = xyz.Y
        self.PositionZ = xyz.Z
        
        await self.waitForMovingFinished(xyz)

    async def AwaitMoveToPositionXY(self, xy: XYPosition):
        """Coroutine to move the stage to a given XY position and waits for its arrival"""
        xyz = XYZPosition(xy.X, xy.Y, self.PositionZ)
        await self.AwaitMoveToPosition(xyz)

    async def waitForMovingFinished(self, xyz: XYZPosition):
        """Coroutine that waits until the stage arrives or 5 seconds passed"""
        counter: int = 0
        while not self.PositionReached or counter < 50:
            counter =+ 1
            await sleep(0.1)

        if not self.PositionReached:
            raise ScanTablePositionNotReachedException(xyz)

class ScanTablePositionNotReachedException(Exception):
    def __init__(self, xyz: XYZPosition):
        super().__init__("Requested Position " + str(xyz) + " not reached.")
"""Module containing the classes for the XYAxes and SamplePositioner"""

from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMBoolParameter, COMFloatParameter, COMTriggerParameter, COMFloatStatusParameter
from WITecSDK.Modules.HelperStructs import XYPosition, userparam, microscopecontrol
from asyncio import sleep
from time import sleep as tsleep

parampath = microscopecontrol + "MotorizedXYZ|XYAxes|"
parampathsp = userparam + "SamplePositioning|"
statuspath = "Status|Software|SamplePositioner|"

class XYAxesBase:
    """Base class for XYAxes and SamplePositioner"""
    
    backlash = XYPosition(30,-30)
    _DesiredSamplePosXCOM: COMFloatParameter = None
    _DesiredSamplePosYCOM: COMFloatParameter = None
    _CurrentSamplePosXCOM: COMFloatParameter|COMFloatStatusParameter = None
    _CurrentSamplePosYCOM: COMFloatParameter|COMFloatStatusParameter = None
    _StopCOM: COMTriggerParameter = None
    _MoveToDesiredSamplePosCOM: COMTriggerParameter = None
    _zeroSamplePosCOM: COMTriggerParameter = None
    _MoveToCalibrationPosCOM: COMTriggerParameter = None
    _ResetCoordinateSysCOM: COMTriggerParameter = None

    @property
    def DesiredSoftwarePos(self) -> XYPosition:
        """Defines the coordinates of the desired positiion"""
        return XYPosition(self._DesiredSamplePosXCOM.Value, self._DesiredSamplePosYCOM.Value)

    @DesiredSoftwarePos.setter
    def DesiredSoftwarePos(self, xy: XYPosition):
        self._DesiredSamplePosXCOM.Value = xy.X
        self._DesiredSamplePosYCOM.Value = xy.Y

    @property
    def CurrentSoftwarePos(self) -> XYPosition:
        """Retrieves the current position"""
        return XYPosition(self._CurrentSamplePosXCOM.Value, self._CurrentSamplePosYCOM.Value)
    
    @property
    def IsNotMoving(self) -> bool:
        """Returns true of the stage is not moving"""
        currentpos = self.CurrentSoftwarePos
        tsleep(0.1)
        return currentpos == self.CurrentSoftwarePos

    def Stop(self):
        """Stops the stage movement"""
        self._StopCOM.ExecuteTrigger()

    def MoveToDesiredSoftwarePos(self):
        """Triggers the move to the desired position"""
        self._MoveToDesiredSamplePosCOM.ExecuteTrigger()

    def ZeroSoftwarePos(self):
        """Sets the current position as zero"""
        self._zeroSamplePosCOM.ExecuteTrigger()
        tsleep(0.1)
        if self.CurrentSoftwarePos != XYPosition():
            raise XYAxesZeroNoSuccessException()
        
    def MoveToCalibrationPosition(self):
        """Moves the stage to the calibration position and adopts the coordinate system"""
        self._MoveToCalibrationPosCOM.ExecuteTrigger()

    def ResetCoordinateSystem(self):
        """Resets the coordinate system to the state of the last calibration or software start"""
        self._ResetCoordinateSysCOM.ExecuteTrigger()

    async def AwaitMoveToSoftwarePos(self, xy: XYPosition):
        """Coroutine to move the stage to a given XY position and waits for its arrival"""
        self.DesiredSoftwarePos = xy
        self.MoveToDesiredSoftwarePos()
        await self.waitForMovingFinished(xy)

    async def AwaitMoveToSoftwarePosBacklashComp(self, xy: XYPosition):
        """Coroutine to move the stage to a given XY position including backlash correction and waits for its arrival"""
        await self.AwaitMoveToSoftwarePos(xy - self.backlash)
        await self.AwaitMoveToSoftwarePos(xy)

    async def AwaitNotMoving(self):
        """Coroutine that waits until the stage is no longer moving"""
        while not self.IsNotMoving:
            await sleep(0.1)
        

class SamplePositionerBase(XYAxesBase):
    """Base class for the SamplePositioner"""
        
    def __init__(self, aGetParameter: Callable):
        self._DesiredSamplePosXCOM: COMFloatParameter = aGetParameter(parampathsp + "AbsolutePositionX")
        self._DesiredSamplePosYCOM: COMFloatParameter = aGetParameter(parampathsp + "AbsolutePositionY")
        self._zeroSamplePosCOM: COMTriggerParameter = aGetParameter(parampathsp + "SetZeroXY")
        self._MoveToCalibrationPosCOM: COMTriggerParameter = aGetParameter(parampathsp + "CalibrationPosition")
        self._ResetCoordinateSysCOM: COMTriggerParameter = aGetParameter(parampathsp + "ResetCoordinateSystem")
        self._StopCOM: COMTriggerParameter = aGetParameter(parampathsp + "StopDriving")
        self._CurrentSamplePosXCOM: COMFloatStatusParameter = aGetParameter(statuspath + "CurrentPositionX")
        self._CurrentSamplePosYCOM: COMFloatStatusParameter = aGetParameter(statuspath + "CurrentPositionY")
    
    @property
    def CurrentPosition(self) -> XYPosition:
        """For compatibility: Defines the coordinates of the desired positiion"""
        return self.CurrentSoftwarePos
    
    async def MoveTo(self, x: float, y: float):
        """For compatibility: """
        await self.AwaitMoveToSoftwarePos(XYPosition(x, y))

    def MoveToDesiredSoftwarePos(self):
        """Triggers the move to the desired position"""
        self.verifyNotInUse()
        super().MoveToDesiredSoftwarePos()

    def verifyNotInUse(self):
        """Returns True if the stage is not moving (parameters are enabled)"""
        if not self.MovingEnabled:
            raise XYAxesInUseException()

    async def waitForMovingFinished(self, xy: XYPosition = XYPosition()):
        """Coroutine that waits until the stage is not moving anymore"""
        while not self.MovingEnabled:
            await sleep(0.1)

        if xy != self.DesiredSoftwarePos:
            raise XYAxesPositionNotReachedException(xy)
    
    @property
    def MovingEnabled(self) -> bool:
        """Returns True if the stage parameters are enabled"""
        return self._MoveToDesiredSamplePosCOM.Enabled


class SamplePositioner(SamplePositionerBase):
    """Implements the SamplePostioner for older versions"""
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._MoveToDesiredSamplePosCOM: COMTriggerParameter = aGetParameter(parampathsp + "GoToPosition")


class SamplePositioner51(SamplePositionerBase):
    """Implements the SamplePostioner for version 5.1 and higher"""
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._MoveToDesiredSamplePosCOM: COMTriggerParameter = aGetParameter(parampathsp + "GoToPositionWithoutQuery")


class XYAxes(XYAxesBase):
    """Implements the XYAxes using parameters under MultiComm for version 6.1 and higher"""

    def __init__(self, aGetParameter: Callable):
        self._StateCOM: COMStringParameter = aGetParameter(parampath + "State")
        self._MoveAcceleratedCOM: COMBoolParameter = aGetParameter(parampath + "MoveAcceleratedWithMaxSpeed")
        self._MinSpeedCOM: COMFloatParameter = aGetParameter(parampath + "MinSpeed")
        self._MaxSpeedCOM: COMFloatParameter = aGetParameter(parampath + "MaxSpeed")
        self._MinSpeedLimitCOM: COMFloatParameter = aGetParameter(parampath + "MinSpeedLimit")
        self._MaxSpeedLimitCOM: COMFloatParameter = aGetParameter(parampath + "MaxSpeedLimit")
        self._SpeedLimitCOM: COMFloatParameter = aGetParameter(parampath + "SpeedLimit")
        self._UseSpeedLimitCOM: COMBoolParameter = aGetParameter(parampath + "UseSpeedLimit")
        self._SpeedCOM: COMFloatParameter = aGetParameter(parampath + "Speed")
        self._DesiredSamplePosXCOM: COMFloatParameter = aGetParameter(parampath + "DesiredSamplePositionX")
        self._DesiredSamplePosYCOM: COMFloatParameter = aGetParameter(parampath + "DesiredSamplePositionY")
        self._CurrentSamplePosXCOM: COMFloatParameter = aGetParameter(parampath + "CurrentSamplePositionX")
        self._CurrentSamplePosYCOM: COMFloatParameter = aGetParameter(parampath + "CurrentSamplePositionY")
        self._StopCOM: COMTriggerParameter = aGetParameter(parampath + "Stop")
        self._MoveToDesiredSamplePosCOM: COMTriggerParameter = aGetParameter(parampath + "MoveToDesiredSamplePosition")
        self._zeroSamplePosCOM: COMTriggerParameter = aGetParameter(parampath + "SetSamplePositionToZero")
        self._MoveToCalibrationPosCOM: COMTriggerParameter = aGetParameter(parampath + "MoveToCalibrationPosition")
        self._ResetCoordinateSysCOM: COMTriggerParameter = aGetParameter(parampath + "ResetCoordinateSystem")

    @property
    def State(self) -> str:
        """Returns the current stage state"""
        return self._StateCOM.Value

    @property
    def IsMoveAccelerated(self) -> bool:
        """Defines whether acceleration is used"""
        return self._MoveAcceleratedCOM.Value

    @IsMoveAccelerated.setter
    def IsMoveAccelerated(self, value: bool):
        self._MoveAcceleratedCOM.Value = value

    @property
    def MinSpeed(self) -> float:
        """Retrieves the minium stage speed (µm/s)"""
        return self._MinSpeedCOM.Value

    @property
    def MaxSpeed(self) -> float:
        """Retrieves the maximum stage speed (µm/s)"""
        return self._MaxSpeedCOM.Value
    
    @property
    def MinSpeedLimit(self) -> float:
        """Retrieves the minium stage speed (µm/s) for the speed limit"""
        return self._MinSpeedLimitCOM.Value

    @property
    def MaxSpeedLimit(self) -> float:
        """Retrieves the maximum stage speed (µm/s) for the speed limit"""
        return self._MaxSpeedLimitCOM.Value

    @property
    def UseSpeedLimit(self) -> bool:
        """Defines if the speed limit is in use"""
        return self._UseSpeedLimitCOM.Value

    @UseSpeedLimit.setter
    def UseSpeedLimit(self, value: bool):
        self._UseSpeedLimitCOM.Value = value

    @property
    def SpeedLimit(self) -> float:
        """Defines the speed limit in µm/s"""
        return self._SpeedLimitCOM.Value

    @SpeedLimit.setter
    def SpeedLimit(self, value: float):
        self._SpeedLimitCOM.Value = value

    @property
    def Speed(self) -> float:
        """Defines the speed of the stage movement in µm/s"""
        return self._SpeedCOM.Value

    @Speed.setter
    def Speed(self, value: float):
        self._SpeedCOM.Value = value

    def MoveToDesiredSoftwarePos(self):
        """Triggers the move to the desired position"""
        super().MoveToDesiredSoftwarePos()
        self.verifyNotInUse()

    def verifyNotInUse(self):
        """Returns True if the stage is not moving (stage state)"""
        if self.State ==  "Axis In Use":
            raise XYAxesInUseException()

    async def waitForMovingFinished(self, xy: XYPosition = XYPosition()):
        """Coroutine that waits until the stage is not moving anymore"""
        while True:
            xyState = self.State

            if xyState == "Desired Position Reached":
                break
            elif xyState == "":
                break
            elif xyState == "Manually Stopped":
                break
            elif xyState == "Position not Reached":
                raise XYAxesPositionNotReachedException(xy)

            await sleep(0.1)
        

class XYAxesPositionNotReachedException(Exception):
    def __init__(self, xy: XYPosition):
        super().__init__("Requested Position " + str(xy) + " not reached.")

class XYAxesInUseException(Exception):
    def __init__(self):
        super().__init__("XY axes already in use.")

class XYAxesZeroNoSuccessException(Exception):
    def __init__(self):
        super().__init__("XY axes could not be set to zero.")
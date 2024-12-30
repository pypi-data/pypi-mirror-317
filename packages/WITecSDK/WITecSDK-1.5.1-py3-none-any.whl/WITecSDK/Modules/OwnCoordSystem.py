from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMBoolParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import XYPosition, userparam
from asyncio import sleep

parampath = userparam + "SequencerRasterSample|"
parampathown = parampath + "OwnCoordinateSystem|"

class OwnCoordSystem:
        
    def __init__(self, aGetParameter: Callable):
        self._useOwnCoodSysCOM: COMBoolParameter = aGetParameter(parampath + "UseOwnCoordinateSystem")
        self._ownPositionXCOM: COMFloatParameter = aGetParameter(parampathown + "OwnPositionX")
        self._ownPositionYCOM: COMFloatParameter = aGetParameter(parampathown + "OwnPositionY")
        self._goToPositionCOM: COMTriggerParameter = aGetParameter(parampathown + "GoToPosition")

    def MoveTo(self, xy: XYPosition):
        self.UseOwnCoordSys = True
        self.OwnPosition = xy
        self.GoToPosition()

    def GoToPosition(self):
        self._goToPositionCOM.ExecuteTrigger()

    @property
    def UseOwnCoordSys(self) -> bool:
        return self._useOwnCoodSysCOM.Value
    
    @UseOwnCoordSys.setter
    def UseOwnCoordSys(self, val: bool):
        self._useOwnCoodSysCOM.Value = val

    @property
    def OwnPosition(self) -> XYPosition:
        return XYPosition(self._ownPositionXCOM.Value, self._ownPositionYCOM.Value)

    @OwnPosition.setter
    def OwnPosition(self, ownPosition: XYPosition):
        self._ownPositionXCOM.Value = ownPosition.X
        self._ownPositionYCOM.Value = ownPosition.Y
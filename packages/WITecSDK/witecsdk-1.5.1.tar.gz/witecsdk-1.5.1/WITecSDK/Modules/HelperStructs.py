from math import hypot

userparam = "UserParameters|"
microscopecontrol = "MultiComm|MicroscopeControl|"
datachannelpath = "Status|Hardware|Controller|DataChannels|"
specchannelpath = userparam + "DAQSources|SpectralChannels|"

class AutofocusSettings:
    """Class to define settings for the spectral Autofocus"""
    def __init__(self, aMinimalIntegrationTime: float = 0.05, aStepSizeMultiplier: float = 1,
                 aMaximumRange: float = 100, aCenter: float = 40, aMask: str = "100;3600"):
        self.MinimalIntegrationTime: float = aMinimalIntegrationTime
        self.StepSizeMultiplier: float = aStepSizeMultiplier
        self.MaximumRange: float = aMaximumRange
        self.Center: float = aCenter
        self.Mask: str = aMask

class DataChannelDescription:
    """Class to define data channels for the Slow Time Series"""
    def __init__(self, aCaption: str, aUnit: str):
        self.Caption: str = aCaption
        self.Unit: str = aUnit

class XYPosition:
    """Class to handle a XY positions (2D)"""
    def __init__(self, x: float = 0, y: float = 0):
        self.X: float  = x
        self.Y: float  = y

    def __str__(self):
        return f"X: {self.X:.2f}, Y: {self.Y:.2f} [µm]"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, XYPosition):
            return self.X == other.X and self.Y == other.Y
        else:
            return NotImplemented
        
    def __add__(self, other):
        if isinstance(other, XYPosition):
            X = self.X + other.X
            Y = self.Y + other.Y
            return self.__class__(X,Y)
        else:
            return NotImplemented
        
    def __sub__(self, other):
        if isinstance(other, XYPosition):
            X = self.X - other.X
            Y = self.Y - other.Y
            return self.__class__(X,Y)
        else:
            return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            X = self.X * other
            Y = self.Y * other
            return self.__class__(X,Y)
    
    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            X = self.X / other
            Y = self.Y / other
            return self.__class__(X,Y)
        
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __iadd__(self, other):
        return self.__add__(other)
        
    def __abs__(self) -> float:
        return hypot(self.X, self.Y)

class SamplePositionerPosition(XYPosition):
    """XYPostion class with compatible name"""
    pass

class XYZPosition:
    """Class to handle a XYZ positions (3D)"""
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.X: float  = x
        self.Y: float  = y
        self.Z: float  = z

    @property
    def SamplePosition(self) -> XYPosition:
        """Defines the XY position only"""
        return XYPosition(self.X, self.Y)
    
    @SamplePosition.setter
    def SamplePosition(self, xy: XYPosition):
        self.X = xy.X
        self.Y = xy.Y

    def AsString(self) -> str:
        """Returns the values as string"""
        return f"{self.X:.4f};{self.Y:.4f};{self.Z:.4f}"

    def __str__(self):
        return f"X: {self.X:.2f}, Y: {self.Y:.2f}, Z: {self.Z:.2f} [µm]"
    
    def __eq__(self, other):
        if type(other) == self.__class__:
            return self.X == other.X and self.Y == other.Y and self.Z == other.Z
        else:
            return NotImplemented

class LargeAreaSettings:
    """Class to define and load settings for a Large Area Scan"""
    def __init__(self, mode: int, points: int, lines: int, layers: int, width: float, height: float, depth: float, integrationTime: float, center: XYZPosition, gamma: float):
        self.Mode: int  = mode
        self.Points: int = points
        self.Lines: int = lines
        self.Layers: int = layers
        self.Width: float  = width
        self.Height: float  = height
        self.Depth: float  = depth
        self.IntegrationTime: float  = integrationTime
        self.Center: XYZPosition  = center
        self.Gamma: float  = gamma

    def AsString(self) -> str:
        """Returns a string containing all parameters"""
        return (f"{self.Mode};{self.Points};{self.Lines};{self.Layers};{self.Width:.4f};{self.Height:.4f};{self.Depth:.4f};" +
                f"{self.IntegrationTime:.5f};{self.Center.AsString()};{self.Gamma:.4f}")
    
    @classmethod
    def FromString(cls, input: str):
        """Creates an instance of this class from a string input"""
        strlst = input.split(';')
        if len(strlst) != 12:
            raise Exception('String input not matching pattern')
        try:
            args = (int(strlst[0]), int(strlst[1]), int(strlst[2]), int(strlst[3]), float(strlst[4]), float(strlst[5]), float(strlst[6]),
                    float(strlst[7]), XYZPosition(float(strlst[8]), float(strlst[9]), float(strlst[10])), float(strlst[11]))
        except Exception as e:
            raise Exception('Converting strings to numbers not successful') from e
        
        return LargeAreaSettings(*args)

class Spectrum:
    """Class to handle spectra retrieved from the silent spectrum"""
    def __init__(self):
        self.XData: list[float] = None
        self.SpectrumData: list[float] = []
        self.Title: list[str] = []
        self.ExcitationWavelength: float = None
        self.SpectrumSize: int = None
        self.XDataKind: str = None
        self.IntegrationTime: float = None
        self.SpectrumNumber: int = []
        self.Accumulations: int = 0

    @property
    def XRamanData(self) -> list[float]:
        """Retrieves the spectrum x-axis"""
        if self.XData is None or self.ExcitationWavelength is None:
            raise Exception('XData and ExcitationWavelength necessary')
        return [((1 / self.ExcitationWavelength - 1 / i) * 10 ** 7) for i in self.XData]
    
    @property
    def AccumulatedSpectrumData(self) -> list[float]:
        """Retrieves the averaged spectrum over all accumulations"""
        if self.Accumulations == 0:
            raise Exception('No SpectrumData available')
        AccSpecData = []
        for column in range(self.SpectrumSize - 1):
            AccSpecData.append(sum(row[column] for row in self.SpectrumData) / self.Accumulations)
        return AccSpecData
    
    @classmethod
    def FromTrueMatchString(cls, input: str):
        """Creates an instance of this class from the ASCII output"""
        newspec = Spectrum()
        sections = input.split('\n\n')
        for section in sections:
            seclist = section.split('\n')
            secheader = seclist[0]
            del seclist[0]
            if secheader == '[WITEC_TRUEMATCH_ASCII_HEADER]':
                for sline in seclist:
                    lparts = sline.split(' = ')
                    if lparts[0] == 'Version':
                        if float(lparts[1]) < 2.0:
                            raise Exception('WITec TrueMatch ASCII Version not supported')
            elif secheader == '[XData]':
                newspec.XData = [float(i) for i in seclist]
            elif secheader == '[SpectrumHeader]':
                for sline in seclist:
                    lparts = sline.split(' = ')
                    if lparts[0] == 'Title':
                        newspec.Title.append(lparts[1])
                    elif lparts[0] == 'ExcitationWavelength':
                        newspec.ExcitationWavelength = float(lparts[1])
                    elif lparts[0] == 'SpectrumSize':
                        newspec.SpectrumSize = int(lparts[1])
                    elif lparts[0] == 'XDataKind':
                        newspec.XDataKind = lparts[1]
            elif secheader == '[SampleMetaData]':
                for sline in seclist:
                    lparts = sline.split(' = ')
                    if lparts[0] == 'double Integration_Time':
                        newspec.IntegrationTime = float(lparts[1])
                    elif lparts[0] == 'int Spectrum_Number':
                        newspec.SpectrumNumber.append(int(lparts[1])) 
            elif secheader == '[SpectrumData]':
                del seclist[-1]
                newspec.SpectrumData.append([float(i) for i in seclist])
                newspec.Accumulations += 1
        
        return newspec

from math import floor, ceil

from pyanten.Measurement.NearField.Planar.samplingLength import samplingLength

def samplingParameters(frequency: float, L: float):
  r""" Planar near-field antenna measurement sampling count according to frequency and desired minimum length

  Parameters
  ----------
  frequency : float
              frequency of interest in Hertz [Hz]
  L         : float
              desired minimum scan length [m]

  Returns
  -------
  Lm    : float
          sampling start position [m]
  Lp    : float
          sampling stop position [m] (equals to negative of Lp)
  N     : float
          samplng count
  Delta : float
          spatial samplng length [mm]

  Notes
  -----
  Calculation assumes a scanning region centered on the AUT.  

  Formula
  -------
  .. math::
      theta = \tan^{-1} \left \dfrac{L-a}{2d} \right
  """
  
  samplingLengthInmm = floor(samplingLength(frequency)*1E3)
  scanLengthInmm     = ceil(L*1E3)
  halfScanLengthInmm = scanLengthInmm/2 if scanLengthInmm%2 ==0 else (scanLengthInmm+1)/2
  if halfScanLengthInmm%samplingLengthInmm > 0:
    halfScanLengthInmm = halfScanLengthInmm + (samplingLengthInmm-halfScanLengthInmm%samplingLengthInmm)
  
  N  = 2*(halfScanLengthInmm/samplingLengthInmm)+1
  Lm = -halfScanLengthInmm
  Lp = +halfScanLengthInmm
  
  return ( Lm/1E3, Lp/1E3, int(N), int(samplingLengthInmm) )
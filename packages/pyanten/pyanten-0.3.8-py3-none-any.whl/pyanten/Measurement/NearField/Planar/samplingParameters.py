from math import floor, ceil

from pyanten.Measurement.NearField.Planar.samplingSpacing import samplingSpacing

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
  
  samplingSpacingInmm = floor(samplingSpacing(frequency)*1E3)
  scanLengthInmm     = ceil(L*1E3)
  halfScanLengthInmm = scanLengthInmm/2 if scanLengthInmm%2 ==0 else (scanLengthInmm+1)/2
  if halfScanLengthInmm%samplingSpacingInmm > 0:
    halfScanLengthInmm = halfScanLengthInmm + (samplingSpacingInmm-halfScanLengthInmm%samplingSpacingInmm)
  
  N  = 2*(halfScanLengthInmm/samplingSpacingInmm)+1
  Lm = -halfScanLengthInmm
  Lp = +halfScanLengthInmm
  
  return ( Lm/1E3, Lp/1E3, int(N), int(samplingSpacingInmm) )
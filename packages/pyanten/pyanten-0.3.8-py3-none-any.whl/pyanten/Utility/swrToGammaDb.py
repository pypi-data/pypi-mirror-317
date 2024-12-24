from math import log10

from pyanten.Utility.swrToGamma import swrToGamma

def swrToGammaDb(swr: float):
  """ Voltage standing wave ratio (vswr) to reflection coefficient (gamma) in decibel conversion

  Parameters
  ----------
  swr : float
      standing wave ratio (swr)

  Returns
  -------
  gamma : float
      reflection coefficient (s11) [dB]
  """
  
  return 20*log10(swrToGamma(swr))
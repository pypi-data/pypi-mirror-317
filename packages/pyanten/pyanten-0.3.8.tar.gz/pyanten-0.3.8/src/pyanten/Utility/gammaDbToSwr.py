from math import pow

from pyanten.Utility.gammaToSwr import gammaToSwr

def gammaDbToSwr(gamma: float):
  """ Reflection coefficient (gamma) in decibels to voltage standing wave ratio (vswr) conversion

  Parameters
  ----------
  gamma : float
      reflection coefficient (s11) [dB]

  Returns
  -------
  swr : float
      standing wave ratio (swr)
  """

  return gammaToSwr(pow(10,gamma/20))
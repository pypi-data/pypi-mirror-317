import math

def gammaDbToReflectedPowerPercentage(gamma: float) -> float:
  """ Reflection coefficient (gamma) in decibels to reflected power percentage

  Parameters
  ----------
  gamma : float
    reflection coefficient (s11) [dB]

  Returns
  -------
  float
    reflected power percentage
  """

  return math.pow(10,gamma/20)*math.pow(10,gamma/20)*100
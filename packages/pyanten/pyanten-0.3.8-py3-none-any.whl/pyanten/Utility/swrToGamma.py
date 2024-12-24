
def swrToGamma(swr: float):
  """ Voltage standing wave ratio (vswr) to reflection coefficient (gamma) conversion

  Parameters
  ----------
  swr : float
      standing wave ratio (swr)

  Returns
  -------
  gamma : float
      reflection coefficient (s11)
  """
  return (swr-1)/(swr+1)

def gammaToSwr(gamma: float):
  """ Reflection coefficient (gamma) to voltage standing wave ratio (vswr) conversion

  Parameters
  ----------
  gamma : float
      reflection coefficient (s11)

  Returns
  -------
  swr : float
      standing wave ratio (swr)
  """
  return (1+gamma)/(1-gamma)
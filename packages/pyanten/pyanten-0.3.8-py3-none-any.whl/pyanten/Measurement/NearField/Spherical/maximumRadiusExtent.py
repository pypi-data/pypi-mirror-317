from math import sqrt

def maximumRadiusExtent(dx: float, dy:float, dz:float):
  r""" Calculates maximum radial extend (MRE) of the antenna for spherical near-field (SNF) measurements

  Parameters
  ----------
  dx : float
       max displacement from rotation center along x-axis
  dy : float
       max displacement from rotation center along y-axis
  dz : float
       max displacement from rotation center along z-axis

  Returns
  -------
  mre : float
        maximum radius extent

  Notes
  -----
  Calculation is unitless so output is the same quantity of inputs.

  Formula
  -------
  .. math::
      mre = \sqrt{dx^2+dy^2+dz^2}
  """
  
  return sqrt(dx*dx + dy*dy + dz*dz)

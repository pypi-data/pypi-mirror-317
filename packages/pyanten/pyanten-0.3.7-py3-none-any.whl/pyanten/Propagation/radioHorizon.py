from math import sqrt

def radioHorizon(height: float):
  r""" Radio horizon in kilometers [km] for a given height

  Parameters
  ----------
  height : float
           height of transmitter/recevier above ground in meters [m]

  Returns
  -------
  Rh : float
       radio horizon in kilometers [km]

  References
  ----------
  .. [1] [Line-of-sight propagation - Wikipedia](https://en.wikipedia.org/wiki/Line-of-sight_propagation)

  Formula
  -------
  .. math::
      R_{rh} \approx 4.12\times\sqrt{h} [km]
  """
  
  return 4.12*sqrt(height)
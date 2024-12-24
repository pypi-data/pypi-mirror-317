from math import sqrt

def lineOfSight(height: float):
  r""" Line-of-sight range in kilometers [km] for a given height

  Parameters
  ----------
  height : float
           height of transmitter/recevier above ground in meters [m]

  Returns
  -------
  LOS : float
        line-of-sight distance in kilometers [km]

  References
  ----------
  .. [1] [Line-of-sight propagation - Wikipedia](https://en.wikipedia.org/wiki/Line-of-sight_propagation)

  Formula
  -------
  .. math::
      R_{los} = \sqrt{2\cdotR\cdoth} \approx 3.57\times\sqrt{h} [km]
  """

  return 3.57*sqrt(height)
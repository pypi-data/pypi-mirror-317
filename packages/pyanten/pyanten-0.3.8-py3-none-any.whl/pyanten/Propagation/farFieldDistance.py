from pyanten.Utility import frequencyToWavelength

def farFieldDistance(frequency: float, D: float):
  r""" Far-field (Fraunhofer) distance of an antenna or aperture

  Parameters
  ----------
  frequency : float
              frequency of interest in Hertz [Hz]
  D         : float
              maximum cross-sectional size [m]

  Returns
  -------
  Rff : float
        minimum far-field range in meters [m]

  References
  ----------
  .. [1] IEEE 1720-2012 Recommended Practice for Near-Field Antenna Measurements, Section B.2.2, Page 175, Equation B.6.
  .. [2] Warren L. Stutzman, Antenna Theory and Design, 3rd Ed., Page 43.

  Formula
  -------
  .. math::
      R_{ff} = Max\left(\dfrac{2D^2}{\lambda},5D,1.6\lambda\right)
  """

  wavelength = frequencyToWavelength(frequency)
  return max([2*D*D/wavelength, 5*D, 1.6*wavelength])




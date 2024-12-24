from pyanten.Utility import frequencyToWavelength

def seperationDistance(frequency: float, closer: bool = False) -> float:
  r""" Minimum recommended seperation distance for near-field antenna measurements in meters

  Parameters
  ----------
  frequency : float
    frequency of interest in Hertz [Hz]

  closer : bool
    closer approximation using 3 wavelength calculation

  Returns
  -------
  float
    minimum distance

  Notes
  -----
  Standard suggests to choose between 3 or 5 wavelength.
  In order to ensure copuling effect, 5 wavelength distance is choosen and implemented. 3 wavelength is optional.

  .. [1] IEEE 1720-2012 Recommended Practice for Near-Field Antenna Measurements, Section 5.3.1.4, Page 27.

  Formula
  -------
  .. math::
      R_{nf} = 5\times\lambda = 5\times c_0/f
  """
  return 3*frequencyToWavelength(frequency) if closer else 5*frequencyToWavelength(frequency)
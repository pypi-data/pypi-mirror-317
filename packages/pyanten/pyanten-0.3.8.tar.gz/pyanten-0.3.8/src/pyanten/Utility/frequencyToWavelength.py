from scipy.constants import speed_of_light

def frequencyToWavelength(frequency: float):
  """ Converts frequency to wavelength

  Parameters
  ----------
  frequency : float
      frequency in Hertz [Hz]

  Returns
  -------
  wavelength : float
      wavelength in meters [m]
  """
  return speed_of_light / frequency
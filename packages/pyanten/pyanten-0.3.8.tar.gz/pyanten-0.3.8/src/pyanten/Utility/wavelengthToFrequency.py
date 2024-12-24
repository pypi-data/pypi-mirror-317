from pyanten.Utility.frequencyToWavelength import frequencyToWavelength

def wavelengthToFrequency(wavelength: float):
  """ Converts frequency to wavelength

  Parameters
  ----------
  wavelength : float
      wavelength in meters [m]

  Returns
  -------
  frequency : float
      frequency in Hertz [Hz]
  """

  return frequencyToWavelength(wavelength)
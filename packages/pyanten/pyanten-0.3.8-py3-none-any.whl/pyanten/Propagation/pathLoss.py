from math import log10

def pathLoss(frequency: float, R: float, G1: float, G2:float):
  r""" Free space path loss under far-field condition

  Parameters
  ----------
  frequency : float
              frequency of interest in MegaHertz [MHz]
  R         : float
              range in kilometers [km]
  G1        : float
              gain of transmitter antenna in decibels [dB]
  G2        : float
              gain of receiver antenna in decibels [dB]

  Returns
  -------
  Lp : float
       path loss in decibels [dB]

  Notes
  -----
  This calculation valid if two antennas are seperated enough to be inside far-field (Fraunhofer) region.

  References
  ----------
  .. [1] IEEE 1720-2012 Recommended Practice for Near-Field Antenna Measurements, Section B.2.2, Page 175, Equation B.6.
  .. [2] Warren L. Stutzman, Antenna Theory and Design, 3rd Ed., Page 43.

  Formula
  -------
  .. math::
      L_P = 32.45 + 20\log10(fR) - G_1 - G_2 \quad [dB]
  """

  return 32.45 + 20*log10(frequency*R) - G1 - G2

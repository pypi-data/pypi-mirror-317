from enum import Enum
from scipy.signal.windows import taylor, chebwin


def amplitudeTaper(N: int, sll: float, window: str = "taylor", **kwargs):
  r""" Generate amplitude taper coefficients for antenna elements in sidelobe controlle array 

  Parameters
  ----------
  N      : int 
           number of array elements
  sll    : float
           desired sidelobe level [dB]
  taper  : str 
           window function associated to desired distribution that can be:
           taylor,
           dolhp-chebyshev / chebyshev / tchebyshev 
**kwargs : dict
           window specific properties. Valid keyword arguments are: 

           taylor_nbar: int: Number of nearly constant-level sidelobes adjacent to the mainlobe in taylor window (default=4)
         
  Returns
  -------
  amplitudes : float[]
               amplitude array corresponds to each element

  References
  ----------
  .. [1] [taylor — SciPy v1.14.1 Manual](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.taylor.html)
  .. [1] [chebwin — SciPy v1.14.1 Manual](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.chebwin.html)
  .. [2] [Armin Doerry, “Catalog of Window Taper Functions for Sidelobe Control”, 2017](https://www.osti.gov/biblio/1365510)
  .. [3] [Sayedu Khasim, Noorbasha & Krishna Y, Murali & Thati, Jagadeesh & Subbarao, M.. (2013). ANALYSIS OF DIFFERENT TAPERING TECHNIQUES FOR EFFICIENT RADIATION PATTERN. e-Journal of Science & Technology (e-JST). 8. 47-55. ](https://www.dl.begellhouse.com/journals/0632a9d54950b268,4b96ebea37254651,10b28d794a40eb40.html)
  """

  if window == "dolhp-chebyshev" or window == "chebyshev" or window == "tchebyshev":
     return chebwin(N, at=sll)
  else:
     return taylor(N, nbar = 4 if "taylor_nbar" not in kwargs.keys() else kwargs["taylor_nbar"], sll=sll)
  



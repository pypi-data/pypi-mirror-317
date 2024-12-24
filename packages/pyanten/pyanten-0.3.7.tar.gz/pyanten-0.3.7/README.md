# PyAnten

Antenna Toolkit

## Installation

```shell
pip install pyanten
```

## Table of Modules and Functions

| Module      | Sub Module (Level1) | Sub Module (Level2) | Functinos                                                                                                                           |
| ----------- | ------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Utility     |                     |                     | frequencyToWavelength, gammaDbToSwr, gammaToSwr, swrToGamma, swrToGammaDb, wavelengthToFrequency, gammaDbToReflectedPowerPercentage |
| Propagation |                     |                     | farfFieldDistance, lineOfSight, pathLoss, radioHorizon,                                                                             |
| Measurement | NearField           |                     | seperationDistance,                                                                                                                       |
| Measurement | NearField           | Planar              | angleOfView, samplingParameters, samplingLength, scanLength,                                                                             |
| Measurement | NearField           | Spherical           | maximumRadiusExtent,                                                                                                                |
| Array       |                     |                     | amplitudeTaper,                                                                                                                     |

## References

[1] [A Python MoM antenna simulator](https://www.linkedin.com/pulse/python-mom-antenna-simulator-t-q-khai-nguyen/)  
[2] [How to document kwargs according to Numpy style docstring?](https://stackoverflow.com/questions/62511086/how-to-document-kwargs-according-to-numpy-style-docstring)

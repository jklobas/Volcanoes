# Volcanoes
Tools for analysis of model output from 2D chemical transport model

This code is designed to be used in a python 2.7 interactive session, such as ipython.

Tools to read binary output (outplqparser.py) and then visualize (ratevizzer.py) provide further insight into the processes which govern stratospheric ozone:
(a) vertical profile of chemical loss rates of ozone following various volcanic perturbations
![rateviz output](https://github.com/jklobas/Volcanoes/blob/master/figure2_4panel_frac.png)

Model outputs can be visualized within classes from the netcdf2py module netcdf.py:
(a) viewing contour plots of stratospheric chemicals
![ClO by latitude and pressure](https://github.com/jklobas/Volcanoes/blob/master/figure_1-2.png)
(b) viewing change in ozone column vs different years
![Ozone column relative to year zero, by latitude](https://github.com/jklobas/Volcanoes/blob/master/figure_2-1.png?raw=true)

And models can be visualized between classes using the o3columns module:
(a) gross ozone:
![model ozone at specific latitude](https://github.com/jklobas/Volcanoes/blob/master/figure_1-1.png?raw=true)
(b) % change in ozone:
![percent change vs no perturbation](https://github.com/jklobas/Volcanoes/blob/master/figure_1.png)
(c) time-series delta column value (ozone in this case) for any given permutation of eruption latitude / composition
![latitude prelim study](https://github.com/jklobas/Volcanoes/blob/master/figure4.png)




import numpy as np

## Reference functions and constants from Numpy
sq, sqrt = np.square, np.sqrt
exp = np.exp
pi  = np.pi

## Define a function that gives Y value for given X on a bell curve
def bell_curve(mu, std, x, scale = 1):
  numerator   = exp( sq(x - mu) / (-2 * sq(std)) )
  denominator = sqrt(2 * pi * sq(std))
  return numerator / denominator * scale

## Define constants
secs_per_h = 60 * 60
two_pm = secs_per_h * 14
max_pv_kw = 3.25
std = 12000

## Compute scale to better match Real PV Power Values
scale = max_pv_kw / bell_curve(two_pm, std, two_pm)

## Define a function to be used in other modules 
## to simulate PV Power Value at time of day
def pv_kw_power_curve_value(sec_of_day):
  return bell_curve(two_pm, std, sec_of_day, scale)

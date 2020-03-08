import numpy as np

sq, sqrt = np.square, np.sqrt
exp = np.exp
pi  = np.pi

def bell_curve(mu, std, x, scale = 1):
  numerator   = exp( sq(x - mu) / (-2 * sq(std)) )
  denominator = sqrt(2 * pi * sq(std))
  return numerator / denominator * scale

secs_per_h = 60 * 60
two_pm = secs_per_h * 14
max_pv_kw = 3.25
std = 12000

scale = max_pv_kw / bell_curve(two_pm, std, two_pm)

def pv_kw_power_curve_value(sec_of_day):
  return bell_curve(two_pm, std, sec_of_day, scale)

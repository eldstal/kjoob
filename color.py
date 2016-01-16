def blend(color_a, color_b, a_factor):
  """ a_factor=1 is all a, a_factor=0 is all b """
  b_factor = 1 - a_factor
  channels = zip(color_a, color_b)
  out = tuple([ a * a_factor + b * b_factor for (a,b) in channels ])
  return out

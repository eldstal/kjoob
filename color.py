import collections

RAINBOW = [ (120, 197, 214),
            ( 69, 155, 168),
            (121, 194, 103),
            (197, 214,  71),
            (245, 214,  61),
            (242, 140,  51),
            (232, 104, 162),
            (191,  98, 166)]

def blend(a, b, b_factor):
  """ b_factor=1 is all b, b_factor=0 is all a """

  if isinstance(a, collections.Iterable):
    # iterable (tuple, color, whatever)
    a_factor = 1 - b_factor
    channels = zip(a, b)
    out = tuple([ int(a * a_factor + b * b_factor) for (a,b) in channels ])
  else:
    # not iterable (just an integer)
    return a * (1-b_factor) + b* b_factor
  return out

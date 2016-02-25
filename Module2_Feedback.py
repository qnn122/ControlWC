"""
In this module, a feedback monitor is added.
The feedback block will regularly (through a timer) read the number
of ticks of 2 wheels and display them on the GUI. The # of tick tells
us how fast the wheelchair truly is since the real velocity of the
wheelchair depends on many factors, e.g. weight of the user.
"""
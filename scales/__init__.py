"""
A module to deal with the maths of musical intervals, scales and temperaments.
"""

import numpy as np

def scale_from_rates(origin, rates):
    """
     Return the frequencies originated by applying the interval ratios `rates`
     to the `origin` frequency.
    """
    return np.cumprod(np.concatenate([[origin], rates]))

class ToneBasis:
    """
     A representation of a sequence of musical intervals that can be combined
     to form scales.
    """

    def __init__(self, intervals):
        """
         Create a representation of the intervals given in cents.
        """
        self.intervals = np.array(intervals)

    @classmethod
    def equidistant(cls, n):
        """
         Create a representation of a equal division of an octave into `n`
         intervals.
        """
        intervals = 1200/n * np.ones(n)
        return cls(intervals)

    def rates(self):
        """
         Return the frequency ratios that correspond to the intervals.
        """
        return 2 ** (self.intervals/1200)

    def scale(self, origin):
        """
         Return a scale formed by the intervals of this basis applied to the
         note of frequency `origin`.
        """
        return scale_from_rates(origin, self.rates())

    def to_scale(self, origin):
        """
         Return a Scale object formed by the intervals of this basis applied to the
         note of frequency `origin`.
        """
        return Scale(origin, self.rates())

class Scale:
    def __init__(self, origin=None, rates=None, notes=None):
        """
         An object representing a scale constructed upon a frequency `origin`
         with interval frequency `rates`.
        """
        if notes is None:
            if origin is None or rates is None:
                raise ValueError('both origin and rates must be given if notes not given')
            self.notes = scale_from_rates(origin, rates)
        else:
            if origin is not None or rates is not None:
                raise ValueError('origin and rates must be None if notes is given')
            self.notes = np.array(notes)

    def copy(self):
        """Return a copy of this object."""
        return Scale(notes=self.notes)

    def rates(self):
        """Return the frequency ratios between the notes in this scale."""
        return self.notes[1:] / self.notes[:-1]

    def intervals(self):
        """Return the scale's intervals in cents."""
        return 1200 * np.log2(self.rates())

    def set_note(self, index, cents, reference='current'):
        """
         Alter the `index`-th note of the scale to a interval of `cents`
         according to the chosen `reference`:
             'current'  -- alter the note by `cents` relative to its current
                            pitch;
             'previous' -- alter the note to `cents` above its predecessor on
                            the scale;
             'origin'   -- alter the note to `cents` above the scale origin;
        """
        rate = 2 ** (cents/1200)
        if reference == 'current':
            self.notes[index] *= rate
        elif reference == 'previous':
            self.notes[index] = self.notes[index-1] * rate
        elif reference == 'origin':
            self.notes[index] = self.notes[0] * rate
        return self


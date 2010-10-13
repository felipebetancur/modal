# Copyright (c) 2010 John Glover, National University of Ireland, Maynooth
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import modal
from modal import EnergyODF, LPEnergyODF
from modal.pydetectionfunctions import EnergyODF as CEnergyODF
from modal.pydetectionfunctions import LPEnergyODF as CLPEnergyODF
import numpy as np
import unittest


class TestEnergyODFs(unittest.TestCase):
    FLOAT_PRECISION = 5 # number of decimal places to check for accuracy

    def test_py_c_equal(self): 
        audio, sampling_rate, onsets = modal.get_audio_file('piano_G2.wav')
        audio = audio[0:4096]
        frame_size = 512
        hop_size = 512
        py_odf = EnergyODF()
        py_odf.set_frame_size(frame_size)
        py_odf.set_hop_size(hop_size)
        c_odf = CEnergyODF()
        c_odf.set_frame_size(frame_size)
        c_odf.set_hop_size(hop_size)
        # if necessary, pad the input signal
        if len(audio) % hop_size != 0:
            audio = np.hstack((audio, np.zeros(hop_size - (len(audio) % hop_size),
                                               dtype=np.double)))
        # get odf samples
        py_samples = py_odf.process(audio)
        c_samples = np.zeros(len(py_samples), dtype=np.double)
        c_odf.process(audio, c_samples)

        self.assertEquals(len(py_samples), len(c_samples))
        for i in range(len(py_samples)):
            self.assertAlmostEquals(py_samples[i], c_samples[i],
                                    places=self.FLOAT_PRECISION)
 
    def test_py_c_equal_rt(self):       
        audio, sampling_rate, onsets = modal.get_audio_file('piano_G2.wav')
        audio = audio[0:4096]
        frame_size = 256
        hop_size = 256
        py_odf = EnergyODF()
        py_odf.set_frame_size(frame_size)
        py_odf.set_hop_size(hop_size)
        c_odf = CEnergyODF()
        c_odf.set_frame_size(frame_size)
        c_odf.set_hop_size(hop_size)
        # if necessary, pad the input signal
        if len(audio) % hop_size != 0:
            audio = np.hstack((audio, np.zeros(hop_size - (len(audio) % hop_size),
                                               dtype=np.double)))
        # get odf samples
        audio_pos = 0
        while audio_pos <= len(audio) - frame_size:
            frame = audio[audio_pos:audio_pos+frame_size]
            py_odf_value = py_odf.process_frame(frame)
            c_odf_value = c_odf.process_frame(frame)
            self.assertAlmostEquals(py_odf_value, c_odf_value,
                                    places=self.FLOAT_PRECISION)
            audio_pos += hop_size
            
            
class TestLPEnergyODFs(unittest.TestCase):
    audio_file = '../examples/audio/drums.wav'
    FLOAT_PRECISION = 5 # number of decimal places to check for accuracy
    order = 5

    def test_py_c_equal(self): 
        audio, sampling_rate, onsets = modal.get_audio_file('piano_G2.wav')
        audio = audio[0:4096]
        frame_size = 512
        hop_size = 512
        py_odf = LPEnergyODF()
        py_odf.set_frame_size(frame_size)
        py_odf.set_hop_size(hop_size)
        py_odf.set_order(self.order)
        c_odf = CLPEnergyODF()
        c_odf.set_frame_size(frame_size)
        c_odf.set_hop_size(hop_size)
        c_odf.set_order(self.order)
        # if necessary, pad the input signal
        if len(audio) % hop_size != 0:
            audio = np.hstack((audio, np.zeros(hop_size - (len(audio) % hop_size),
                                               dtype=np.double)))
        # get odf samples
        py_samples = py_odf.process(audio)
        c_samples = np.zeros(len(py_samples), dtype=np.double)
        c_odf.process(audio, c_samples)

        self.assertEquals(len(py_samples), len(c_samples))
        for i in range(len(py_samples)):
            self.assertAlmostEquals(py_samples[i], c_samples[i],
                                    places=self.FLOAT_PRECISION)

    def test_py_c_equal_rt(self):       
        audio, sampling_rate, onsets = modal.get_audio_file('piano_G2.wav')
        audio = audio[0:4096]
        frame_size = 256
        hop_size = 256
        py_odf = LPEnergyODF()
        py_odf.set_frame_size(frame_size)
        py_odf.set_hop_size(hop_size)
        c_odf = CLPEnergyODF()
        c_odf.set_frame_size(frame_size)
        c_odf.set_hop_size(hop_size)
        # if necessary, pad the input signal
        if len(audio) % hop_size != 0:
            audio = np.hstack((audio, np.zeros(hop_size - (len(audio) % hop_size),
                                               dtype=np.double)))
        # get odf samples
        audio_pos = 0
        while audio_pos <= len(audio) - frame_size:
            frame = audio[audio_pos:audio_pos+frame_size]
            py_odf_value = py_odf.process_frame(frame)
            c_odf_value = c_odf.process_frame(frame)
            self.assertAlmostEquals(py_odf_value, c_odf_value,
                                    places=self.FLOAT_PRECISION)
            audio_pos += hop_size

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestEnergyODFs('test_py_c_equal'))
    suite.addTest(TestEnergyODFs('test_py_c_equal_rt'))
    suite.addTest(TestLPEnergyODFs('test_py_c_equal'))
    suite.addTest(TestLPEnergyODFs('test_py_c_equal_rt'))
    unittest.TextTestRunner().run(suite)

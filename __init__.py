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

# import detection function classes
from detectionfunctions import OnsetDetectionFunction
from detectionfunctions import LinearPredictionODF
from detectionfunctions import PeakODF
from detectionfunctions import EnergyODF
from detectionfunctions import SpectralDifferenceODF
from detectionfunctions import ComplexODF
from detectionfunctions import LPEnergyODF
from detectionfunctions import LPSpectralDifferenceODF
from detectionfunctions import LPComplexODF
from detectionfunctions import PeakAmpDifferenceODF

# file paths
import os
pkg_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(pkg_path, "data")
onsets_path = os.path.join(data_path, "onsets.hdf5")
analysis_path = os.path.join(data_path, "analysis.hdf5")
results_path = os.path.join(data_path, "results.hdf5")

# list all files in the onsets database
def list_onset_files():
    import h5py
    try:
        onsets_db = h5py.File(onsets_path, 'r')
        return list(onsets_db)
    except:
        return []
    finally:
        onsets_db.close()

# list polyphonic files
def list_onset_files_poly():
    import h5py
    try:
        files = []
        onsets_db = h5py.File(onsets_path, 'r')
        for file in onsets_db:
            if onsets_db[file].attrs['texture'] == "Polyphonic":
                files.append(file)
        return files
    except:
        return []
    finally:
        onsets_db.close()

# get the current number of onsets in the onsets database
def num_onsets():
    import h5py
    try:
        num_onsets = 0
        onsets_db = h5py.File(onsets_path, 'r')
        for file in onsets_db:
            num_onsets += len(onsets_db[file].attrs['onsets'])
        return num_onsets
    except:
        return 0
    finally:
        onsets_db.close()

# get a given audio file from the onset database
def get_audio_file(file_name):
    import h5py
    import numpy as np
    audio = np.array([])
    sampling_rate = 0.0
    onsets = np.array([])
    try:
        onsets_db = h5py.File(onsets_path, 'r')
        if file_name in onsets_db:
            # create new arrays so we can close the database connection
            audio = np.array(onsets_db[file_name], dtype=np.double)
            sampling_rate = onsets_db[file_name].attrs['sampling_rate']
            onsets = np.array(onsets_db[file_name].attrs['onsets'])
    finally:
        onsets_db.close()
        return (audio, sampling_rate, onsets)

#!/usr/bin/env python

"""
Copy audio files from a modal database to a given output directory.

An optional audio file name may be given in order to only extract a single
audio file. If omitted, all files will be extracted.

For each audio file, the metadata will also be extracted to a YAML file in
the same directory, called file_name.yaml.
"""
import sys
import os
import h5py
import yaml
from scipy.io.wavfile import write
import numpy as np

def _extract_file(audio_db, output_dir, file_name):
    sampling_rate = int(audio_db[file_name].attrs['sampling_rate'])
    audio = np.asarray(np.array(audio_db[file_name]) * 32768.0, np.int16)
    write(os.path.join(output_dir, file_name), sampling_rate, audio)
    onsets = [int(o) for o in audio_db[file_name].attrs['onsets']]
    metadata = {'onsets': onsets, 'sampling_rate': sampling_rate}
    metadata_file = os.path.join(output_dir, file_name + '.yaml')
    with open(metadata_file, 'w') as f:
        f.write(yaml.dump(metadata))

if __name__ == '__main__':
    usage = 'Usage: db_to_audio <audio database file> <output directory> [<audio file>]'
    if len(sys.argv) not in [3, 4]:
        print usage
        sys.exit(1)

    audio_db_path = sys.argv[1]
    output_dir = sys.argv[2]

    if len(sys.argv) == 4:
        file_name = sys.argv[3]
    else:
        file_name = None

    try: 
        audio_db = h5py.File(audio_db_path, 'r')
        if file_name:
            _extract_file(audio_db, output_dir, file_name)
        else:
            for file_name in audio_db:
                _extract_file(audio_db, output_dir, file_name)
    finally:
        if audio_db:
            audio_db.close()

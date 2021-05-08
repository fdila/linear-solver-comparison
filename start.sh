#!/bin/bash
echo "PYTHON:"
cd python;
python main.py;
echo "MATLAB:"
cd ../matlab;
bash exec.sh;
echo "OCTAVE:"
cd ../octave;
# exec octave
cd ..;

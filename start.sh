#!/bin/bash
echo "PYTHON:"
cd python;
python3 main.py;
echo "MATLAB:"
cd ../matlab;
bash exec.sh;
echo "OCTAVE:"
cd ../octave;
octave --persist main.m
cd ..;

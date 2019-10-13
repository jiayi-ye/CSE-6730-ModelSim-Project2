# CX 4230: Computer Simulation Project 2

Simulating average time to pass through Peachtree Street southbound between 10th and 14th street in Atlanta, GA with NGSIM Traffic Data.

## Models

This project contains three different models for traffic. 
- Activity Scanning Queueing (contained in `ActivityScan` directory)
- Event Oriented Queueing (contained in `EventOriented` directory)
- Cellular Automata (contained in `CA` directory)

Each of these directories contains a `README.md` explaining how to run the simulation.

## Background Distributions
To generate background distribution see `Background Distribution.ipynb`. This requires that the NGSIM data is in a directory at the root level called `NGSIM-Data` however is not included in this repo because it is very large.

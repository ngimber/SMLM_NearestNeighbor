Nearest Neighbor Analysis for Single Molecule Localization Microscopy
==========

The included Python script calculates the (k)-nearest neighbor distribution from single-molecule localization microscopy data.
Localization tables must have the ThunderSTORM [1] file format.

The script was used for the the following publications:



Instruction
-------

- Localization tables must have the ThunderSTORM .csv file format. x/y columns have the headers: "x [nm]" and "y [nm]" (including quotation marks).
- Subject and reference files must be stored in the same folder and file names must contain channel-specific identifyer (e.g. ch1 and ch2).
- Users will be asked to set the following parameters:
    - k: The rank of the neighbor being searched. For a 'nearest neighbors analysis' chose k = 0. k > 1 will calculate the 'k nearest neighbor' distribution with the rank k.
    - Subset: In order to speed up calculations, a random subset of reference localizations can be generated from the localization table and analyzed. '0' will process the whole dataset.
    - Block size: The references will be split into blocks before processing in order to save memory. In cases of memory overload this value msut be reduced.
    - File identifyer subject: e.g. 'ch1'
    - File identifyer reference: e.g. 'ch2'
  
- Output files will have a 'R' for reference or a 'S' for subject in their filename.


References
-------
[1] Ovesny, M., et al., ThunderSTORM: a comprehensive ImageJ plug-in for PALM and STORM data analysis and super-resolution imaging. Bioinformatics, 2014. 30(16): p. 2389-90. 

# Hydrogenline

This package provides scripts to interface with the RTL-SDR to automate measurements for [measuring the hydrogen line](https://www.on5vo.be/html/radio/hydrogenline.html).

Data is automatically stored in your home directory under `~/.hydrogenline`. It consists of a settings file `settings.json` and the averaged spectra under `[folder]/data/YYYMMDD_HH:MM:SS.npy`.

# Installation

To use the RTL-SDR on Linux, it must first be blacklisted as a device.

# Scripts

The scripts available as CLI executables:

- `capture`: captures samples repeatedly from the RTL-SDR, calculates and averages the PSD, and stores them.
- `waterfall`: creates a waterfall plot of the measured PSDs.
### SpecDB GUI

SpecDB GUI is a simple front-end for SpecDB and QUBRICS formatted spectral databases. It allows users to query a database and plot the results using either [Astrocook](https://das-oats.github.io/astrocook/), or matplotlib.

#### Requirements

- SpecDB and its requirements

- Astrocook and its requirements

- PySimpleGUI

If you are only interested in a QUBRICS formatted database, SpecDB is not required. We recommend using Conda or virtual environments to keep the base Python installation clean. The project is developed in Python 3.7, but any Python 3 version should work.

#### Installation

To install SpecDB GUI, follow these steps:

1- Clone the repository: `git clone https://github.com/G-Francio/SpecDB-Gui.git`

2 - Change the `ac_path` parameter in `config.yaml` to reflect the installation path of Astrocook.

3 - Start the GUI: `python gui.py`
### SpecDB GUI

A simple front-end for SpecDB and QUBRICS formatted spectral DataBases. It allows a user to query a database and plot the results using [Astrocook](https://das-oats.github.io/astrocook/), or matplotlib.

#### Requirements

- SpecDB, and its requirements

- Astrocook, and its requirements

- PySimpleGUI

If one is only interested in a QUBRICS formatted database, SpecDB is then not required.

Using a Conda, or virtual environments, is recommended, as they allow to keep the base python installation clean. The project is developed in Python3.7, but any Python3 version should work.

#### Installation

Clone the repository (`git clone https://github.com/G-Francio/SpecDB-Gui.git`) and change `ac_path` parameter in `config.yaml` so that it reflects the installation path of Astrocook's.

To start the GUI: `python gui.py`
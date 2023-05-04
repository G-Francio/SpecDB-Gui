from config import config, load_config

import PySimpleGUI as sg
import utils
import sys
import os
import log
import sdb

# check if SpecDB is installed by trying an import
try:
    from specdb.specdb import SpecDB
    config["specdb_installed"] = True
except ModuleNotFoundError:
    log.logger.warning(
        "SpecDB not found! You will only be able to search QUBRICS' formatted databases.")
    config["specdb_installed"] = False


# Set default font to be bigger
sg.set_options(font=(sg.DEFAULT_FONT, 13))


# Window to open the database selector
def make_db_select_window():
    layout = [[sg.Text("Select a database. Default loads the path of the default database.")],
              [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse()],
              [sg.Button("Open"), sg.Button("Cancel"), sg.Button("Default"),
              [sg.Checkbox('Is a QUBRICS formatted database?', default=config["qubrics_db"], key="is_qubrics_db")]]]
    return sg.Window('DB selection', layout, finalize=True)


# window to handle the search in specdb
def make_search_window():
    layout = [
        [sg.Text("RA (hms)"),  sg.InputText(size=(20, 1), key='-RA_HMS-'),  # , default_text="00:11:15.23"),
            sg.Text("DEC (dms)"), sg.InputText(size=(20, 1), key='-DEC_DMS-')],  # , default_text="14:46:01.8")],
        [sg.Text("RA (deg)"),  sg.InputText(size=(20, 1), key='-RA_DEC-'),
            sg.Text("DEC (deg)"), sg.InputText(size=(20, 1), key='-DEC_DEG-')],
        [sg.Text("qid     "),  sg.InputText(size=(20, 1), key='-QID-'),
            sg.Text("Matching r. ('')"), sg.InputText(size=(5, 1), key='-MATCH_R-', default_text="1")],
        [sg.B("Search"), sg.B("Open (mpl)"), sg.B("Open (Astrocook)")]
    ]
    return sg.Window('Search in DB', layout, finalize=True)


def load_db(active_db=None, is_qubrics=False):
    if not config["specdb_installed"] and not is_qubrics:
        return False, None

    if is_qubrics:
        config["active_db"] = active_db
        return True, None
    else:
        db = SpecDB(db_file=config["active_db"])
        config["active_db"] = active_db
        return True, db


def main():
    spectra = [None]

    # Create the window
    file_window, search_window = make_db_select_window(), None

    # Event loop
    while True:
        window, event, values = sg.read_all_windows()

        if window == file_window and event in (sg.WINDOW_CLOSED, "Cancel"):
            break

        if event == "Open":
            if os.path.isfile(values["-FILE-"]) and values["-FILE-"].endswith(".hdf5"):
                config["active_db"] = values["-FILE-"]
                config["qubrics_db"] = values["is_qubrics_db"]
                ok, db = load_db(config["active_db"], config["qubrics_db"])
                if not search_window:
                    search_window = make_search_window() if ok else sg.popup(
                        log.wrong_db_format, title="Error")
            elif os.path.isfile(values["-FILE-"]) and not values["-FILE-"].endswith(".hdf5"):
                sg.popup("Wrong file type: please load an hdf5 file.",
                         title="Error")
            else:
                sg.popup("File does not exists, check your path!", title="Error")
        elif event == "Default":
            file_window["-FILE-"].update(config["database"]["igmspec"])

        if window == search_window:
            if event in (sg.WIN_CLOSED, 'Exit'):
                search_window.close()
                search_window = None
            elif event == "Search":
                try:
                    spectra, n_spec = sdb.search_spectra(
                        values, db, is_qubrics=config["qubrics_db"], config=config)
                    sg.popup(f'Found {n_spec} spectra!', title="Info")
                except utils.InvalidInput as e:
                    sg.popup(str(e), title="Error")
                    log.logger.error(str(e))
            elif event == "Open (Astrocook)":
                if spectra[0] is None:
                    sg.popup("Nothing to open.", title="Warning")
                else:
                    utils.write_and_open(spectra)
            elif event == "Open (mpl)":
                print("TODO! Use astrocook if you can, it's much better anyway!")
                pass

    # Close the window
    file_window.close()
    if search_window is not None:
        search_window.close()
    # close open database
    try:
        # SpecDB deals with closin the DB on his own apparently
        db.close()
    except (AttributeError, UnboundLocalError):
        log.logger.warning("Nothing to close.")


if __name__ == '__main__':
    load_config(sys.argv[1] if len(sys.argv) > 1 else None)
    main()

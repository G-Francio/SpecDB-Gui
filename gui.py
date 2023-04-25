import PySimpleGUI as sg
import utils
from config import config, load_config
import sys
import os
import log
import sdb

# Set default font to be bigger
sg.set_options(font=(sg.DEFAULT_FONT, 13))

# Window to open the database selector


def make_db_select_window():
    layout = [[sg.Text("Select a database. Default loads the path of the default database.")],
              [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse()],
              [sg.Button("Open"), sg.Button("Cancel"), sg.Button("Default"),
              [sg.Checkbox('Is a QUBRICS formatted database?', default=False, key="is_qubrics_db")]]]
    return sg.Window('DB selection', layout, finalize=True)


# window to handle the search in specdb
def make_search_window():
    layout = [
        [sg.Text("RA (hms)"),  sg.InputText(size=(20, 1), key='-RA_HMS-'),
            sg.Text("DEC (dms)"), sg.InputText(size=(20, 1), key='-DEC_DMS-')],
        [sg.Text("RA (deg)"),  sg.InputText(size=(20, 1), key='-RA_DEC-'),
            sg.Text("DEC (deg)"), sg.InputText(size=(20, 1), key='-DEC_DEG-')],
        [sg.Text("qid     "),  sg.InputText(size=(20, 1), key='-QID-'),
            sg.Text("Matching r. ('')"), sg.InputText(size=(5, 1), key='-MATCH_R-', default_text="1")],
        [sg.B("Search"), sg.B("Open (mpl)"), sg.B("Open (Astrocook)")]
    ]
    return sg.Window('Search in DB', layout, finalize=True)


def _search_specdb(values):
    RA, DEC, tol = utils.parse_input(
        values['-RA_HMS-'], values['-DEC_DMS-'],
        values['-RA_DEC-'], values['-DEC_DEG-'],
        values['-MATCH_R-'])
    spectra = sdb.get_spectra(RA, DEC, tol)
    if spectra[0] is None:
        n_spec = 0
    else:
        n_spec = spectra[0].nspec
    return spectra, n_spec


def _search_qubrics(values):
    return None, 0


def _search_by_query(query):
    try:
        spectra = sdb.query_db(query)
        if spectra[0] is None:
            n_spec = 0
        else:
            n_spec = spectra[0].nspec
        return spectra, n_spec
    except AttributeError:
        return None, 0


def _search_by_qid(values):
    qid = utils.parse_qid(values["-QID-"])
    query = {'qid': qid}
    return _search_by_query(query)


def search_spectra(values, is_qubrics=False):
    if values["-QID-"] != "":
        return _search_by_qid(values)
    elif is_qubrics:
        return _search_qubrics(values)
    else:
        return _search_specdb(values)


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
            if os.path.isfile(values["-FILE-"]):
                config["active_db"] = values["-FILE-"]
                is_qubrics_db = values["is_qubrics_db"]
                if not search_window:
                    search_window = make_search_window()
            else:
                sg.popup("File does not exists, check your path!")
        elif event == "Default":
            file_window["-FILE-"].update(config["database"]["igmspec"])

        if window == search_window:
            if event in (sg.WIN_CLOSED, 'Exit'):
                search_window.close()
                search_window = None
            elif event == "Search":
                try:
                    spectra, n_spec = search_spectra(
                        values, is_qubrics=is_qubrics_db)
                    sg.popup(f'Found {n_spec} spectra!')
                except utils.InvalidInput as e:
                    sg.popup(str(e))
                    log.logger.error(str(e))
            elif event == "Open (Astrocook)":
                if spectra[0] is None:
                    sg.popup("Nothing to open.")
                else:
                    sdb.write_and_open(spectra)
            elif event == "Open (mpl)":
                print("TODO! Use astrocook if you can, it's much better anyway!")
                pass

    # Close the window
    file_window.close()
    if search_window is not None:
        search_window.close()


if __name__ == '__main__':
    load_config(sys.argv[1] if len(sys.argv) > 1 else None)
    main()


# import PySimpleGUI as sg
# import matplotlib.pyplot as plt

# """
#     Simultaneous PySimpleGUI Window AND a Matplotlib Interactive Window
#     A number of people have requested the ability to run a normal PySimpleGUI window that
#     launches a MatplotLib window that is interactive with the usual Matplotlib controls.
#     It turns out to be a rather simple thing to do.  The secret is to add parameter block=False to plt.show()
# """

# def draw_plot():
#     plt.plot([0.1, 0.2, 0.5, 0.7])
#     plt.show(block=False)

# layout = [[sg.Button('Plot'), sg.Cancel(), sg.Button('Popup')]]

# window = sg.Window('Have some Matplotlib....', layout)

# while True:
#     event, values = window.read()
#     if event in (sg.WIN_CLOSED, 'Cancel'):
#         break
#     elif event == 'Plot':
#         draw_plot()
#     elif event == 'Popup':
#         sg.popup('Yes, your application is still running')
# window.close()

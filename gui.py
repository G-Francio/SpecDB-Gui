import PySimpleGUI as sg
import sdb
import utils
import log

# Set default font to be bigger
sg.set_options(font=(sg.DEFAULT_FONT, 13))


def main():
    # Define the layout of the window
    layout = [
        [sg.Text("RA (hms)"), sg.InputText(size=(20, 1)),
         sg.Text("DEC (dms)"), sg.InputText(size=(20, 1))],
        [sg.Text("RA (deg)"), sg.InputText(size=(20, 1)),
         sg.Text("DEC (deg)"), sg.InputText(size=(20, 1))],
        [sg.Text("qid     "), sg.InputText(size=(20, 1)),
         sg.Text("Matching r. ('')"), sg.InputText(size=(5, 1))],
        [sg.Button("Search"), sg.Button("Open (mpl)"),
         sg.Button("Open (Astrocook)")]
    ]

    # Create the window
    window = sg.Window("SpecDB spectral search", layout)
    spectra = [None]

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Search":
            try:
                RA, DEC, tol = utils.parse_input(
                    values[0], values[1], values[2], values[3], values[5])
                spectra = sdb.get_spectra(RA, DEC, tol)
                if spectra[0] is None:
                    n_spec = 0
                else:
                    n_spec = spectra[0].nspec
                sg.popup(f'Found {n_spec} spectra!')
            except utils.InvalidInput as e:
                sg.popup(str(e))
                log.logger.error(str(e))

        elif event == "Open (Astrocook)":
            if spectra[0] is None:
                print("nothing searched, please search for a spectrum first!")
            else:
                sdb.write_and_open(spectra)
        elif event == "Open (mpl)":
            print("TODO! Use astrocook if you can, it's much better anyway!")
            pass

    # Close the window
    window.close()


if __name__ == '__main__':
    main()

import PySimpleGUI as sg

# Define the layout of the window
layout = [
    [sg.Text("RA (hms)"), sg.InputText(size=(20, 1)),
     sg.Text("DEC (dms)"), sg.InputText(size=(20, 1))],
    [sg.Text("RA (deg)"), sg.InputText(size=(20, 1)),
     sg.Text("DEC (deg)"), sg.InputText(size=(20, 1))],
    [sg.Column([[sg.Text("qid"), sg.InputText(size=(20, 1))]],
               justification='center')],
    [sg.Button("Search"), sg.Button("Open (mpl)"),
     sg.Button("Open (Astrocook)")]
]

# Create the window
window = sg.Window("My Simple GUI", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Search":
        # Handle search button click
        print("Search button clicked")
    elif event == "Open":
        # Handle open button click
        print("Open button clicked")

# Close the window
window.close()

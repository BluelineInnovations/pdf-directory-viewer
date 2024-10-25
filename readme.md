<!-- @format -->

# PDF Viewer Desktop App

- For those new to python, you should start the python session in a venv. Drill into the project directory, and run `source venv/bin/activate` (on macOS. use on windows may vary)
- Launch app, if from code, with `python main.py`

## What does it do?

This project was developed at the end of October, 2024, to aide in a situation where a large number of citation documents were printed, but not mailed. Due to them having been printed, we were unable to query any database to know what should potentially be voided. So Zach wrote an OCR application, Cole helped setup for mass scanning, and we scanned all the documents into digital PDF format, and used the OCR tool to lift the citation number. Although successful, the OCR app misread about 22% of the documents. That's where this tool comes into play.

This application allows a user to select a directory, and the app will display a list of all the PDF's in that directory. The user can then click one of the PDF's from the sidebar, and it will load into a workspace. The user will then be shown the selected PDF, and be allowed to type the citation number, from that document, a text field. When the user clicks enter, the content will save to a shared CSV file, that will be located in the root of the directory the user selected.

The application will show in the sidebar

- a list of PDF's in the directory
- Highlights in blue the sidebar item that is currently loaded in the workspace
- Changes the color of sidebar item green, if that item has a saved note
- changes the color of an item red, if that item is flagged

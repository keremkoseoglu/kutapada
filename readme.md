# Kutapada
Kutapada is a lightweight password keeper. Your passwords are kept in a local JSON file.

## Desktop
![Kutapada](/scr_desktop.png "Kutapada")
- Create your own JSON file, which should look like data/sample_data.json
- Modify config/config.json so it points to your own data file
- Run main.py

## Mobile
![Kutapada](/scr_ios.jpeg "Kutapada")
- Works over Dropbox
- Ensure that your JSON file is placed as Dropbox/Apps/kutapada/kutapada.json

## Warnings
The encryption within the JSON file is not very strong. If you fork this repository, you might want to improve data/encryption.py .

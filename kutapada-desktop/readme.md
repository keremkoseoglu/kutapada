# Kutapada
Kutapada is a lightweight password keeper. Your passwords are kept in a local JSON file.

# How to use
- Create your own JSON file, which should look like data/sample_data.json
- Modify config/config.json so it points to your own data file
- Run main.py

# Warnings
The encryption within the JSON file is not very strong. If you fork this repository, you might want to improve data/encryption.py .
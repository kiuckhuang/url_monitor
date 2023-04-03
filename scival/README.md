# README #

Python script to download scival api data

## How to use
- Install Python from Official website
https://www.python.org/downloads/

- Windows users
Run powershell from windows
```
powershell
```


- Install the required modules
```
cd \scival
pip install -r requirements.txt
```

- Run the script with following syntax
```
python scival_download.py -i scival_ids.txt -o scival_out.csv
```
    `scival_ids.txt` contains the scival author id
    `scival_out.csv` will be saved after fetch api output, in CSV format

- Use Excel to open the `scival_out.csv` file

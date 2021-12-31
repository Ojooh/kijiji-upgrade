# KIJIJI AUTOBOT

This is a scrapping tool for the kijiji web application, it scarpes the website searching for specific keywords inputed, to return advertisment links based on the keyword(S). The links are opened and specific data are extracted and stored in a csv File

## Tools Used

[Pyhton 3.7.5](https://www.python.org/ftp/python/3.7.5/python-3.7.5.exe).

[VSCode](https://code.visualstudio.com/download)

[Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Installation

KIJIJI AUTOBOT is a desktop application developed using python programming language and tkinter GUI framework, the following steps will guide you on how to setup and run it locally.

- STEP 1: DOWNLOAD OR PULL KIJIJI-AUTOBOT FOLDER
- STEP 2: OPEN TERMINAL AND CD INTO KIJI-AUTOBOT FOLDER

```bash
cd ...../~KIJI-AUTOBOT_folder~/
```

- STEP 3: CREATE VIRTUAL ENVIRONMENT FOLDER
- first install virtualenv

```bash
pip install virtualenv
```

- Then run the below command

```bash
virtualenv env
```

- activate virtual environment

```bash
cd venv/Scripts
```

```bash
activate
```

```bash
cd ../../
```

- STEP 4: INTSALL REQUIREMNTS.TXT FILE

```bash
pip install -r requirements.txt
```

- STEP 5: START PYHTON SERVER LOCALLY

```bash
cd src/
```

```bash
pyhton start.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

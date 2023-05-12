# ocrWebApp
This is a basic application for OCR using FastAPI as Backend framework. This contains a basic visualization layer in JS, HTML and CSS for easy visualization

## cloning the repo

```
git clone https://github.com/johanpina/ocrWebApp.git
cd ocrWebApp/
```


## Prerequisites

```
sudo apt install tesseract-ocr
sudo apt-get install tesseract-ocr-spa

```

## Virtual environment creation

First we have to create an activate the virtual environment


```
python3 -m venv .env
source .env/bin/activate

```

## Python packages installation 

```
pip install -r requirements.txt

```


## Server Execution

```
uvicorn main:app --reload

```


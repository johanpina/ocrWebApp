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
sudo apt-get install cifs-utils
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

## Server Shared ImageFolder linux2windows configuration
```
mkdir imagefolder/      # This is to mount the shared folder in this local route
chown -R 0777 imagefolder/   # Give permission for read/write to each user
sudo mount -t cifs //xxx.xxx.xxx.xx/folder_path /abs_route/to/image_folder -o username=domain_username,password=domain_passwd,domain=DomainOfEnterprise,vers=3.0
```

## Configurate to mount disk always while starting server

```
sudo nano /etc/fstab    #abrimos este archivo y agregamos la siguiente linea al final

//<dirección-ip-del-servidor>/<nombre-de-la-carpeta-compartida> /mnt/compartido cifs username=<wind_username>,password=<wind_password>,domain=<PeopleDomain>,uid=<id-de-usuario>,gid=<id-de-grupo>,iocharset=utf8,file_mode=0777,dir_mode=0777 0 0
```

para obtener el id de usuario:

```
id -u username
```

Para obtener el id de grupo:

```
groupP = $(id -gn)
getent group $(groupP) | cut -d: -f3
```

Ejecutamos los siguientes códigos

```
sudo mount -a
sudo reboot
```


# Deploy as service

```
sudo nano /etc/systemd/system/myapp.service
```

Editar el archivo con esta informacion

```
[Unit]
Description=Application description
After=network.target

[Service]
User=administrador
WorkingDirectory=/home/usr/myapp
ExecStart=/bin/bash -c "source /home/usr/myapp/.env/bin/activate && /home/usr/myapp/.env/bin/uvicorn main:app --host 0.0.0.0 --port 8000"
Restart=always

[Install]
WantedBy=multi-user.target
```

-Save Our file-
ExecStart first execute the venv activation and then the app deployment with uvicorn

Configurate the environment and install pip dependencies with requirements.txt
# Reload the systemd configuration

sudo systemctl daemon-reload
sudo systemctl restart myapp.service
sudo systemctl status myapp.service
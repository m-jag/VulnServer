# VulnServer
Trying to make a python server to host applications for a GDB class that I'm teaching.
The idea is to have something similar to an interactive CTF platform where students can 
send requests to the python server, which will get parsed there and then passed on to an 
underlying C/C++ application that has been dockerized.

Desired Features:
- Simple Webpages/CSS
- Spin-up docker containers to run the different labs/examples
    -  Pass info from client requests to docker containers
- Provide dump files for students to debug

TODO:
- Accounts
- Docker Integration
    - Spin up containers
    - Link user input to docker and back
- Share coredump files
- Write some sample applications, e.g. common buffer overflows, etc.

## Install
```bash
pip3 install docker
```

## Run
```bash
python3 main.py
```

# Credit
The base server code was modified from here. I like the simplicity, which makes it easier to secure hopefully.

Modified from:
https://medium.com/@andrewklatzke/creating-a-python3-webserver-from-the-ground-up-4ff8933ecb96
https://medium.com/@andrewklatzke/building-a-python-webserver-from-the-ground-up-part-two-c8ca336abe62

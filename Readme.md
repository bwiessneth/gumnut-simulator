# Gumnut Softcore Simulator

Requires python3.4


## Virtual environment

To ensure a persistent and encapsulated environment over several machines 
create a virtual environment with the following commands:

```bash
sudo apt-get install python-virtualenv
virtualenv env -p python3.4
source env/bin/activate
pip install -r requirements.txt
deactivate
```

## Tests

In order to run the tests call the following from the repository's top-level 
directory:

```bash
source env/bin/activate
nosetest -v
deactivate
```
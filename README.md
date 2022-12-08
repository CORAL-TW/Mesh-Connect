# Mesh Connect

## Installation
### Clone to your project
`git clone https://github.com/CoralSense/Mesh-Connect.git`

### Library Setup
pip3 install -r requirements.txt

### CDB Profile Setup
Copy your main Mesh CDB file to `Mesh-Connect/database/` folder

#### More CDB Profiles
Please put other CDB files in `Mesh-Connect/database/bullpen`

## Sample
### Load the main CDB file
```python
from mesh import MeshNetworkManager
MeshNetworkManager().load()	# load Sample1.json
```

### Save
```python
from mesh import MeshNetworkManager
MeshNetworkManager().save()
```

### Swap
```python
from mesh import MeshNetworkManager
try:
    MeshNetworkManager().swap(name='Sample2')	# swap to Sample2.json
except Exception as err:
    print(err)
```

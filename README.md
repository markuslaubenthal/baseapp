# BaseApp

BaseApp is a Python application framework designed to facilitate the creation and management of routines and services. It provides a structured way to define, discover, and execute routines and services with support for CLI integration.

## Features

- Fast bootstrapping of parameterized scripts
- Routine and Service discovery
- Parameter management with environment variable support
- CLI integration using click and click-shell
- (WIP) Logging support with configurable log levels and destinations
- Graceful shutdown of routines and services

## Roadmap

- Add a web interface to manage routines and services.
- Refactor the logging section completely.
- Refactor how executors work and how the app communicates with different components.
- Add nested Commands
- More

## Installation

To install the baseapp package with pip:

```
pip install -i https://gitlab.laubenthal.me/api/v4/projects/7/packages/pypi/simple baseapp
```

The package is currently only available on my public gitlab, but will be soon available in the default PyPI.

## Usage

### Implementing Routines and Services

To use BaseApp, you need to implement your own routines and services in the `routines` and `services` directories respectively. Here is an example of how to implement a routine:

```python
# start.py
from baseapp import BaseApp
app = BaseApp("MyApp")
app.start()
```


```python
# routines/MyRoutine.py
from baseapp import BaseRoutine
from baseapp import Parameter

class MyRoutine(BaseRoutine):
    name = "MyRoutine"
    
    param1 = Parameter[int]("param1", default=1).env("PARAM1")
    param2 = Parameter[int]("param2", default=2).env("PARAM2")
    
    def run(self):
        result = self.param1 + self.param2
        print(f"Result: {result}")
```

The parameters can be set as CLI arguments with:

```sh
python start.py --param1 val --param2 val
```

They can alternatively be retrieved from the environment variables ```PARAM1```, ```PARAM2```respectively.

By default the application will try to read the .env file in the working directory and get the environment variables. If the parameters are set via CLI parameters, they will override the environment variables. If neither is set, the default value will be used.

And here is an example of how to implement a service:

```python
# services/MyService.py
from baseapp import BaseService
from baseapp import Parameter
import time

class MyService(BaseService):
    name = "MyService"
    
    def run(self):
        while not self.stopEvent.is_set():
            print("Service is running")
            time.sleep(1)
```

### Starting the Application
To start the application, create a new Python file, import the BaseApp class, and execute it:

```python
# start.py
from baseapp import BaseApp
import logging

if __name__ == "__main__":
    app = BaseApp()
    app.setLogLevel(logging.WARNING)
    app.config["routines_directories"] = ["routines"]
    app.config["services_directories"] = ["services"]
    app.start()
```

Run the application in shell mode:
```sh
python start.py
```

```sh
python start.py routines run ROUTINE_NAME --parameter value
python start.py services run SERVICE_NAME --parameter value
```

Example:

```sh
python start.py routines run my_routine --param1=5 --param2=10
```

### Parameters

Supported Parameter types are:
- int
- str
- bool
- any other primitive datatypes

Parameters can be given a name to set in the CLI.
If no name is provided, the variable name will be transformed to camel_case and used as the name.

Booleans can be activated in the CLI command
```python
class MyRoutine(BaseRoutine):
    name = "MyRoutine"
    
    myBoolean = Parameter[bool]("myBoolean")
    myOtherBoolean = Parameter[bool]()
    varWithoutName = Parameter[str]()
    a_float = Parameter[float]()
```

```bash
python start.py my_routine \
    --myBoolean \
    --my_other_boolean \
    --var_without_name="VALUE" \
    --a_float=7.5
```

### Configuration

Configuration can be set through environment variables or by modifying the `BaseApp` class in `start.py`.

Example:

```python
app = BaseApp(
    enableRoutineDiscovery=True,
    enableServiceDiscovery=True,
    logDestination="logs/"
)
app.config["routines_directories"] = ["routines"]
app.config["services_directories"] = ["services"]
```

### Logging

Logs are stored in the directory specified by the `logDestination` configuration. By default, logs are stored in the `logs` directory.

## Testing

To run the tests, use `pytest`:

```sh
pytest
```

## License

This project is licensed under the MIT License.
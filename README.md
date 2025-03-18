# BaseApp

BaseApp is a Python application framework designed to facilitate the creation and management of routines and services. It provides a structured way to define, discover, and execute routines and services with support for CLI integration.

## Features

- Routine and Service discovery
- Parameter management with environment variable support
- CLI integration using Click
- Logging support with configurable log levels and destinations
- Graceful shutdown of routines and services

## Installation

To install the dependencies, use `poetry`:

```sh
poetry install
```

## Usage

### Implementing Routines and Services

To use BaseApp, you need to implement your own routines and services in the `routines` and `services` directories respectively. Here is an example of how to implement a routine:

```python
# routines/MyRoutine.py
from baseapp.registry.routines import BaseRoutine
from baseapp.registry import Parameter

class MyRoutine(BaseRoutine):
    name = "MyRoutine"
    
    param1 = Parameter[int]("param1", default=1).env("PARAM1")
    param2 = Parameter[int]("param2", default=2).env("PARAM2")
    
    def run(self):
        result = self.param1 + self.param2
        print(f"Result: {result}")
```

And here is an example of how to implement a service:

```python
# services/MyService.py
from baseapp.registry.services import BaseService
from baseapp.registry import Parameter
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
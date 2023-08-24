import pytest
from baseapp import BaseApp

class ChildApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
@pytest.fixture
def childApp():
    app = ChildApp(
        enableRoutineDiscovery=True,
        enableServiceDiscovery=True
    )
    
    app.config["routines_directories"] = ["tests/routines/fixtures"]
    app.config["services_directories"] = ["tests/services/fixtures"]
    
    app.init()
    return app
    
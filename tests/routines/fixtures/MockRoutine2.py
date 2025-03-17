from baseapp.registry.routines import BaseRoutine
 
class MockRoutine2(BaseRoutine):
    """This is a Mock Routine"""
    
    name = "MockRoutine2"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
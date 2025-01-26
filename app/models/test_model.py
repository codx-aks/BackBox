from app.models.base_model import BaseModel

class Test(BaseModel):
    def __init__(self):
        super().__init__()
    
    # Add any Test-specific methods here
    def custom_test_method(self):
        return "Custom test method"
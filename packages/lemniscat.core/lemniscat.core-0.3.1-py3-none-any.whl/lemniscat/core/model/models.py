from dataclasses import dataclass
from typing import List

@dataclass
class Meta:
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}: {self.version}'

@dataclass
class TaskResult:
    name: str
    status: str
    errors: List[str]
       
@dataclass
class VariableValue:
    sensitive: bool
    value: object
     
    def __init__(self, value: object, sensitive: bool = False) -> None:
        if(isinstance(value, dict) and value.__contains__('value') and value.__contains__('sensitive')):
            self.value = value['value']
            self.sensitive = value['sensitive']
        else:
            self.value = value
            self.sensitive = sensitive

    def __str__(self) -> str:
        if(self.sensitive):
            return '********'
        return str(self.value)
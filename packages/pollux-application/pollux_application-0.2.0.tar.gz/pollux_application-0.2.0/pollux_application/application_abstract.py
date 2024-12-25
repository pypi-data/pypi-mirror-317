from abc import ABC, abstractmethod


# from pollux_framework.framework.boot_plant import setup


class ApplicationAbstract(ABC):
    """Abstract class fpr application"""

    def __init__(self):
        self.parameters = dict()
        self.inputs = dict()
        self.outputs = dict()

    def set_input(self, inputs):
        """Function to set the input"""
        self.inputs = inputs

    def get_input(self):
        """Function to get the input"""
        return self.inputs

    def get_output(self):
        """Function to get the output"""
        return self.outputs

    @abstractmethod
    def init_parameters(self, inputs):
        """Abstract function to initialize the model parameters"""
        pass

    @abstractmethod
    def calculate(self, inputs):
        """Abstract function to calculate the model"""
        pass

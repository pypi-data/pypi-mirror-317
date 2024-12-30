class Transformation:

    def __init__(self):
        pass

    def transform(self, value) -> bool:
        pass


class Verification:

    def __init__(self):
        pass

    def verify(self, value) -> bool:
        pass


class InputDataManager:
    pass


class DraftDataManager:
    def list(self):
        pass

    def set(self):
        pass

    def remove(self):
        pass


class OutputDataManager:
    def list(self):
        pass

    def set(self):
        pass

    def remove(self):
        pass


class DataProcessingStage:
    name: str

    def __init__(self, name, folder_location):
        self.name = name
        self.folder_location = folder_location
        self.input_data = InputDataManager()
        self.output_data = OutputDataManager()

    def status(self):
        pass

    def goal(self):
        pass

    def process(self, value) -> bool:
        pass

    def seed(self):
        pass

    def finalize(self):
        pass

    def input(self):
        pass

    def output(self):
        pass

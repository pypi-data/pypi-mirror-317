class Config:
    def __init__(self, mock_name_pattern: str):
        self.mock_name_pattern = mock_name_pattern


class DefaultConfig(Config):
    def __init__(self, mock_name_pattern: str = r"(?=.*mock)(?!.*grpc)"):
        super().__init__(mock_name_pattern=mock_name_pattern)

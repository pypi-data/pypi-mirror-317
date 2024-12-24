class CompareFuncNotFoundError(Exception):
    def __init__(self, incorrect_func: str, *args):
        super().__init__(f"compare func {incorrect_func} not found. Compare func must be one of: "
                         f"'startswith', "
                         f"'equal', "
                         f"'endswith', 'in'", *args)

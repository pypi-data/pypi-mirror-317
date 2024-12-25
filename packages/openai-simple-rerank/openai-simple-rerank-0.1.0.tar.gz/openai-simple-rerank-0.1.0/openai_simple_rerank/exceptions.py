__all__ = [
    "NoneValueError",
    "RerankNoneValueError",
    "GetRerankScoresError",
]

class NoneValueError(RuntimeError):
    """不允许None值。"""

    def __init__(self, *args, **kwargs):
        args = args or ["不允许None值。"]
        super().__init__(*args, **kwargs)

class RerankNoneValueError(NoneValueError):
    """None值无法参与重排。"""

    def __init__(self, *args, **kwargs):
        args = args or ["None值无法参与重排。"]
        super().__init__(*args, **kwargs)

class GetRerankScoresError(RuntimeError):
    """获取rerank得分失败。"""

    def __init__(self, *args, **kwargs):
        args = args or ["获取rerank得分失败。"]
        super().__init__(*args, **kwargs)

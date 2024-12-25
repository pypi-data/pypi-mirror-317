__all__ = [
    "GetTextEmbeddingsError",
]


class GetTextEmbeddingsError(RuntimeError):
    """获取文本向量失败。"""

    def __init__(self, *args, **kwargs):
        args = args or ["获取文本向量失败。"]
        super().__init__(*args, **kwargs)

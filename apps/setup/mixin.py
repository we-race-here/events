

class GridSizeMixin:
    def __init__(self, *args, grid_size=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size or "w-full"

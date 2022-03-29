class BaseController(object):
    """
    """
    def __init__(self, model, view):
        super(BaseController, self).__init__()
        self.model = model
        self.view = view
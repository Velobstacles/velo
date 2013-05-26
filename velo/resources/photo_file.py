from . import meta


class Collection(meta.Resource):

    def show(self):
        return self.ancestor['media'].model.get_content_grid_out()

import royal


class Collection(royal.Resource):

    def show(self):
        return self.ancestor['media'].model.get_content_grid_out()

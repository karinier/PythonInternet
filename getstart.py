import flask, flask.view
app=flask.Flask(__name__)
class views(flask.view.MethodView):
    def get(self):
        return "Hello World!"
    app.add_url_rule ( '/ ', view_func=view.asview('main'))
app.debug=TRUE
app.run()
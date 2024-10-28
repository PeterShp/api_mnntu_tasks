import flask
import flask_restful

app = flask.Flask(__name__)
api = flask_restful.Api(app)

items = []

class Item(flask_restful.Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return flask.jsonify(item)
        return {'message': 'Item not found'}, 404
    
    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]
        return {'message': 'Item deleted'}
    
class ItemList(flask_restful.Resource):
    def post(self):
        data = flask.request.get_json()
        print(data)
        new_item = {
            'name': data['name'],
            'price': data['price']
        }
        items.append(new_item)
        return flask.jsonify(new_item)
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')

if __name__ == '__main__':
    app.run(debug=True)

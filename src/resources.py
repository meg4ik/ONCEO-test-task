from flask import request, jsonify, abort, Response

from .database.models import Order, Item, OrderItem, AddressNode, User
from src import db, app, jsonrpc
from flask_login import login_required
import json
from flask_login import login_user

@app.route('/create_order', methods=['POST'])
def create_order():
    data = json.loads(request.data)

    new_order = Order()

    try:

        items = data.get('items')
        for item_data in items:
            item_id = item_data.get('id')
            item_count = item_data.get('count', 1)

            item = Item.query.get(item_id)
            if item:
                order_item = OrderItem(item_id=item.id, order=new_order, count=item_count)
                new_order.order_item_to.append(order_item)
            else:
                return jsonify({'error': f'Item with id {item_id} not found'}), 400

        addresses = data.get('addresses')
        prev_node = None

        for address in addresses:
            current_node = AddressNode(address=address, order=new_order, prev_node=prev_node)
            db.session.add(current_node)
            db.session.commit()

            prev_node = current_node.id

        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/get_order/<string:order_uuid>', methods=['GET'], endpoint='get_specific_order')
# @jsonrpc.method('App.index')
@login_required
def create_order(order_uuid):
    order = Order.query.filter_by(uuid=order_uuid).first()

    if order is None:
        abort(404, description="Order not found")

    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    items_info = []
    for order_item in order_items:
        item = Item.query.get(order_item.item_id)
        if item:
            items_info.append({
                'id': item.id,
                'title': item.title,
                'color': item.color,
                'weight': item.weigth,
                'price': item.price,
                'count': order_item.count
            })

    adresses = []
    node = AddressNode.query.filter_by(order_id=order.id, prev_node=None).first()
    if node:
        adresses.append(node.address)
        while True:
            next_node = AddressNode.query.filter_by(order_id=order.id, prev_node=node.id).first()
            if not next_node:
                break
            adresses.append(next_node.address)
            node = next_node
    
    response = {
        'order_id': order.id,
        'order_uuid': order.uuid,
        'order_status': order.status.value,
        'created_date': order.created_date.isoformat(),
        'items': items_info,
        'adresses':adresses
    }
    response_json = json.dumps(response, ensure_ascii=False)
    response = Response(response_json, content_type="application/json; charset=utf-8")
    return response

@jsonrpc.method('App.login')
def login(username: str, password: str) -> str:
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return "Done"

    return "Wrong"
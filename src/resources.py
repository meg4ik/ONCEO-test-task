from flask import request, jsonify

from .database.models import Order, Item, OrderItem, AddressNode
from src import db, app

import json


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

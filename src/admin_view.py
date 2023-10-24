import uuid

# from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
# from flask import request, redirect, url_for
# from flask_security import current_user

class ItemModelView(ModelView):
    column_list = ['id', 'title', 'color', 'weigth', 'price']

class AdressModelView(ModelView):
    column_list = ['id', 'address', 'prev_node', 'order_id']
    
class OrderModelView(ModelView):

    column_list = ['id', 'uuid', 'created_date', 'status']

    def create_form(self, obj=None):
        form = super().create_form(obj=obj)
        new_uuid = str(uuid.uuid4())
        form.uuid.data = new_uuid
        return form
    
    def on_model_change(self, form, model, is_created):
        if not form.uuid.data:
            model.uuid = str(uuid.uuid4())

class OrderItemModelView(ModelView):

    column_list = ['id', 'uuid', 'item_id', 'order_id', 'count']

    def create_form(self, obj=None):
        form = super().create_form(obj=obj)
        new_uuid = str(uuid.uuid4())
        form.uuid.data = new_uuid
        return form
    
    def on_model_change(self, form, model, is_created):
        if not form.uuid.data:
            model.uuid = str(uuid.uuid4())
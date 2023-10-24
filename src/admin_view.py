import uuid

from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import flash, redirect, request, url_for

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        
        return redirect(url_for('login', next=request.url))
    

class ItemModelView(AuthenticatedModelView):
    column_list = ['id', 'title', 'color', 'weigth', 'price']


class AdressModelView(AuthenticatedModelView):
    column_list = ['id', 'address', 'prev_node', 'order_id']

    
class OrderModelView(AuthenticatedModelView):

    column_list = ['id', 'uuid', 'created_date', 'status']

    def create_form(self, obj=None):
        form = super().create_form(obj=obj)
        new_uuid = str(uuid.uuid4())
        form.uuid.data = new_uuid
        return form
    
    def on_model_change(self, form, model, is_created):
        if not form.uuid.data:
            model.uuid = str(uuid.uuid4())

class OrderItemModelView(AuthenticatedModelView):

    column_list = ['id', 'uuid', 'item_id', 'order_id', 'count']

    def create_form(self, obj=None):
        form = super().create_form(obj=obj)
        new_uuid = str(uuid.uuid4())
        form.uuid.data = new_uuid
        return form
    
    def on_model_change(self, form, model, is_created):
        if not form.uuid.data:
            model.uuid = str(uuid.uuid4())

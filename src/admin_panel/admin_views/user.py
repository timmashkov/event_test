from sqladmin import ModelView

from infrastructure.database.models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.login,
        User.email,
        User.age,
        User.phone_number,
        User.registered_at,
    ]
    column_searchable_list = [User.login]
    column_sortable_list = [User.registered_at]
    column_default_sort = [(User.age, True), (User.id, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

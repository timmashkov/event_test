from sqladmin import ModelView

from infrastructure.database.models import Company


class CompanyAdmin(ModelView, model=Company):
    column_list = [
        Company.id,
        Company.name,
        Company.bio,
        Company.phone_number,
        Company.address,
        Company.email,
    ]
    column_searchable_list = [Company.name]
    column_sortable_list = [Company.address]
    column_default_sort = [(Company.phone_number, True), (Company.email, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

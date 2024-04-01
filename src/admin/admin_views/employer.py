from sqladmin import ModelView

from infrastructure.database.models import Employer


class EmployerAdmin(ModelView, model=Employer):
    column_list = [
        Employer.id,
        Employer.user_id,
        Employer.first_name,
        Employer.last_name,
        Employer.middle_name,
        Employer.position,
        Employer.exp,
        Employer.company_id,
        Employer.bio,
    ]
    column_searchable_list = [Employer.first_name]
    column_sortable_list = [Employer.exp]
    column_default_sort = [(Employer.position, True), (Employer.last_name, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

from sqladmin import ModelView

from infrastructure.database.models import Teacher


class TeacherAdmin(ModelView, model=Teacher):
    column_list = [
        Teacher.id,
        Teacher.user_id,
        Teacher.first_name,
        Teacher.last_name,
        Teacher.middle_name,
        Teacher.degree,
        Teacher.exp,
        Teacher.course_id,
    ]
    column_searchable_list = [Teacher.first_name]
    column_sortable_list = [Teacher.degree]
    column_default_sort = [(Teacher.exp, True), (Teacher.last_name, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

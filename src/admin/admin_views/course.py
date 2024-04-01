from sqladmin import ModelView

from infrastructure.database.models import Course


class CourseAdmin(ModelView, model=Course):
    column_list = [
        Course.id,
        Course.title,
        Course.price,
        Course.description,
        Course.duration,
        Course.company_id,
    ]
    column_searchable_list = [Course.title]
    column_sortable_list = [Course.price]
    column_default_sort = [(Course.duration, True), (Course.id, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

from sqladmin import ModelView

from infrastructure.database.models import Feedback


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [
        Feedback.id,
        Feedback.title,
        Feedback.body,
        Feedback.created_at,
        Feedback.author_id,
    ]
    column_searchable_list = [Feedback.title]
    column_sortable_list = [Feedback.created_at]
    column_default_sort = [(Feedback.id, True), (Feedback.body, False)]

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True

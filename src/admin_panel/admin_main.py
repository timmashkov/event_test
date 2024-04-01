from sqladmin import Admin

from admin_panel.admin_auth import auth_backend
from admin_panel.admin_views import (
    UserAdmin,
    CourseAdmin,
    EmployerAdmin,
    CompanyAdmin,
    TeacherAdmin,
    FeedbackAdmin,
)
from application.server import ApiServer
from infrastructure.database.session import vortex

admin = Admin(ApiServer.app, vortex.engine, authentication_backend=auth_backend)


admin.add_view(UserAdmin)
admin.add_view(CourseAdmin)
admin.add_view(EmployerAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(TeacherAdmin)
admin.add_view(FeedbackAdmin)

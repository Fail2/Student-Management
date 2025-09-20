{
    'name': 'Student Management',
    'version': '1.0.0',
    'category': 'Education',
    'summary': 'Manage students, courses and enrollments',
    'description': """
        Student Management System
        =========================
        This module allows you to:
        * Manage students with basic information
        * Manage courses with credits
        * Handle many-to-many enrollment relationships
        * Generate reports of student enrollments
    """,
    'author': 'Malay Chakma',
    'website': 'https://fail2.github.io/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
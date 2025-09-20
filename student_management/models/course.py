from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Course(models.Model):
    """Course model to store course information"""
    
    _name = 'student.management.course'
    _description = 'Student Management - Course'
    _rec_name = 'name'
    
    # Basic Course Information
    name = fields.Char(
        string='Course Name',
        required=True,
        help='Full name of the course'
    )
    
    code = fields.Char(
        string='Course Code',
        required=True,
        help='Unique course code (e.g., CS101)',
        copy=False
    )
    
    credit = fields.Integer(
        string='Credits',
        required=True,
        default=2,
        help='Number of credits for this course'
    )
    
    description = fields.Text(
        string='Description',
        help='Detailed course description'
    )
    
    # Many-to-many relationship with students
    student_ids = fields.Many2many(
        comodel_name='student.management.student',
        relation='student_course_rel',
        column1='course_id',
        column2='student_id',
        string='Enrolled Students',
        help='Students enrolled in this course'
    )
    
    # Computed field to count enrolled students
    student_count = fields.Integer(
        string='Number of Students',
        compute='_compute_student_count',
        help='Total number of enrolled students'
    )
    
    # Active field to archive/unarchive courses
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Uncheck to archive the course'
    )
    
    @api.depends('student_ids')
    def _compute_student_count(self):
        """Calculate number of enrolled students"""
        for record in self:
            record.student_count = len(record.student_ids)
    
    @api.constrains('credit')
    def _check_credit_positive(self):
        """Ensure credits are positive"""
        for record in self:
            if record.credit <= 0:
                raise ValidationError('Credits must be greater than zero.')
    
    @api.constrains('code')
    def _check_unique_code(self):
        """Ensure course code is unique"""
        for record in self:
            if record.code:
                existing = self.search([
                    ('code', '=', record.code),
                    ('id', '!=', record.id),
                    ('active', 'in', [True, False])
                ])
                if existing:
                    raise ValidationError(f'Course code {record.code} already exists!')
    
    def action_view_students(self):
        """Action to show enrolled students"""
        return {
            'name': f'Students in {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'student.management.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.student_ids.ids)],
            'context': {'default_course_ids': [(6, 0, [self.id])]},
        }
    
    def name_get(self):
        """Custom display name format: [CODE] Name"""
        result = []
        for record in self:
            name = f'[{record.code}] {record.name}'
            result.append((record.id, name))
        return result
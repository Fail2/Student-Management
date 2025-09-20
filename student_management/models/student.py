from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    """Student model to store student information"""
    
    # Technical name of the model (used in database)
    _name = 'student.management.student'
    
    # Description shown in technical menus
    _description = 'Student Management - Student'
    
    # Field to use as record name/title
    _rec_name = 'name'
    
    # Basic Information Fields
    name = fields.Char(
        string='Student Name', 
        required=True,
        help='Full name of the student'
    )
    
    email = fields.Char(
        string='Email Address',
        required=True,
        help='Student email address for communication'
    )
    
    roll_no = fields.Char(
        string='Roll Number',
        required=True,
        help='Unique student roll number',
        copy=False  # Don't copy this field when duplicating record
    )
    
    department = fields.Char(
        string='Department',
        required=True,
        help='Academic department of the student'
    )
    
    # Many-to-many relationship with courses
    course_ids = fields.Many2many(
        comodel_name='student.management.course',  # Related model
        relation='student_course_rel',             # Database table name
        column1='student_id',                      # This model's column
        column2='course_id',                       # Other model's column
        string='Enrolled Courses',
        help='Courses in which student is enrolled'
    )
    
    # Computed field to count enrolled courses
    course_count = fields.Integer(
        string='Number of Courses',
        compute='_compute_course_count',
        help='Total number of enrolled courses'
    )
    
    # Computed field for total credits
    total_credits = fields.Integer(
        string='Total Credits',
        compute='_compute_total_credits',
        help='Total credits from all enrolled courses'
    )
    
    @api.depends('course_ids')
    def _compute_course_count(self):
        """Calculate number of enrolled courses"""
        for record in self:
            record.course_count = len(record.course_ids)
    
    @api.depends('course_ids.credit')
    def _compute_total_credits(self):
        """Calculate total credits from all enrolled courses"""
        for record in self:
            record.total_credits = sum(course.credit for course in record.course_ids)
    
    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format"""
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError('Please enter a valid email address.')
    
    @api.constrains('roll_no')
    def _check_unique_roll_no(self):
        """Ensure roll number is unique"""
        for record in self:
            if record.roll_no:
                existing = self.search([
                    ('roll_no', '=', record.roll_no),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(f'Roll number {record.roll_no} already exists!')
    
    def action_view_courses(self):
        """Action to show enrolled courses (Bonus feature)"""
        return {
            'name': f'Courses for {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'student.management.course',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.course_ids.ids)],
            'context': {'default_student_ids': [(6, 0, [self.id])]},
        }
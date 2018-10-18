# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def send_birthday_wish(self):
        today_date = datetime.today().date()
        for employee in self.env['hr.employee'].search([]):
            _logger.info('%s, birthday: %s, today: %s', employee, employee.birthday, today_date.day)
            if employee.birthday:
                emp_birthdate = datetime.strptime(str(employee.birthday), '%Y-%m-%d').date()
                if today_date.day == emp_birthdate.day and today_date.month == emp_birthdate.month:
                    template_id = self.env.ref('fl_birthday_wish.email_birthday_wishes_employee_template')
                    template_id.send_mail(employee.id, force_send=True)
                    employee.message_post(body='Birthday message sent!')
        for partner in self.env['res.partner'].search([]):
            if partner.birthday:
                cust_birthdate = datetime.strptime(str(partner.birthday), '%Y-%m-%d').date()
                if today_date.day == cust_birthdate.day and today_date.month == cust_birthdate.month:
                    template_id = self.env.ref('fl_birthday_wish.email_birthday_wishes_partner_template')
                    template_id.send_mail(partner.id, force_send=True)
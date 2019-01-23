# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _



class payment_request(models.Model):
    _description = 'Request For Money Approval'
    _name = 'account.payment.request'
    _inherit = ['mail.thread']
    
    
    
    #Method For login user == employee
    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    
    #Relational Fields
    employee_id = fields.Many2one('hr.employee', string='Employee Name',default=_default_employee,index=True, readonly=True, required=True)
    currency_id = fields.Many2one("res.currency")
    journal_id = fields.Many2one("account.journal", string="Payment Journal", domain=[('type', 'in', ('bank', 'cash'))])
    journ_id = fields.Char(string="Use This Journal", compute="update_journal")
   
    
    
    
    #Fields 
    request_date = fields.Datetime("Request Date")
   
    pay_to = fields.Selection([
        ('vendor', 'Vendor'),
        ('petty', 'Petty Cash')], default='petty')
    payment_amount = fields.Monetary("Required Amount", required=True)
    partner_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier', '=', True)])
    name = fields.Char("Request Number")
    description  = fields.Char("Description", required=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('refuse', 'Refused'),
        ('approve', 'To Approve'),
        ('validate', 'Approved')], string="Status", default='draft')
    
    @api.model
    def create(self, values):
        record = super(payment_request, self).create(values)
        record['name'] = self.env['ir.sequence'].next_by_code('account.payment.request') or _('New')
        return record
    
    
    #Change States
    @api.multi
    def action_cancel(self):
        self.state = 'cancel'
        
    @api.multi
    def action_draft(self):
        self.write({
            'state': 'approve',
        })
        message_body = """
            <p>Dear """ + self.employee_id.parent_id.name + """,</p>
            <p>A Payment request # """ + self.name + """ has been sent to you for approval. </P><br/>
             <p>You can view the request by clicking the following link: </p>
             <p>
             <a href=""" + self.generate_url() + """ style="padding: 5px 10px; color: #FFFFFF; text-decoration: none;
                    background-color: #875A7B; border: 1px solid #875A7B; border-radius: 3px; text-align: center">
                    View Request
                </a>
            </p><br/>
            <p>Regards,</p>
            <p>""" + self.employee_id.name + """</p>"""

        template_obj = self.env['mail.mail']
        template_data = {
                       'subject': self.name + ' - Request for Payment Approval',
                       'body_html': message_body,
                       'email_from': self.employee_id.work_email,
                       'email_to': self.employee_id.parent_id.work_email,
                       }
        template_id = template_obj.create(template_data)
        if template_id:
            template_obj.send(template_id)
        
        
    @api.multi
    def action_refuse(self):
        self.state = 'refuse'
        
    @api.multi
    def action_approval(self):
        self.write({
            'state': 'validate',
        })

    @api.depends('journal_id')
    def update_journal(self):
        for rec in self:
            self['journ_id'] = rec.journal_id.name
            
            
    def generate_url(self):
        """
        Build the URL to the record's form view.
          - Base URL + Database Name + Record ID + Model Name

        :param self: any Odoo record browse object (with access to env, _cr, and _model)
        :return: string with url
        """
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        if base_url and base_url[-1:] != '/':
            base_url += '/'
        db = self._cr.dbname
        return "{}web?db={}#id={}&view_type=form&model={}".format(base_url, db, self.id, self._name)


    
    
        
    
   

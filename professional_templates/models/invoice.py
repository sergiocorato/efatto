# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

try:
    from num2words import num2words
except ImportError:
    raise ValidationError('In order to proceed, please install python module called `num2words`.\n How to install the latest version in Linux/UNIX or Windows System:\n 1. Download it from https://github. com/savoirfairelinux/num2words \n 2. Unzip the downloaded file\n 3. Change directory to the unziped `num2words` folder  and run this command: "python setup.py install"\n')

class professional_templates(models.Model):
	_inherit=["account.invoice"]

	@api.model
	def _default_template(self):
	    if not self.env.user.company_id.template_invoice:
		def_tpl = self.env['ir.ui.view'].search([('name', 'like', 'Invoice Template' ), ('type', '=', 'qweb')], order='id asc', limit=1)
                self.env.user.company_id.write({'template_invoice': def_tpl.id})
	    return self.env.user.company_id.template_invoice or self.env.ref('account.report_invoice_document')
	

	project_title = fields.Char('Project Title', help="The title of your customer project or work you are doing for your customer")	
	
        invoice_logo = fields.Binary("Logo", attachment=True,
             help="This field holds the image used as logo for the invoice, if non is uploaded, the default logo define in the copmany settings will be used")
	template_id = fields.Many2one('ir.ui.view', 'Invoice Template', default=_default_template,required=False, 
		domain="[('type', '=', 'qweb'), ('name', 'like', 'Invoice Template' )]")
        odd = fields.Char('Odd parity Color', size=7, required=True, default= lambda self: self.env.user.company_id.odd , help="The background color for Odd lines in the invoice")	
        even = fields.Char('Even parity Color', size=7, required=True, default=lambda self: self.env.user.company_id.even, help="The background color for Even lines in the invoice" )	
        theme_color = fields.Char('Theme Color', size=7, required=True, default=lambda self: self.env.user.company_id.theme_color, help="The Main Theme color of the invoice. Normally this\
			 should be one of your official company colors")	
        theme_txt_color = fields.Char('Theme Text Color', size=7, required=True, default=lambda self: self.env.user.company_id.theme_txt_color, 
			help="The Text color of the areas with theme color. This should not be the same the theme color")	
        text_color = fields.Char('Text Color', size=7, required=True, default=lambda self: self.env.user.company_id.text_color, help="The Text color of the invoice. Normally this\
			 should be one of your official company colors or default HTML text color")	
        name_color = fields.Char('Company Name Color', size=7, required=True, default=lambda self: self.env.user.company_id.name_color, help="The Text color of the Company Name. \
			Normally thisshould be one of your official company colors or default HTML text color")	
        cust_color = fields.Char('Customer Name Color', size=7, required=True, default=lambda self: self.env.user.company_id.cust_color, help="The Text color of the Customer Name. \
			Normally this should be one of your official company colors or default HTML text color")	
        header_font = fields.Selection([(x,str(x)) for x in range(1,51)], string="Header Font-Size(px):", default=lambda self: self.env.user.company_id.header_font, required=True)
        body_font = fields.Selection([(x,str(x)) for x in range(1,51)], string="Body Font-Size(px):", default=lambda self: self.env.user.company_id.body_font, required=True)
        footer_font = fields.Selection([(x,str(x)) for x in range(1,51)], string="Footer Font-Size(px):", default=lambda self: self.env.user.company_id.footer_font, required=True)
        font_family = fields.Char('Font Family:', default=lambda self: self.env.user.company_id.font_family, required=True)
        amount_words= fields.Char('Amount in Words:', help="The invoice total amount in words is automatically generated by the system..few languages are supported currently",                             compute='_compute_num2words')
        aiw_report = fields.Boolean('Show in report?', default=lambda self: self.env.user.company_id.aiw_report,  help="If you want to display the Invoice total in words in the report, then check this box")
        show_img = fields.Boolean('Display Product Image?', default = lambda self: self.env.user.company_id.show_img, help="Check this Box to display the product image in the PDF invoice report")

        @api.one
        def _compute_num2words(self):
            try:
                self.amount_words = (num2words(self.amount_total, lang=self.partner_id.lang) + ' ' + (self.currency_id.currency_name or '')).upper()
            except NotImplementedError:
                self.amount_words = (num2words(self.amount_total, lang='en') + ' ' + (self.currency_id.currency_name or '')).upper()


	##Override invoice_print method in original invoice class in account module
	@api.multi
	def invoice_print(self):
            """ Print the invoice and mark it as sent, so that we can see more
               easily the next step of the workflow
	       This Method overrides the one in the original invoice class
            """
            self.ensure_one()
            self.sent = True
            return self.env['report'].get_action(self, 'professional_templates.report_invoice')


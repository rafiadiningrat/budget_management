from odoo import _, api, fields, models

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountBudget(models.Model):
    _inherit = 'account.budget'

    
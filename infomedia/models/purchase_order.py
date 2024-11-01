from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    budget_status = fields.Selection([
        ('lolos', 'Lolos'),
        ('tlolos', 'Tidak Lolos')
    ], string='Budget Status', compute='_compute_budget_status', store=True)

    @api.depends('order_line', 'order_line.price_subtotal')
    def _compute_budget_status(self):
        for order in self:
            if order.check_budget(raise_exception=False):
                order.budget_status = 'lolos'
            else:
                order.budget_status = 'tlolos'

    def button_confirm(self):
        for order in self:
            if not order.check_budget(raise_exception=True):
                _logger.warning("Budget check failed for Purchase Order %s", order.name)
                raise UserError(_('Budget exceeded! Cannot confirm purchase order.'))
            return super(PurchaseOrder, self).button_confirm()

    def check_budget(self, raise_exception=True):
        self.ensure_one()
        AccountBudgetPost = self.env['account.budget.post']
        CrossoveredBudget = self.env['crossovered.budget']
        CrossoveredBudgetLines = self.env['crossovered.budget.lines']
        
        for line in self.order_line:
            budget_posts = AccountBudgetPost.search([
                ('account_ids', 'in', line.product_id.categ_id.property_account_expense_categ_id.id)
            ])
            _logger.info("Found %d budget post(s) for the product category", len(budget_posts))

            if not budget_posts:
                _logger.warning("No budget defined for category %s", line.product_id.categ_id.name)
                if raise_exception:
                    raise UserError(_('No budget defined for category %s. Please set a budget to proceed.') % line.product_id.categ_id.name)
                return False
            
            for budget_post in budget_posts:
                date_from = fields.Date.today().replace(month=1, day=1)
                date_to = fields.Date.today().replace(month=12, day=31)
            
                budget_lines = CrossoveredBudgetLines.search([
                    ('general_budget_id', '=', budget_post.id),
                    ('date_from', '>=', date_from),
                    ('date_to', '<=', date_to),
                    ('crossovered_budget_id.state', '=', 'validate')
                ])
                
                budgeted_amount = sum(budget_lines.mapped('planned_amount'))
                
                actual_amount = sum(self.env['account.move.line'].search([
                    ('account_id', 'in', budget_post.account_ids.ids),
                    ('date', '>=', date_from),
                    ('date', '<=', date_to),
                    ('move_id.state', '=', 'posted')
                ]).mapped('balance'))
                
                remaining_budget = budgeted_amount - actual_amount               
                if line.price_subtotal > remaining_budget:
                    _logger.warning("Budget exceeded for line %s. Price subtotal: %f, Remaining budget: %f",
                                    line.product_id.name, line.price_subtotal, remaining_budget)
                    return False
                else:
                    _logger.info("Budget check passed for line %s", line.product_id.name)
        return True
from odoo import fields, models


class MarkBlockedWizard(models.TransientModel):
    _name = "wizard.mark.blocked"
    _description = "Wizard mark blocked"

    note = fields.Char(required=True)

    def mark_blocked(self):
        rec_ids = self.env.context.get("active_ids", False)
        records = self.env[self.env.context["active_model"]].browse(rec_ids)
        for rec in records:
            rec.write(
                {
                    "blocked_note": self.note,
                    "is_blocked": True,
                }
            )

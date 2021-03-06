from odoo import models, api


class MailMail(models.Model):
    _inherit = "mail.mail"

    """
        Inherit mail.mail to deactivate a linked partner after a send.
    """

    @api.multi
    def _postprocess_sent_message(self, success_pids, failure_reason=False,
                                  failure_type='UNKNOWN'):
        for mail in self:
            partner_ids = mail.partner_ids
            for partner in mail.partner_ids:
                if partner.contact_type == "attached" and partner.active:
                    partner.toggle_active()

            # When we deactivate a partner, he is remove from the email.
            mail.write({"partner_ids": partner_ids})

        s = super()._postprocess_sent_message(
            success_pids, failure_reason, failure_type)
        return s

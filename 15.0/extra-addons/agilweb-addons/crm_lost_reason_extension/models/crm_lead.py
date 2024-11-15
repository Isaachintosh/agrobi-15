from odoo import models, fields, api, exceptions

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        # Busca o estágio "Perdido" baseado no nome
        perdido_stage = self.env['crm.stage'].search([('name', '=', 'Perdido')], limit=1)
        
        # Verifica se o estágio mudou para "Perdido" e se o motivo da perda não foi definido
        if self.stage_id == perdido_stage and not self.lost_reason:
            raise exceptions.UserError(
                'Você deve informar o motivo da perda antes de mover para o estágio "Perdido".'
            )

    @api.model
    def write(self, vals):
        stage_perdido = self.env['crm.stage'].search([('name', '=', 'Perdido')], limit=1)
        # Checa se a mudança de estágio é para "Perdido" sem definir um motivo de perda
        if 'stage_id' in vals and vals['stage_id'] == stage_perdido.id:
            for lead in self:
                # Garante que o motivo da perda está definido antes de mover para "Perdido"
                if not vals.get('lost_reason') and not lead.lost_reason:
                    raise exceptions.UserError(
                        'Você deve informar o motivo da perda antes de mover para o estágio "Perdido".'
                    )
        return super(CrmLead, self).write(vals)

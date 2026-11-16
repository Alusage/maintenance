# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    equipment_ids = fields.One2many("maintenance.equipment", "assigned_partner_id")
    maintenance_request_ids = fields.One2many("maintenance.request", "partner_id")
    equipment_count = fields.Integer(compute="_compute_equipment_count")
    maintenance_request_count = fields.Integer(
        compute="_compute_maintenance_request_count"
    )

    @api.depends("equipment_ids")
    def _compute_equipment_count(self):
        counts = dict(
            self.env["maintenance.equipment"]._read_group(
                [("assigned_partner_id", "in", self.ids)],
                ["assigned_partner_id"],
                ["__count"],
            )
        )
        for partner in self:
            partner.equipment_count = counts.get(partner, 0)

    @api.depends("maintenance_request_ids")
    def _compute_maintenance_request_count(self):
        counts = dict(
            self.env["maintenance.request"]._read_group(
                [("partner_id", "in", self.ids)], ["partner_id"], ["__count"]
            )
        )
        for partner in self:
            partner.maintenance_request_count = counts.get(partner, 0)

# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class MrpInventoryProcure(models.TransientModel):
    _name = "repair.move.transfer"
    _description = "Create an internal transfer from repaired moves"

    repair_order_id = fields.Many2one(
        "repair.order", string="Repair Order", required=True
    )
    location_dest_id = fields.Many2one(
        "stock.location", string="Destination location", required=True
    )
    quantity = fields.Float("Quantity to transfer", required=True)
    remaining_quantity = fields.Float("Remaining Quantity to Transfer")

    def _get_picking_type(self):
        self.ensure_one()
        warehouse = self.repair_order_id.location_id.warehouse_id
        return warehouse.int_type_id

    def _prepare_picking_vals(self):
        return {
            "partner_id": False,
            "user_id": False,
            "picking_type_id": self._get_picking_type().id,
            "move_type": "direct",
            "location_id": self.repair_order_id.location_id.id,
            "location_dest_id": self.location_dest_id.id,
        }

    def _prepare_stock_move_vals(self, picking):
        self.ensure_one()
        return {
            "name": self.repair_order_id.product_id.name,
            "product_id": self.repair_order_id.product_id.id,
            "location_id": self.repair_order_id.location_id.id,
            "location_dest_id": self.location_dest_id.id,
            "picking_id": picking.id,
            "state": "draft",
            "company_id": picking.company_id.id,
            "picking_type_id": self._get_picking_type().id,
            "product_uom_qty": self.quantity,
            "product_uom": self.repair_order_id.move_id.product_uom.id,
            "quantity": 0,
            "repair_id": self.repair_order_id.id,
        }

    def action_create_transfer(self):
        self.ensure_one()

        if (
            float_compare(
                self.quantity,
                0.0,
                precision_rounding=self.repair_order_id.product_id.uom_id.rounding,
            )
            <= 0
        ):
            raise UserError(_("Quantity to transfer must be greater than 0."))

        if (
            float_compare(
                self.quantity,
                self.repair_order_id.remaining_quantity,
                precision_rounding=self.repair_order_id.product_id.uom_id.rounding,
            )
            > 0
        ):
            raise UserError(
                _(
                    "Quantity to transfer cannot exceed the remaining "
                    "quantity in the repair order."
                )
            )

        picking = self.env["stock.picking"].create(self._prepare_picking_vals())
        stock_move = self.env["stock.move"].create(
            self._prepare_stock_move_vals(picking)
        )
        picking.action_assign()
        if self.repair_order_id.lot_id:
            stock_move.move_line_ids[0].write(
                {"lot_id": self.repair_order_id.lot_id.id}
            )
        self.repair_order_id._compute_picking_ids()

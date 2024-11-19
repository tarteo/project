from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_start = fields.Datetime(
        string="Started Date", help="Date on which the task has started being worked on"
    )
    date_planned_start = fields.Datetime("Planned Start")
    date_planned_end = fields.Datetime("Planned End")

    @api.model_create_multi
    def create(self, vals_list):
        now = fields.Datetime.now()
        for vals in vals_list:
            if vals.get("stage_id") and not vals.get("date_start"):
                project_task_type = self.env["project.task.type"].browse(
                    vals["stage_id"]
                )
                if not project_task_type.is_start:
                    continue
                vals["date_start"] = now
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if vals.get("stage_id") and not vals.get("date_start"):
            now = fields.Datetime.now()
            for task in self.filtered(
                lambda t: not t.date_start and t.stage_id.is_start
            ):
                task.date_start = now
        return res

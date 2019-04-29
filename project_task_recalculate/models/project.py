# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning, ValidationError
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil import relativedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def project_recalculate(self):
        """
            Recalculate project tasks start and end dates.
            After that,
            recalculate new project start or end date
        """
        for project in self:
            if not project.calculation_type:
                raise Warning(_("Cannot recalculate project because your "
                                "project don't have calculation type."))
            if (project.calculation_type == 'date_begin' and not
                    project.date_start):
                raise Warning(_("Cannot recalculate project because your "
                                "project don't have date start."))
            if (project.calculation_type == 'date_end' and not
                    project.date):
                raise Warning(_("Cannot recalculate project because your "
                                "project don't have date end."))
            if project.calculation_type != 'none':

                task_with_only_childs = self.env['project.task'].search(
                    [('project_id', '=', project.id),
                    ('child_ids', '!=', False), ('parent_ids', '=', False)])
                for task in task_with_only_childs:
                    task.task_recalculate()

                task_with_childs_parents = self.env['project.task'].search(
                    [('project_id', '=', project.id),
                    ('child_ids', '!=', False), ('parent_ids', '!=', False)])
                for task in task_with_childs_parents:
                    task.task_recalculate()

                task_with_only_parents = self.env['project.task'].search(
                    [('project_id', '=', project.id),
                    ('child_ids', '=', False), ('parent_ids', '!=', False)])
                for task in task_with_only_parents:
                    task.task_recalculate()

                task_without_childs_parents = self.env['project.task'].search(
                    [('project_id', '=', project.id),
                    ('child_ids', '=', False), ('parent_ids', '=', False)])
                for task in task_without_childs_parents:
                    task.task_recalculate()

                vals = project._start_end_dates_prepare()
                if vals:
                    project.write(vals)
        return True


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def task_recalculate(self):
        to_string = fields.Datetime.to_string

        for task in self:
            if not task.include_in_recalculate:
                return True

            resource, calendar = task._resource_calendar_select()
            increment, project_date, from_days = task._calculation_prepare()
            date_start = False
            date_end = False
            from_days = self._from_days_dec(
                from_days, project_date, resource, calendar, increment)
            start = self._calendar_schedule_days(
                from_days, project_date, resource, calendar)[1]
            if start:
                day = start[0].replace(hour=0, minute=0, second=0)
                first = self._first_interval_of_day_get(
                    day, resource, calendar)
                if first:
                    date_start = first[0]
            if date_start:
                if task.parent_ids:
                    date_start = self._get_max_date_from_parents(task, date_start)
                end = self._calendar_schedule_days(
                    task.estimated_days + 0.001, date_start, resource, calendar)[1]
                if end:
                    date_end = end[1]

            task.with_context(task.env.context, task_recalculate=True).write({
                'date_start': date_start and to_string(date_start) or False,
                'date_end': date_end and to_string(date_end) or False,
                'date_deadline': task.priority == u'2' and date_start and to_string(date_start) or False,
            })

        return True

    @api.multi
    def _get_max_date_from_parents(self, task, date_start):
        max_date = date_start

        for parent in task.parent_ids:
            if parent.date_end:
                if datetime.strptime(
                        parent.date_end, DEFAULT_SERVER_DATETIME_FORMAT) > max_date:
                    max_date = datetime.strptime(
                        parent.date_end, DEFAULT_SERVER_DATETIME_FORMAT)

        return max_date

    @api.onchange('date_end')
    def onchange_date_end(self):
        def recurse_child_task(task):
            for child_task in task.child_ids:
                if child_task.date_end and child_task.date_start:
                    duration = datetime.strptime(
                        child_task.date_end, DEFAULT_SERVER_DATETIME_FORMAT
                    ) - datetime.strptime(
                        child_task.date_start, DEFAULT_SERVER_DATETIME_FORMAT)
                elif child_task.estimated_days:
                    duration = timedelta(child_task.estimated_days)
                else:
                    duration = timedelta(0)
                child_task.write({
                    'date_end': (datetime.strptime(
                        task.date_end, DEFAULT_SERVER_DATETIME_FORMAT) +
                                 relativedelta.relativedelta(
                                     days=duration.days or 0)).strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT),
                    'date_start': task.date_end})
                if child_task.child_ids:
                    recurse_child_task(child_task)

        recurse_child_task(self)
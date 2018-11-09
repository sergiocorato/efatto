# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _, exceptions


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )

    @api.multi
    @api.constrains('task_id', 'account_id')
    def _check_task_project(self):
        for hr in self:
            if hr.task_id and hr.account_id != \
                    hr.task_id.project_id.analytic_account_id:
                raise exceptions.ValidationError(
                    "Task must be children of project")

    # when create analytic timesheet directly, create project.task.work
    @api.model
    def create(self, vals):
        res = super(HrAnalyticTimesheet, self).create(vals)
        if vals.get('task_id', False):
            date = vals['date']
            if date == fields.Date.today():
                date = fields.Datetime.now()
            values = {
                'name': vals['name'],
                'date': date,
                'task_id': vals['task_id'],
                'hours': vals['unit_amount'],
                'user_id': vals['user_id'],
                'company_id': self.env['res.users'].browse(
                    vals['user_id']).company_id.id,
                'hr_analytic_timesheet_id': res.id,
            }
            self.env['project.task.work'].with_context(
                {'no_analytic_entry': True}).create(values)
            # force update of project hours and progress
            task = self.env['project.task'].browse(vals['task_id'])
            if task and task.project_id:
                project_vals = task.project_id._progress_rate(
                    names=False, arg=False)
                self._cr.execute(
                    'update project_project set effective_hours='
                    '(%s) where id=%s',
                    (project_vals[task.project_id.id][
                         'effective_hours'], task.project_id.id))
                self.invalidate_cache()
        return res

    @api.multi
    def write(self, vals):
        for line in self:
            if line.task_id or vals.get('task_id', False):
                date = vals.get('date', False) or line.date
                if date == fields.Date.today():
                    date = fields.Datetime.now()
                user = vals.get('user_id', False) or line.user_id.id
                task_work = self.env['project.task.work'].search([
                    ('hr_analytic_timesheet_id', '=', line.id)
                ])
                values = {
                    'name': vals.get('name', False) or line.name,
                    'date': date,
                    'task_id': vals.get('task_id', False) or line.task_id.id,
                    'hours': vals.get('unit_amount', False) or
                    line.unit_amount,
                    'user_id': user,
                    'company_id': self.env['res.users'].browse(
                        user).company_id.id,
                }
                # task_work is found here only if task_id was set initially
                if task_work:
                    task_work.with_context(
                        {'no_analytic_entry': True}).write(values)
                # create task work when modify timesheet adding task_id
                # but if timesheet is created from task, task not yet exists,
                # so added super() of create() with context no_task_entry
                # perhaps there is a better way, but pay attention to recursion
                else:
                    if not self._context.get('no_task_entry', False):
                        values['hr_analytic_timesheet_id'] = line.id
                        task_work.with_context(
                            {'no_analytic_entry': True}).create(values)
        return super(HrAnalyticTimesheet, self).write(vals)

    @api.multi
    def unlink(self):
        # when unlink, unlink task work
        for line in self:
            if line.task_id:
                task_work = self.env['project.task.work'].search([
                    ('hr_analytic_timesheet_id', '=', line.id)
                ])
                if task_work:
                    task_work.with_context(
                        {'no_analytic_entry': True}).unlink()
        return super(HrAnalyticTimesheet, self).unlink()


class ProjectWork(models.Model):
    _inherit = "project.task.work"

    @api.model
    def _create_analytic_entries(self, vals):
        timeline_id = super(ProjectWork, self)._create_analytic_entries(
            vals=vals)
        if vals.get('task_id', False) and timeline_id:
            self.env['hr.analytic.timesheet'].browse(
                timeline_id).task_id = vals['task_id']
        return timeline_id

    @api.multi
    def write(self, vals):
        # Bypass original write method to avoid recursion generated from
        # project_timesheet
        if self.env.context.get('no_analytic_entry', False):
            if 'hours' in vals and (not vals['hours']):
                vals['hours'] = 0.00
            if 'hours' in vals:
                for work in self:
                    old_project_id = work.task_id.project_id
                    old_project_progress = old_project_id._progress_rate(
                        names=False, arg=False)
                    if 'task_id' in vals:
                        # task is changed
                        # update old task adding remaining hours not used
                        self._cr.execute(
                            'update project_task set remaining_hours='
                            'remaining_hours + (%s) where id=%s',
                            (work.hours, work.task_id.id))
                        # and new task removing remaining hours used
                        self._cr.execute(
                            'update project_task set remaining_hours='
                            'remaining_hours - %s where id=%s',
                            (vals.get('hours', 0.0), vals.get('task_id')))
                        # update project total hours
                        new_project_id = self.env['project.task'].browse(
                            vals.get('task_id')).project_id
                        if old_project_id != new_project_id:
                            # update old project removing hours not done
                            self._cr.execute(
                                'update project_project set effective_hours='
                                '(%s) - (%s) where id=%s',
                                (old_project_progress[old_project_id.id][
                                 'effective_hours'],
                                 work.hours, old_project_id.id))
                            # and new project adding hours done
                            new_project_progress = new_project_id.\
                                _progress_rate(names=False, arg=False)
                            self._cr.execute(
                                'update project_project set effective_hours='
                                '(%s) + %s where id=%s',
                                (new_project_progress[new_project_id.id][
                                 'effective_hours'],
                                 vals.get('hours', 0.0), new_project_id.id))
                        else:
                            self._cr.execute(
                                'update project_project set effective_hours='
                                '(%s) + %s - (%s) where id=%s',
                                (old_project_progress[old_project_id.id][
                                 'effective_hours'],
                                 vals.get('hours', 0.0), work.hours,
                                 old_project_id.id))
                    else:
                        # task is unchanged
                        self._cr.execute(
                            'update project_task set remaining_hours='
                            'remaining_hours - %s + (%s) where id=%s',
                            (vals.get('hours', 0.0), work.hours,
                             work.task_id.id))
                        # update project total hours
                        self._cr.execute(
                            'update project_project set effective_hours='
                            '(%s) + %s - (%s) where id=%s',
                            (old_project_progress[old_project_id.id][
                             'effective_hours'],
                             vals.get('hours', 0.0), work.hours,
                             work.task_id.project_id.id))
                    self.invalidate_cache()
            return super(models.Model, self).write(vals)
        return super(ProjectWork, self).write(vals)

    def create(self, cr, uid, vals, *args, **kwargs):
        context = kwargs.get('context', {})
        ctx = context.copy()
        ctx.update({'no_task_entry': True})
        kwargs['context'] = ctx
        return super(ProjectWork,self).create(cr, uid, vals, *args, **kwargs)

    @api.multi
    def unlink(self):
        if self.env.context.get('no_analytic_entry', False):
            for work in self:
                self._cr.execute(
                    'update project_task set remaining_hours=remaining_hours'
                    ' + %s where id=%s', (work.hours, work.task_id.id))
                project_vals = work.task_id.project_id._progress_rate(
                    names=False, arg=False)
                self._cr.execute(
                    'update project_project set effective_hours='
                    '(%s) - %s where id=%s',
                    (project_vals[work.task_id.project_id.id][
                             'effective_hours'],
                     work.hours, work.task_id.project_id.id))
                self.invalidate_cache()
            return super(models.Model, self).unlink()
        return super(ProjectWork, self).unlink()
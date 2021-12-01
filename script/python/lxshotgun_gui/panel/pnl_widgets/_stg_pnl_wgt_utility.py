# coding:utf-8
import copy

from lxutil import utl_core

from lxutil_gui.panel import utl_gui_pnl_abs_utility

import lxshotgun.objects as stg_objects

import lxshotgun.methods as stg_methods


class ShotgunEntityCreator(utl_gui_pnl_abs_utility.AbsShotgunEntitiesCreatorPanel):
    def __init__(self, *args, **kwargs):
        super(ShotgunEntityCreator, self).__init__(*args, **kwargs)
        self._stg_connector = stg_objects.StgConnector()
        self.get_log_bar().set_expanded(True)

    def _get_projects_(self):
        lis = []
        for stg_project_query in self._stg_connector.get_stg_project_queries():
            if stg_project_query.get('sg_studio') in self.STUDIO_INCLUDES:
                name = stg_project_query.get('tank_name')
                if name:
                    lis.append(name)
        #
        lis.sort()
        return lis

    def _set_create_(self):
        project = self._get_project_()
        entities = self._get_entities_()
        task_template = self._get_task_template_()
        stg_methods.StgTaskMtd.set_entities_create_by_template(
            project=project, entities=entities, task_template=task_template
        )

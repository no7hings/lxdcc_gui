# coding:utf-8
import copy

import six

import os

import functools

import types

import lxlog.core as log_core

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

from lxgui.qt.widgets import _gui_qt_wgt_utility, _gui_qt_wgt_button, _gui_qt_wgt_input, _gui_qt_wgt_input_for_storage

import lxgui.proxy.abstracts as gui_prx_abstracts

from lxgui.proxy.widgets import _gui_prx_wdt_utility, _gui_prx_wgt_port_base, _gui_prx_wgt_view_for_tree


class PrxInputAsStgTask(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _gui_qt_wgt_utility._QtTranslucentWidget
    
    class Schemes(object):
        AssetTask = 'asset-task'

        SequenceTask = 'sequence-task'
        ShotTask = 'shot-task'

        ProjectTask = 'project-task'

        All = [
            AssetTask,
            SequenceTask,
            ShotTask,
            ProjectTask
        ]

    def __init__(self, *args, **kwargs):
        super(PrxInputAsStgTask, self).__init__(*args, **kwargs)

        self.__signals = gui_qt_core.QtActionSignals(self.get_widget())

        self.__resource_type = 'asset'
        self.__scheme = self.Schemes.AssetTask

        self.__next_tip = '...'

        self.__project_dict = {}
        self.__resource_dict = {}
        self.__task_dict = {}

        self.__result_dict = None

        import lxwarp.shotgun.core as wrp_stg_core

        self._stg_connector = wrp_stg_core.StgConnector()

        l_0 = _gui_qt_wgt_utility.QtHLayout(self.get_widget())
        l_0.setContentsMargins(*[0]*4)
        l_0._set_align_top_()

        self.__scheme_input = _gui_qt_wgt_input.QtInputAsBubbleWithChoose()
        l_0.addWidget(self.__scheme_input)
        self.__scheme_input._set_choose_values_(
            self.Schemes.All
        )
        self.__scheme_input.input_value_change_accepted.connect(
            self.__update_branch
        )

        self.__path_input = _gui_qt_wgt_input.QtInputAsPath()
        l_0.addWidget(self.__path_input)

        self.__path_input._set_buffer_fnc_(
            self.__buffer_fnc
        )

        self.__path_input._set_value_('/')
        self.__path_input._set_choose_popup_auto_resize_enable_(False)
        self.__path_input._set_choose_popup_tag_filter_enable_(True)
        self.__path_input._set_choose_popup_keyword_filter_enable_(True)

        self.__path_input._set_choose_popup_item_size_(40, 40)

        self.__path_input._setup_()

        self.__path_input.input_value_change_accepted.connect(self.__update_task)
        self.__path_input.user_input_entry_finished.connect(self.__accept_result)

        self.__scheme_input._set_value_(self.Schemes.AssetTask)

        self.__scheme_input._set_history_key_('gui.shotgun-branch')
        self.__scheme_input._pull_history_latest_()

        self.__path_input._set_history_key_('gui.input-path-{}'.format(self.__scheme))
        self.__path_input._pull_history_latest_()

        self.__path_input._create_widget_shortcut_action_(
            self.__to_next_scheme, 'Alt+Right'
        )
        self.__path_input._create_widget_shortcut_action_(
            self.__to_previous_scheme, 'Alt+Left'
        )

    def __to_next_scheme(self):
        self.__scheme_input._get_entry_widget_()._to_next_()

    def __to_previous_scheme(self):
        self.__scheme_input._get_entry_widget_()._to_previous_()

    def set_focus_in(self):
        self.__path_input._set_input_entry_focus_in_()

    def has_focus(self):
        return self.__path_input._get_input_entry_has_focus_()

    def connect_result_to(self, fnc):
        self.__signals.dict_accepted.connect(fnc)

    def connect_tip_trace_to(self, fnc):
        self.__signals.str_accepted.connect(fnc)

    def __update_branch(self, text):
        if text != self.__scheme:
            path_text = self.__path_input._get_value_()
            path = bsc_core.DccPathDagOpt(path_text)

            self.__scheme = text
            self.__path_input._restore_buffer_cache_()

            self.__resource_type = None
            if self.__scheme == self.Schemes.AssetTask:
                self.__resource_type = 'asset'
            elif self.__scheme == self.Schemes.SequenceTask:
                self.__resource_type = 'sequence'
            elif self.__scheme == self.Schemes.ShotTask:
                self.__resource_type = 'shot'

            self.__path_input._set_history_key_('gui.input-path-{}'.format(self.__scheme))
            if self.__path_input._pull_history_latest_() is False:
                cs = path.get_components()
                cs.reverse()
                d = len(cs)
                if d > 1:
                    self.__path_input._set_value_(cs[1].to_string())

            path_text_cur = self.__path_input._get_value_()
            if path_text_cur == path_text:
                self.__path_input._update_next_()

    def __cache_projects(self):
        self.__project_dict = {}
        (
            self.__project_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs=dict(
                entity_type='Project',
                filters=[
                    ['users', 'in', [self._stg_connector.get_current_stg_user()]],
                    ['sg_status', 'in', ['Active', 'Accomplish']]
                ],
                fields=['name', 'sg_description']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'sg_description'],
            tag_filter_fields=['sg_status']
        )
        return self.__project_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def __cache_resources(self, project):
        self.__resource_type = None
        if self.__scheme == self.Schemes.AssetTask:
            self.__resource_type = 'asset'
            stg_entity_type = self._stg_connector.StgEntityTypes.Asset
            tag_filter_fields = ['sg_asset_type']
            keyword_filter_fields = ['code', 'sg_chinese_name']
        elif self.__scheme == self.Schemes.SequenceTask:
            self.__resource_type = 'sequence'
            stg_entity_type = self._stg_connector.StgEntityTypes.Sequence
            tag_filter_fields = ['tags']
            keyword_filter_fields = ['code', 'description']
        elif self.__scheme == self.Schemes.ShotTask:
            self.__resource_type = 'shot'
            stg_entity_type = self._stg_connector.StgEntityTypes.Shot
            tag_filter_fields = ['sg_sequence']
            keyword_filter_fields = ['code', 'description']
        else:
            raise RuntimeError()

        (
            self.__resource_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs=dict(
                entity_type=stg_entity_type,
                filters=[
                    ['project', 'is', self._stg_connector.get_stg_project(project=project)],
                ],
                fields=keyword_filter_fields
            ),
            name_field='code',
            keyword_filter_fields=keyword_filter_fields,
            tag_filter_fields=tag_filter_fields,
        )
        return self.__resource_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def __cache_project_tasks(self, project):
        kw = {
            'project': project,
        }
        (
            self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs={
                'entity_type': 'Task',
                'filters': [
                    ['entity', 'is', self._stg_connector.get_stg_project(**kw)]
                ],
                'fields': ['content', 'sg_status_list'],
            },
            name_field='content',
            keyword_filter_fields=['content', 'sg_status_list'],
            tag_filter_fields=['step'],
        )
        return self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def __cache_resource_tasks(self, project, resource):
        kw = {
            'project': project,
            self.__resource_type: resource
        }
        (
            self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs={
                'entity_type': 'Task',
                'filters': [
                    ['entity', 'is', self._stg_connector.get_stg_resource(**kw)]
                ],
                'fields': ['content', 'sg_status_list'],
            },
            name_field='content',
            keyword_filter_fields=['content', 'sg_status_list'],
            tag_filter_fields=['step'],
        )
        return self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def __update_project_task_result(self, project, task):
        kw = {
            'project': project,
            'task': task
        }
        stg_task = self._stg_connector.find_stg_task(
            **kw
        )
        if stg_task:
            result = copy.copy(kw)
            result['scheme'] = self.__scheme
            result['project'] = kw['project'].lower()
            result['task_id'] = stg_task['id']
            self.__result_dict = result

    def __update_resource_task_result(self, project, resource, task):
        kw = {
            'project': project,
            self.__resource_type: resource,
            'task': task
        }
        stg_task = self._stg_connector.find_stg_task(
            **kw
        )
        if stg_task:
            result = copy.copy(kw)
            result['scheme'] = self.__scheme
            result['project'] = kw['project'].lower()
            result['task_id'] = stg_task['id']
            self.__result_dict = result

    def __update_task(self, path_text):
        self.__result_dict = None
        if path_text:
            path = bsc_core.DccPathDagOpt(path_text)
            cs = path.get_components()
            cs.reverse()

            self.__next_tip = '...'
            if len(cs) == 1:
                self.__next_tip = 'enter or choose a "project"'
            elif len(cs) == 2:
                if self.__scheme == self.Schemes.ProjectTask:
                    self.__next_tip = 'enter or choose a "task"'
                else:
                    self.__next_tip = 'enter or choose a "{}"'.format(self.__scheme)
            elif len(cs) == 3:
                if self.__scheme == self.Schemes.ProjectTask:
                    project = cs[1].get_name()
                    task = cs[2].get_name()
                    self.__update_project_task_result(project, task)

                    self.__next_tip = 'press "Enter" to accept'
                else:
                    self.__next_tip = 'enter or choose a "task"'
            elif len(cs) == 4:
                project = cs[1].get_name()
                resource = cs[2].get_name()
                task = cs[3].get_name()
                self.__update_resource_task_result(project, resource, task)

                self.__next_tip = 'press "Enter" to accept'

            self.__accept_tip()

    def __buffer_fnc(self, path):
        dict_ = {}

        cs = path.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            (
                entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
            ) = self.__cache_projects()
        elif d == 2:
            project = cs[1].get_name()
            if self.__scheme == self.Schemes.ProjectTask:
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self.__cache_project_tasks(project)
            else:
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self.__cache_resources(project)
        elif d == 3:
            if self.__scheme == self.Schemes.ProjectTask:
                entity_dict = {}
                name_texts = []
                image_url_dict = {}
                keyword_filter_dict = {}
                tag_filter_dict = {}
            else:
                project = cs[1].get_name()
                resource = cs[2].get_name()
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self.__cache_resource_tasks(project, resource)
        else:
            entity_dict = {}
            name_texts = []
            image_url_dict = {}
            keyword_filter_dict = {}
            tag_filter_dict = {}

        dict_['query_dict'] = entity_dict
        dict_['names'] = name_texts
        dict_['image_url_dict'] = image_url_dict
        dict_['keyword_filter_dict'] = keyword_filter_dict
        dict_['tag_filter_dict'] = tag_filter_dict

        return dict_

    def __accept_result(self):
        self.__update_task(
            self.__path_input._get_value_()
        )
        dict_ = self.__result_dict
        if dict_:
            self.__signals.dict_accepted.emit(dict_)

    def __accept_tip(self):
        self.__signals.str_accepted.emit(
            (
                'load task for {}:\n'
                '    press "Alt+Left" or "Alt+Right" to switch branch;\n'
                '    {}.'
            ).format(
                self.__scheme, self.__next_tip
            )
        )

    def get_scheme(self):
        return self.__scheme

    def setup(self):
        self.__accept_tip()

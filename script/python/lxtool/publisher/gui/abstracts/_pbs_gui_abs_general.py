# coding:utf-8
import collections
import copy

import lxbasic.core as bsc_core

import lxgui.proxy.widgets as prx_widgets

from lxutil import utl_core

import lxutil.scripts as utl_scripts

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxgui.proxy.scripts as gui_prx_scripts

import lxresolver.commands as rsv_commands

import lxsession.commands as ssn_commands

import lxgui.core as gui_core


class AbsPnlPublisherForGeneral(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlPublisherForGeneral, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self.__task_data = {}
        #
        self.__stg_user = None
        self.__stg_task = None
        #
        self._rsv_project = None
        self._rsv_task = None
        self._step_mapper = dict()
        self._version_properties = None

    def set_all_setup(self):
        sa_1 = prx_widgets.PrxVScrollArea()
        self.add_widget(sa_1)

        self.__input = prx_widgets.PrxInputAsStgTask()
        sa_1.add_widget(self.__input)

        self.__input.set_focus_in()

        self.__tip = prx_widgets.PrxTextBrowser()
        sa_1.add_widget(self.__tip)
        self.__tip.set_focus_enable(False)

        self.__next_button = prx_widgets.PrxPressItem()
        self.__next_button.set_name('next')
        self.add_button(self.__next_button)
        self.__next_button.connect_press_clicked_to(self.__do_next)
        self.__next_button.set_enable(False)

        self.__input.connect_result_to(self.__do_accept)
        self.__input.connect_tip_trace_to(self.__do_tip_accept)

        self.__input.setup()
        # publish
        layer_widget = self.create_layer_widget('publish', 'Publish')
        sa_2 = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(sa_2)
        self._publish_options_prx_node = prx_widgets.PrxNode('options')
        sa_2.add_widget(self._publish_options_prx_node)
        self._publish_options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.publish_options')
        )

        self._publish_options_prx_node.get_port('version_scheme').connect_input_changed_to(
            self.refresh_publish_version_directory
        )

        self._publish_tip = prx_widgets.PrxTextBrowser()
        sa_2.add_widget(self._publish_tip)
        self._publish_tip.set_content(
            self._session.configure.get('build.node.publish_content')
        )
        self._publish_tip.set_font_size(12)

        tool_bar = prx_widgets.PrxHToolBar()
        layer_widget.add_widget(tool_bar)
        tool_bar.set_expanded(True)

        self._publish_button = prx_widgets.PrxPressItem()
        tool_bar.add_widget(self._publish_button)
        self._publish_button.set_name('publish')
        self._publish_button.connect_press_clicked_to(
            self.execute_publish
        )

        self.refresh_all_fnc()

    def __do_tip_accept(self, text):
        if self.__input.get_is_valid():
            self.__next_button.set_enable(True)
        else:
            self.__next_button.set_enable(False)

        self.__tip.set_content(text)

    def __do_accept(self, dict_):
        if dict_:
            task_id = dict_['task_id']
            self.__stg_task = self._stg_connector.get_stg_task(id=task_id)
            self.__task_data = self._stg_connector.get_data_from_task_id(
                str(dict_['task_id'])
            )
            if self.validator_fnc() is True:
                self.switch_current_layer_to('publish')
                self.get_layer_widget('publish').set_name(
                    'publish for [{project}.{resource}.{task}]'.format(
                        **self.__task_data
                    )
                )
                fncs = [
                    self.refresh_publish_options,
                    self.refresh_publish_version_directory,
                    self.refresh_publish_notice,
                    self.refresh_publish_scene,
                    self.refresh_publish_process_settings,
                ]
                #
                with self.gui_progressing(maximum=len(fncs), label='execute refresh process') as g_p:
                    for i_fnc in fncs:
                        g_p.do_update()
                        i_fnc()

    def __do_next(self):
        self.__do_accept(self.__input.get_result())

    def refresh_all_fnc(self):
        import lxwrap.shotgun.core as wrp_stg_core

        self._stg_connector = wrp_stg_core.StgConnector()
        self._user_name = bsc_core.SystemMtd.get_user_name()
        self.__stg_user = self._stg_connector.get_stg_user(user=self._user_name)
        if not self.__stg_user:
            utl_core.DccDialog.create(
                self._session.gui_name,
                content='user "{}" is not available'.format(self._user_name),
                status=utl_core.DccDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            self.close_window_later()
            return

        task_id = bsc_core.EnvironMtd.get(
            'PAPER_TASK_ID'
        )
        if task_id:
            self.__input.setup_from_task_id(task_id)
            self.__do_accept(dict(task_id=task_id))
        else:
            pass

    def refresh_publish_notice(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxwrap.shotgun.core as wrp_stg_core

            t_o = wrp_stg_core.StgTaskOpt(self._stg_connector.to_query(stg_task))
            notice_stg_users = t_o.get_notice_stg_users()
            return list(set([self._stg_connector.to_query(i).get('name').decode('utf-8') for i in notice_stg_users]))

        def built_fnc_(user_names):
            self._publish_options_prx_node.set(
                'notice', user_names
            )

        p = self._publish_options_prx_node.get_port('notice')
        p.set_clear()
        p.set_shotgun_entity_kwargs(
            dict(
                entity_type='HumanUser',
                filters=[
                    ['sg_studio', 'is', 'CG'],
                    ['sg_status_list', 'is', 'act']
                ],
                fields=['name', 'email', 'sg_nickname']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

        stg_task = self.__stg_task

        p.run_as_thread(
            cache_fnc_, built_fnc_, post_fnc_
        )

    def create_task_directory(self):
        if self.__task_data:
            keyword = '{branch}-release-task-dir'.format(**self.__task_data)
            task_directory_pattern = self._rsv_project.get_pattern(
                keyword
            )
            kwargs = copy.copy(self._rsv_project.properties.get_value())
            kwargs['workspace'] = self._rsv_project.to_workspace(
                self._rsv_project.WorkspaceKeys.Release
            )
            kwargs.update(self.__task_data)
            task_directory_path = task_directory_pattern.format(
                **kwargs
            )
            if bsc_core.StgPathMtd.get_is_exists(task_directory_path) is False:
                bsc_core.StgPathPermissionMtd.create_directory(
                    task_directory_path
                )

    def validator_fnc(self):
        if self.__task_data:
            self._resolver = rsv_commands.get_resolver()
            self._rsv_project = self._resolver.get_rsv_project(
                **self.__task_data
            )
            if self._rsv_project is None:
                utl_core.DccDialog.create(
                    self.session.gui_name,
                    content='project is not available',
                    status=utl_core.DccDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
                return False
            #
            self._step_mapper = self._rsv_project.properties.get(
                '{}_steps'.format(self.__task_data.get('branch'))
            )
            #
            self._rsv_task = self._resolver.get_rsv_task(
                **self.__task_data
            )
            if self._rsv_task is None:
                w = utl_core.DccDialog.create(
                    self.session.gui_name,
                    content='task directory is non-exists, press "Yes" to create and continue',
                    status=utl_core.DccDialog.ValidationStatus.Warning,
                    yes_method=self.create_task_directory,
                    # do not use thread
                    # use_thread=False
                )
                result = w.get_result()
                if result is True:
                    self._rsv_task = self._resolver.get_rsv_task(
                        **self.__task_data
                    )
                return result
            return True
        return False

    def refresh_publish_version_directory(self):
        version_scheme = self._publish_options_prx_node.get('version_scheme')
        #
        branch = self._rsv_task.properties.get('branch')
        self._step_mapper = self._rsv_project.properties.get('{}_steps'.format(branch))
        #
        version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='{branch}-release-version-dir'
        )
        version_directory_path = version_directory_rsv_unit.get_result(
            version=version_scheme
        )
        self._publish_options_prx_node.set(
            'version_directory', version_directory_path
        )
        self._version_properties = version_directory_rsv_unit.generate_properties_by_result(
            version_directory_path
        )
        self._version_properties.update_from(self.__task_data)
        self._version_properties.set('user', self._user_name)

    def refresh_publish_options(self):
        self._publish_options_prx_node.set('version_type', 'daily')
        self._publish_options_prx_node.set('version_scheme', 'new')
        self._publish_options_prx_node.set('description', '')
        self._publish_options_prx_node.get_port('review').set_clear()
        self._publish_options_prx_node.get_port('extra.scene').set_clear()
        self._publish_options_prx_node.get_port('extra.image').set_clear()
        self._publish_options_prx_node.set(
            'process.settings.with_scene', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_render_texture', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_preview_texture', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_look_yml', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_camera_abc', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_camera_usd', False
        )

    def refresh_publish_scene(self):
        if bsc_core.ApplicationMtd.get_is_dcc():
            if bsc_core.ApplicationMtd.get_is_maya():
                import lxmaya.dcc.dcc_objects as mya_dcc_objects

                self._publish_options_prx_node.set(
                    'extra.scene', [mya_dcc_objects.Scene.get_current_file_path()]

                )
            elif bsc_core.ApplicationMtd.get_is_katana():
                import lxkatana.dcc.dcc_objects as ktn_dcc_objects

                self._publish_options_prx_node.set(
                    'extra.scene', [ktn_dcc_objects.Scene.get_current_file_path()]

                )

    def refresh_publish_process_settings(self):
        step = self.__task_data['step']
        if self._step_mapper:
            if step in {self._step_mapper.get('surface')}:
                self._publish_options_prx_node.set(
                    'process.settings.with_scene', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_preview_texture', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_look_yml', True
                )
            elif step in {self._step_mapper.get('camera')}:
                self._publish_options_prx_node.set(
                    'process.settings.with_scene', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_camera_abc', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_camera_usd', True
                )

    def __do_next_(self):
        if self.__next_button.get_is_enable() is True:
            self.__task_data = self._stg_connector.get_data_from_task_id(
                str(self.__stg_task['id'])
            )
            if self.validator_fnc() is True:
                self.switch_current_layer_to('publish')
                self.get_layer_widget('publish').set_name(
                    'publish for [{project}.{resource}.{task}]'.format(
                        **self.__task_data
                    )
                )
                fncs = [
                    self.refresh_publish_options,
                    self.refresh_publish_version_directory,
                    self.refresh_publish_notice,
                    self.refresh_publish_scene,
                    self.refresh_publish_process_settings,
                ]
                #
                with self.gui_progressing(maximum=len(fncs), label='execute refresh process') as g_p:
                    for i_fnc in fncs:
                        g_p.do_update()
                        i_fnc()

    def execute_publish(self):
        p = utl_scripts.ScpGeneralPublish(
            self,
            self._session,
            self._rsv_task,
            self._version_properties,
            self._publish_options_prx_node.to_dict()
        )
        p.execute()
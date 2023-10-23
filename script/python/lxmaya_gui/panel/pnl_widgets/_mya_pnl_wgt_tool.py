# coding:utf-8
from lxutil import utl_core

from lxutil import utl_configure

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxgui.proxy.widgets as prx_widgets


class PnlSceneClearner(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlSceneClearner, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

    def apply_fnc(self):
        ps = [i_p for i_p in self._options_prx_node.get_ports() if i_p.get_type() == 'check_button' and i_p]
        if ps:
            with self.gui_progressing(maximum=len(ps), label='clean all') as g_p:
                for i_p in ps:
                    g_p.set_update()
                    #
                    i_p.execute()


class PnlGeometryExporter(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlGeometryExporter, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

        self.post_setup_fnc()
        self.refresh_components()

    def post_setup_fnc(self):
        from lxutil import utl_core

        import lxresolver.commands as rsv_commands

        import lxresolver.scripts as rsv_scripts

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_commands.get_resolver()

        self._rsv_task = self._resolver.get_rsv_task(
            **env_data
        )
        if self._rsv_task is not None:
            self._rsv_project = self._rsv_task.get_rsv_project()

            self._dcc_data = self._rsv_project.get_dcc_data(application='maya')

            keyword = 'asset-source-geometry-usd-payload-file'

            rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )

            result = rsv_unit.get_result('new')

            o = self._options_prx_node

            o.set('usd.file', result)

            o.get_port('renderable.components').connect_value_changed_to(
                self.refresh_components
            )
            o.set('renderable.export', self.export_renderable_fnc_)
            o.get_port('auxiliary.components').connect_value_changed_to(
                self.refresh_components
            )
            o.set('auxiliary.export', self.export_auxiliary_fnc_)
        else:
            utl_core.DccDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=utl_core.DccDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.close_window_later()

    def export_renderable_fnc_(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        renderable_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'renderable']
        if file_path and renderable_locations:
            import lxmaya.fnc.exporters as mya_fnc_exporters
            mya_fnc_exporters.FncGeometryUsdExporterNew(
                option=dict(
                    file=file_path,
                    renderable_locations=renderable_locations,
                )
            ).execute()

    def export_auxiliary_fnc_(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        auxiliary_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'auxiliary']
        if file_path and auxiliary_locations:
            import lxmaya.fnc.exporters as mya_fnc_exporters
            mya_fnc_exporters.FncGeometryUsdExporterNew(
                option=dict(
                    file=file_path,
                    auxiliary_locations=auxiliary_locations,
                )
            ).execute()

    def apply_fnc(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        renderable_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'renderable']
        auxiliary_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'auxiliary']
        if file_path and (renderable_locations or auxiliary_locations):
            import lxmaya.fnc.exporters as mya_fnc_exporters
            mya_fnc_exporters.FncGeometryUsdExporterNew(
                option=dict(
                    file=file_path,
                    renderable_locations=renderable_locations,
                    auxiliary_locations=auxiliary_locations,
                )
            ).execute()

    def refresh_components(self):
        objs = []
        for i_branch_key in ['renderable', 'auxiliary']:
            i_leafs = self._options_prx_node.get('{}.components'.format(i_branch_key)) or []
            for j_leaf in i_leafs:
                j_leaf_location = self._dcc_data.get(
                    '{}.{}'.format(i_branch_key, j_leaf)
                )
                if i_branch_key == 'renderable':
                    j_obj = utl_dcc_objects.Obj(j_leaf_location, type_name=i_branch_key, icon_name='obj/renderable')
                elif i_branch_key == 'auxiliary':
                    j_obj = utl_dcc_objects.Obj(j_leaf_location, type_name=i_branch_key, icon_name='obj/non-renderable')
                else:
                    raise RuntimeError()
                #
                objs.append(j_obj)
        #
        self._options_prx_node.set(
            'geometry.components', objs
        )


class PnlGeometryBuilder(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlGeometryBuilder, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        # tip
        self._tip_group = prx_widgets.PrxHToolGroup()
        self.add_widget(self._tip_group)
        self._tip_group.set_expanded(True)
        self._tip_group.set_name('tips')
        self._tip_text_browser = prx_widgets.PrxTextBrowser()
        self._tip_group.add_widget(self._tip_text_browser)

        self.post_setup_fnc()

    def post_setup_fnc(self):
        from lxutil import utl_core

        import lxresolver.commands as rsv_commands

        import lxresolver.scripts as rsv_scripts

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_commands.get_resolver()

        self._rsv_task = self._resolver.get_rsv_task(
            **env_data
        )
        if self._rsv_task is not None:
            self._rsv_project = self._rsv_task.get_rsv_project()
            self._dcc_data = self._rsv_project.get_dcc_data(application='maya')

            o = self._options_prx_node

            o.set('geometry.import', self.import_geometry_fnc)
            o.set('geometry_uv_map.import', self.import_geometry_uv_map_fnc)
            self._tip_text_browser.set_content(self._session.gui_configure.get('content'))
        else:
            utl_core.DccDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=utl_core.DccDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.close_window_later()

    def import_geometry_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        kwargs = self._options_prx_node.to_dict()
        #
        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry=True,
                #
                with_model='model' in kwargs.get('geometry.includes'),
                with_model_dynamic=kwargs.get('geometry.model.mode') == 'dynamic',
                model_space=kwargs.get('geometry.model.space'),
                model_elements=kwargs.get('geometry.model.elements'),
                #
                with_groom='groom' in kwargs.get('geometry.includes'),
                groom_space=kwargs.get('geometry.groom.space'),
                with_groom_grow=kwargs.get('geometry.groom.grow'),
            )
        ).execute()

    def import_geometry_uv_map_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry_uv_map=True,
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()

    def apply_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        kwargs = self._options_prx_node.to_dict()
        #
        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry='geometry' in kwargs.get('includes'),
                with_geometry_uv_map='geometry_uv_map' in kwargs.get('includes'),
                #
                with_model='model' in kwargs.get('geometry.includes'),
                with_model_dynamic=kwargs.get('geometry.model.mode') == 'dynamic',
                model_space=kwargs.get('geometry.model.space'),
                model_elements=kwargs.get('geometry.model.elements'),
                #
                with_groom='groom' in kwargs.get('geometry.includes'),
                groom_space=kwargs.get('geometry.groom.space'),
                with_groom_grow=kwargs.get('geometry.groom.grow'),
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()


class PnlLookBuilder(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlLookBuilder, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        # tip
        self._tip_group = prx_widgets.PrxHToolGroup()
        self.add_widget(self._tip_group)
        self._tip_group.set_expanded(True)
        self._tip_group.set_name('tips')
        self._tip_text_browser = prx_widgets.PrxTextBrowser()
        self._tip_group.add_widget(self._tip_text_browser)

        self.post_setup_fnc()

    def post_setup_fnc(self):
        from lxutil import utl_core

        import lxresolver.commands as rsv_commands

        import lxresolver.scripts as rsv_scripts

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_commands.get_resolver()

        self._rsv_task = self._resolver.get_rsv_task(
            **env_data
        )
        if self._rsv_task is not None:
            self._rsv_project = self._rsv_task.get_rsv_project()
            self._dcc_data = self._rsv_project.get_dcc_data(application='maya')

            o = self._options_prx_node

            o.set('look.import_render', self.import_look_render_fnc)
            o.set('look.import_preview', self.import_look_preview_fnc)
            o.set('geometry_uv_map.import', self.import_geometry_uv_map_fnc)
            self._tip_text_browser.set_content(self._session.gui_configure.get('content'))
        else:
            utl_core.DccDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=utl_core.DccDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.close_window_later()

    def import_look_render_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_look=True,
                #
                with_surface=True,
                surface_space=kwargs.get('look.surface.space'),
            )
        ).execute()

    def import_look_preview_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_look=True,
                #
                with_surface_preview=True,
                surface_space=kwargs.get('look.surface.space'),
            )
        ).execute()

    def import_geometry_uv_map_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry_uv_map=True,
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()

    def apply_fnc(self):
        import lxmaya.fnc.builders as mya_fnc_builders

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_builders.FncAssetBuilderNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry_uv_map='geometry_uv_map' in kwargs.get('includes'),
                #
                with_look='look' in kwargs.get('includes'),
                with_surface_preview=kwargs.get('look.surface.mode') == 'preview',
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()

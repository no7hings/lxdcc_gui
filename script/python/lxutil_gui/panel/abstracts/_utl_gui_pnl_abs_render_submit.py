# coding:utf-8
import collections

from lxbasic import bsc_configure, bsc_core

import lxutil_gui.proxy.widgets as prx_widgets


class AbsPnlRenderSubmitter(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = None
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlRenderSubmitter, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._item_frame_size = self._session.gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._session.gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._session.gui_configure.get('item_icon_size')

        sa_0 = prx_widgets.PrxVScrollArea()
        self.set_widget_add(sa_0)

        ep_0 = prx_widgets.PrxExpandedGroup()
        sa_0.set_widget_add(ep_0)
        ep_0.set_expanded(True)
        ep_0.set_name('render nodes')

        h_s_0 = prx_widgets.PrxHSplitter()
        ep_0.set_widget_add(h_s_0)

        self._filter_tree_view = prx_widgets.PrxTreeView()
        h_s_0.set_widget_add(self._filter_tree_view)
        self._filter_tree_view.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/3.0) - 32
        )
        #
        self._result_list_view = prx_widgets.PrxListView()
        self._result_list_view.set_view_list_mode()
        h_s_0.set_widget_add(self._result_list_view)
        h_s_0.set_stretches([1, 3])
        h_s_0.set_widget_hide_at(0)
        self._result_list_view.set_item_frame_size_basic(*self._item_frame_size)
        self._result_list_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._result_list_view.set_item_icon_size(*self._item_icon_size)
        self._result_list_view.set_item_icon_frame_draw_enable(True)
        self._result_list_view.set_item_name_frame_draw_enable(True)
        self._result_list_view.set_item_names_draw_range([None, 1])
        self._result_list_view.set_item_image_frame_draw_enable(True)

        self._result_list_view.get_top_tool_bar().set_expanded(True)
        self._result_list_view.get_check_tool_box().set_visible(True)
        self._result_list_view.get_scale_switch_tool_box().set_visible(True)

        self._result_list_view.connect_item_select_changed_to(
            self.node_selection_fnc
        )
        self.connect_window_activate_changed_to(
            self.gui_refresh_all_render_nodes
        )

        self._options_prx_node = prx_widgets.PrxNode_('options')
        sa_0.set_widget_add(self._options_prx_node)
        self._options_prx_node.create_ports_by_configure(
            self._session.configure.get('build.node.options'),
        )
        self._options_prx_node.set(
            'submit', self.submit_to_farm
        )

        self.post_setup_fnc()

        self.set_refresh_all()

    def post_setup_fnc(self):
        pass

    def node_selection_fnc(self):
        raise NotImplementedError()

    def set_refresh_all(self):
        raise NotImplementedError()

    def get_all_render_layers(self):
        raise NotImplementedError()

    def gui_add_all_render_nodes(self):
        raise NotImplementedError()

    def gui_refresh_all_render_nodes(self):
        raise NotImplementedError()

    def submit_to_farm(self):
        raise NotImplementedError()


# coding:utf-8
import collections

from lxutil_gui import utl_gui_configure

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_view_for_tree

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_item

import fnmatch


class PrxTreeView(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxViewDef,
    #
    utl_gui_prx_abstract.AbsPrxViewFilterTagDef,
    _utl_gui_prx_wgt_item.AbsPrxTreeDef,
    #
    utl_gui_prx_abstract.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_view_for_tree.QtTreeWidget
    def __init__(self, *args, **kwargs):
        super(PrxTreeView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._prx_h_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_h_tool_bar.widget)
        self._prx_h_tool_bar.set_border_radius(1)
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_h_tool_bar.set_widget_add(self._prx_filer_bar_0)
        #
        self._loading_index = 0
        self._loading_show_index = 0
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_view.setMinimumHeight(42)
        self._qt_view.setMaximumHeight(166667)
        self._qt_view.gui_proxy = self
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._set_prx_tree_def_init_()
        self._qt_view.customContextMenuRequested.connect(
            self.set_menu_show
        )
        self._qt_view.ctrl_f_key_pressed.connect(
            self.set_filter_start
        )
        self._qt_view.f_key_pressed.connect(
            self.set_scroll_to_select_item
        )
        self._prx_filer_bar_0.set_filter_connect_to(self)
        self._gui_menu_raw = []
        self._item_dict = collections.OrderedDict()
        self._loading_item_prxes = []
        self._occurrence_index_current = 0
        #
        self._prx_filter_bar = self._prx_filer_bar_0
        self._keyword_filter_item_prxes = []

    def set_resize_enable(self, boolean):
        self._qt_widget._set_resize_enable_(boolean)

    def set_resize_minimum(self, value):
        self._qt_widget._set_resize_minimum_(value)

    def set_resize_target(self, widget):
        self._qt_widget._set_resize_target_(widget)
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_filter_entry_tip(self, text):
        self._prx_filter_bar.set_entry_tip(text)

    def set_loading_item_add(self, item_prx):
        if not item_prx in self._loading_item_prxes:
            self._loading_item_prxes.append(item_prx)

    def set_loading_item_remove(self, item_prx):
        if item_prx in self._loading_item_prxes:
            self._loading_item_prxes.remove(item_prx)

    def set_loading_update(self):
        self._loading_index += 1
        if self._loading_index % 15 == 0:
            self._loading_show_index += 1
            for i in self._loading_item_prxes:
                i.set_name(
                    'loading {}'.format('.'*(self._loading_show_index % 5))
                )
            #
            utl_gui_qt_core.QtWidgets.QApplication.instance().processEvents(
                utl_gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def set_filter_start(self):
        self._prx_h_tool_bar.set_expanded(True)
        self._prx_filer_bar_0.set_entry_focus(True)

    def get_tool_bar(self):
        return self._prx_filer_bar_0

    def set_scroll_to_select_item(self):
        selection_items = self.view.selectedItems()
        if selection_items:
            self.view._set_scroll_to_item_top_(selection_items[-1])

    def set_selection_use_single(self):
        self._qt_view.setSelectionMode(utl_gui_qt_core.QtWidgets.QAbstractItemView.SingleSelection)

    def set_selection_disable(self):
        self._qt_view.setSelectionMode(utl_gui_qt_core.QtWidgets.QAbstractItemView.NoSelection)

    def set_size_policy_height_fixed_mode(self):
        self._qt_view._set_size_policy_height_fixed_mode_()
    # noinspection PyUnusedLocal
    def set_menu_show(self, *args):
        indices = self.view.selectedIndexes()
        if indices:
            index = indices[-1]
            qt_object = self.view.itemFromIndex(index)
            menu_raw = qt_object.gui_proxy.get_gui_menu_raw()
            menu_content = qt_object._get_menu_content_()
        else:
            menu_raw = self.get_gui_menu_raw()
            menu_content = self.view._get_menu_content_()
        #
        menu = None
        #
        if menu_content:
            if menu is None:
                menu = _utl_gui_prx_wdt_utility.PrxMenu(self.view)
            #
            menu.set_menu_content(menu_content)
            menu.set_show()
        #
        if menu_raw:
            if menu is None:
                menu = _utl_gui_prx_wdt_utility.PrxMenu(self.view)
            menu.set_menu_raw(menu_raw)
            menu.set_show()

    def set_gui_menu_raw(self, data):
        self._gui_menu_raw = data

    def get_gui_menu_raw(self):
        return self._gui_menu_raw

    def _get_all_items_(self):
        return self.view._get_all_items_()

    def get_all_items(self):
        return [i.gui_proxy for i in self.view._get_all_items_() if hasattr(i, 'gui_proxy')]

    def get_all_checked_items(self):
        return [i.gui_proxy for i in self.view._get_all_checked_items_() if hasattr(i, 'gui_proxy')]

    def get_all_leaf_items(self):
        return [i.gui_proxy for i in self.view._get_all_leaf_items_()]

    def get_item_prxes_by_keyword_filter(self, keyword, match_case=False, match_word=False):
        return [i.gui_proxy for i in self.view._get_items_by_keyword_filter_(
            keyword=keyword,
            match_case=match_case,
            match_word=match_word
        )]
    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]

    def get_current_item(self):
        _ = self._qt_view.currentItem()
        if _:
            return _.gui_proxy

    def set_item_selected(self, item_prx, exclusive=False):
        if exclusive is True:
            self.view.setCurrentItem(item_prx.widget)
        else:
            self.view.setItemSelected(item_prx.widget, True)

    def set_item_add(self, *args, **kwargs):
        return self._set_item_add_(
            self.view.addTopLevelItem,
            *args, **kwargs
        )

    def set_clear(self):
        self.view._set_clear_()
        self._item_dict.clear()
        self._loading_item_prxes = []

    def set_restore(self):
        self.set_clear()

    def connect_item_select_changed_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)

    def set_item_check_changed_connect_to(self, fnc):
        self.view.item_check_changed.connect(fnc)

    def set_item_changed_connect_to(self, fnc):
        self.view.itemChanged.connect(fnc)

    def set_item_expand_connect_to(self, prx_item, fnc, time=0):
        self.view._set_item_expand_connect_to_(prx_item.widget, fnc, time)

    def set_all_items_expand(self):
        self.view.expandAll()

    def set_items_expand_by_depth(self, depth):
        qt_items = self.view._get_items_by_depth_(depth)
        for qt_item in qt_items:
            qt_item.setExpanded(True)

    def set_all_items_collapse(self):
        self.view.collapseAll()

    def set_header_view_create(self, data, max_width=0):
        self.view._set_view_header_(data, max_width)

    def set_tag_filter_all_keys_src(self, keys):
        utl_gui_prx_abstract.AbsPrxViewFilterTagDef.set_tag_filter_all_keys_src(
            self, keys
        )
        # self._set_items_hidden_by_any_filter_()
    @classmethod
    def _get_item_tag_filter_tgt_match_args_(cls, prx_item_tgt, tag_filter_all_keys_src):
        tag_filter_tgt_keys = prx_item_tgt.get_tag_filter_tgt_keys()
        tag_filter_tgt_mode = prx_item_tgt.get_tag_filter_tgt_mode()
        if tag_filter_tgt_keys:
            if tag_filter_tgt_mode == utl_gui_configure.TagFilterMode.MatchAll:
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key not in tag_filter_all_keys_src:
                        return True, True
                return True, False
            elif tag_filter_tgt_mode == utl_gui_configure.TagFilterMode.MatchOne:
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key in tag_filter_all_keys_src:
                        return True, False
                return True, True
            return True, False
        return False, False
    @classmethod
    def _get_item_keyword_filter_match_args_(cls, item_prx, keyword):
        if keyword:
            keyword = keyword.lower()
            keyword_filter_keys_tgt = item_prx.get_keyword_filter_keys_tgt() or []
            if keyword_filter_keys_tgt:
                context = '+'.join([i.decode('utf-8') for i in keyword_filter_keys_tgt if i])
            else:
                context = '+'.join([i.decode('utf-8') for i in item_prx.get_names() if i])
            #
            context = context.lower()
            if '*' in keyword:
                filter_key = u'*{}*'.format(keyword.lstrip('*').rstrip('*'))
                if fnmatch.filter([context], filter_key):
                    return True, False
            else:
                filter_key = u'*{}*'.format(keyword)
                if fnmatch.filter([context], filter_key):
                    return True, False
            return True, True
        return False, False

    def _set_items_hidden_by_any_filter_(self):
        tag_filter_all_keys_src = self.view._get_view_tag_filter_data_src_()
        filter_keyword = self._prx_filter_bar.get_keyword()
        self._keyword_filter_item_prxes = []
        #
        prx_items = self.get_all_items()
        for i_prx_item_tgt in prx_items:
            i_tag_filter_hidden_ = False
            i_keyword_filter_hidden_ = False
            if tag_filter_all_keys_src:
                i_tag_filter_is_enable, i_tag_filter_hidden = self._get_item_tag_filter_tgt_match_args_(
                    i_prx_item_tgt, tag_filter_all_keys_src
                )
                if i_tag_filter_is_enable is True:
                    i_tag_filter_hidden_ = i_tag_filter_hidden
            #
            if filter_keyword:
                i_keyword_filter_enable, i_keyword_filter_hidden = self._get_item_keyword_filter_match_args_(
                    i_prx_item_tgt, filter_keyword
                )
                if i_keyword_filter_enable is True:
                    i_keyword_filter_hidden_ = i_keyword_filter_hidden
                    if i_keyword_filter_hidden_ is False:
                        self._keyword_filter_item_prxes.append(i_prx_item_tgt)
            #
            if True in [i_tag_filter_hidden_, i_keyword_filter_hidden_]:
                is_hidden = True
            else:
                is_hidden = False
            #
            i_prx_item_tgt.set_hidden(is_hidden)
            for i in i_prx_item_tgt.get_ancestors():
                if is_hidden is False:
                    i.set_hidden(False)
        #
        self.view._refresh_view_all_items_viewport_showable_()
    @classmethod
    def _get_item_name_colors_(cls, prx_items, column=0):
        lis = []
        for i_prx_item in prx_items:
            item = i_prx_item.widget
            lis.append(item.textColor(column))
        return lis

    def _set_filter_bar_(self, filter_bar):
        self._prx_filter_bar = filter_bar

    def _execute_occurrence_to_current_(self):
        prx_items = self._keyword_filter_item_prxes
        if prx_items:
            idx_cur = 0
            item_prx_pre = prx_items[idx_cur]
            item_prx_pre._set_filter_occurrence_(True)
            self.view._set_scroll_to_item_top_(item_prx_pre.widget)
            self._occurrence_index_current = idx_cur
        else:
            self._occurrence_index_current = None
        #
        self._prx_filter_bar.set_result_index(self._occurrence_index_current)

    def _execute_occurrence_to_previous_(self):
        prx_items = self._keyword_filter_item_prxes
        if prx_items:
            idx_max, idx_min = len(prx_items)-1, 0
            idx = self._occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_prx = prx_items[idx]
            item_prx._set_filter_occurrence_(False)
            #
            if idx == idx_min:
                idx = idx_max
            else:
                idx -= 1
            idx_pre = max(min(idx, idx_max), 0)
            item_prx_pre = prx_items[idx_pre]
            item_prx_pre._set_filter_occurrence_(True)
            self.view._set_scroll_to_item_top_(item_prx_pre.widget)
            self._occurrence_index_current = idx_pre
        else:
            self._occurrence_index_current = None
        #
        self._prx_filter_bar.set_result_index(self._occurrence_index_current)

    def _execute_occurrence_to_next_(self):
        prx_items = self._keyword_filter_item_prxes
        if prx_items:
            idx_max, idx_min = len(prx_items)-1, 0
            idx = self._occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_prx = prx_items[idx]
            item_prx._set_filter_occurrence_(False)
            #
            if idx == idx_max:
                idx = idx_min
            else:
                idx += 1
            idx_pst = max(min(idx, idx_max), 0)
            item_prx_pst = prx_items[idx_pst]
            item_prx_pst._set_filter_occurrence_(True)
            self.view._set_scroll_to_item_top_(item_prx_pst.widget)
            self._occurrence_index_current = idx_pst
        else:
            self._occurrence_index_current = None
        #
        self._prx_filter_bar.set_result_index(self._occurrence_index_current)

    def get_item_by_filter_key(self, filter_key):
        return self._item_dict.get(filter_key)

    def set_item_select_by_filter_key(self, filter_key, exclusive=False):
        item_prx = self.get_item_by_filter_key(filter_key)
        #
        if item_prx is not None:
            self.set_item_selected(item_prx, exclusive=exclusive)
            self.set_scroll_to_select_item()
            # item_prx.set_select()
        #
        self.set_view_update()

    def set_view_update(self):
        self.view.update()

    def connect_refresh_action_to(self, fnc):
        self._qt_view.f5_key_pressed.connect(fnc)

    def set_filter_history_key(self, key):
        self._prx_filter_bar.set_history_key(key)

    def set_filter_completion_gain_fnc(self, fnc):
        self._prx_filter_bar.set_filter_completion_gain_fnc(fnc)

    def set_draw_for_check_state_enable(self, boolean):
        self._qt_view._set_draw_for_check_state_enable_(boolean)

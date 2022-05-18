# coding:utf-8
import collections

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_view, _utl_gui_qt_wgt_item

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_item

from lxutil import utl_core

import fnmatch


class PrxHSplitter(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtHSplitter
    def __init__(self, *args, **kwargs):
        super(PrxHSplitter, self).__init__(*args, **kwargs)

        self._stretches = []

    def set_widget_add(self, widget):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget.addWidget(qt_widget)

    def set_stretches(self, stretches):
        for seq, i in enumerate(stretches):
            self.widget._set_stretch_factor_(seq, i)
        self._stretches = stretches

    def set_widget_hide(self, index):
        widget = self.widget.widget(index)
        if widget:
            widget.setMaximumWidth(0)

    def set_sizes(self, sizes):
        self.widget._set_sizes_(sizes)

    def set_swap_enable(self, boolean):
        self.widget._swap_enable = boolean


class PrxVSplitter(PrxHSplitter):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtVSplitter
    def __init__(self, *args, **kwargs):
        super(PrxVSplitter, self).__init__(*args, **kwargs)


class PrxTabView(utl_gui_prx_abstract.AbsPrxWidget):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtTabView
    def __init__(self, *args, **kwargs):
        super(PrxTabView, self).__init__(*args, **kwargs)

    def set_item_add(self, widget, *args, **kwargs):
        if isinstance(widget, utl_gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget._set_item_add_(qt_widget, *args, **kwargs)


class AbsPrxViewDef(object):
    @property
    def view(self):
        raise NotImplementedError()
    #
    def set_item_select_changed_connect_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)
    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]


class PrxTreeView(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxViewDef,
    #
    utl_gui_prx_abstract.AbsPrxViewFilterTagDef,
    _utl_gui_prx_wgt_item.AbsPrxTreeDef,
    #
    utl_gui_prx_abstract.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_view.QtTreeWidget
    def __init__(self, *args, **kwargs):
        super(PrxTreeView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)
        self._qt_layout_0.setSpacing(2)
        self._prx_tool_bar_0 = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_tool_bar_0.widget)
        self._prx_tool_bar_0.set_border_radius(4)
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_tool_bar_0.set_widget_add(self._prx_filer_bar_0)
        #
        self._loading_index = 0
        self._loading_show_index = 0
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
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
        self._match_occurrence_index = 0
        #
        self._prx_filter_bar = self._prx_filer_bar_0
        self._keyword_filter_item_prxes = []
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

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
        self._prx_tool_bar_0.set_expanded(True)
        self._prx_filer_bar_0.set_entry_focus(True)

    def get_tool_bar(self):
        return self._prx_filer_bar_0

    def set_scroll_to_select_item(self):
        selection_items = self.view.selectedItems()
        if selection_items:
            self.view._set_scroll_to_item_top_(selection_items[-1])

    def set_single_selection(self):
        self.view.setSelectionMode(utl_gui_qt_core.QtWidgets.QAbstractItemView.SingleSelection)

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

    def _get_view_items_(self):
        return self.view._get_view_items_()

    def get_all_items(self):
        return [i.gui_proxy for i in self.view._get_view_items_() if hasattr(i, 'gui_proxy')]

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

    def set_item_select_changed_connect_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)

    def set_item_check_changed_connect_to(self, fnc):
        self.view.item_checked.connect(fnc)

    def set_item_changed_connect_to(self, fnc):
        self.view.itemChanged.connect(fnc)

    def set_item_expand_connect_to(self, item_prx, fnc, time=0):
        self.view._set_item_expand_connect_to_(item_prx.widget, fnc, time)

    def set_all_items_expand(self):
        self.view.expandAll()

    def set_items_expand_by_depth(self, depth):
        qt_items = self.view._get_items_by_depth_(depth)
        for qt_item in qt_items:
            qt_item.setExpanded(True)

    def set_all_items_collapse(self):
        self.view.collapseAll()

    def set_header_view_create(self, data, max_width):
        self.view._set_view_header_(data, max_width)

    def set_tag_filter_tgt_keys(self, keys):
        utl_gui_prx_abstract.AbsPrxViewFilterTagDef.set_tag_filter_tgt_keys(
            self, keys
        )
        # self._set_items_hidden_by_any_filter_()
    @classmethod
    def _get_item_tag_filter_tgt_match_args_(cls, prx_item_tgt, tag_filter_src_all_keys):
        tag_filter_tgt_keys = prx_item_tgt.get_tag_filter_tgt_keys()
        tag_filter_tgt_mode = prx_item_tgt.get_tag_filter_tgt_mode()
        if tag_filter_tgt_keys:
            if tag_filter_tgt_mode == 'A+B':
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key not in tag_filter_src_all_keys:
                        return True, True
            elif tag_filter_tgt_mode == 'A/B':
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key in tag_filter_src_all_keys:
                        return True, False
            return True, False
        return False, False
    @classmethod
    def _get_item_keyword_filter_match_args_(cls, item_prx, keyword):
        if keyword:
            keyword = keyword.lower()
            keyword_filter_contexts = item_prx.get_keyword_filter_tgt_contexts() or []
            if keyword_filter_contexts:
                context = u'+'.join(keyword_filter_contexts)
            else:
                context = u'+'.join([i for i in item_prx.get_names() if i])
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
        tag_filter_src_all_keys = self.view._get_view_tag_filter_tgt_keys_()
        filter_keyword = self._prx_filter_bar.get_keyword()
        self._keyword_filter_item_prxes = []
        #
        item_prxes = self.get_all_items()
        for prx_item_tgt in item_prxes:
            i_tag_filter_hidden_ = False
            i_keyword_filter_hidden_ = False
            if tag_filter_src_all_keys:
                i_tag_filter_is_enable, i_tag_filter_hidden = self._get_item_tag_filter_tgt_match_args_(
                    prx_item_tgt, tag_filter_src_all_keys
                )
                if i_tag_filter_is_enable is True:
                    i_tag_filter_hidden_ = i_tag_filter_hidden
            #
            if filter_keyword:
                i_keyword_filter_enable, i_keyword_filter_hidden = self._get_item_keyword_filter_match_args_(
                    prx_item_tgt, filter_keyword
                )
                if i_keyword_filter_enable is True:
                    i_keyword_filter_hidden_ = i_keyword_filter_hidden
            #
            if True in [i_tag_filter_hidden_, i_keyword_filter_hidden_]:
                is_hidden = True
            else:
                is_hidden = False
            #
            prx_item_tgt.set_hidden(is_hidden)
            for i in prx_item_tgt.get_ancestors():
                if is_hidden is False:
                    i.set_hidden(False)
        #
        self.view._set_view_items_show_update_()
    @classmethod
    def _get_item_name_colors_(cls, item_prxes, column=0):
        lis = []
        for item_prx in item_prxes:
            item = item_prx.widget
            lis.append(item.textColor(column))
        return lis

    def _set_filter_bar_(self, filter_bar):
        self._prx_filter_bar = filter_bar

    def _set_scroll_to_pre_occurrence_match_item_(self):
        item_prxes = self._keyword_filter_item_prxes
        if item_prxes:
            idx_max, idx_min = len(item_prxes)-1, 0
            idx = self._match_occurrence_index or 0
            if idx == idx_min:
                idx = idx_max
            #
            idx = max(min(idx, idx_max), 0)
            item_prx = item_prxes[idx]
            item_prx._set_filter_occurrence_(False)
            #
            idx -= 1
            idx_pre = max(min(idx, idx_max), 0)
            item_prx_pre = item_prxes[idx_pre]
            item_prx_pre._set_filter_occurrence_(True)
            self.view._set_scroll_to_item_top_(item_prx_pre.widget)
            self._match_occurrence_index = idx_pre
        else:
            self._match_occurrence_index = None
        #
        self._prx_filter_bar.set_result_index(self._match_occurrence_index)

    def _set_scroll_to_pst_occurrence_match_item_(self):
        item_prxes = self._keyword_filter_item_prxes
        if item_prxes:
            idx_max, idx_min = len(item_prxes)-1, 0
            idx = self._match_occurrence_index or 0
            if idx == idx_max:
                idx = idx_min
            #
            idx = max(min(idx, idx_max), 0)
            item_prx = item_prxes[idx]
            item_prx._set_filter_occurrence_(False)
            #
            idx += 1
            idx_pst = max(min(idx, idx_max), 0)
            item_prx_pst = item_prxes[idx_pst]
            item_prx_pst._set_filter_occurrence_(True)
            self.view._set_scroll_to_item_top_(item_prx_pst.widget)
            self._match_occurrence_index = idx_pst
        else:
            self._match_occurrence_index = None
        #
        self._prx_filter_bar.set_result_index(self._match_occurrence_index)

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


class PrxListView(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxViewDef,
    #
    utl_gui_prx_abstract.AbsPrxViewFilterTagDef,
    #
    utl_gui_prx_abstract.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_view.QtListWidget
    def __init__(self, *args, **kwargs):
        super(PrxListView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)
        self._qt_layout_0.setSpacing(2)
        self._prx_tool_bar_0 = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_tool_bar_0.widget)
        self._prx_tool_bar_0.set_border_radius(4)
        self._view_mode_swap_button = _utl_gui_qt_wgt_item._QtIconPressItem()
        self._view_mode_swap_button._set_icon_file_path_(utl_core.Icon.get('grid_mode'))
        self._view_mode_swap_button.clicked.connect(self.set_view_mode_swap)
        self._prx_tool_bar_0.set_widget_add(self._view_mode_swap_button)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_tool_bar_0.set_widget_add(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_layout_0.addWidget(self._qt_view)
        self._set_prx_view_def_init_(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_view_mode_swap(self):
        self.view._set_view_mode_swap_()
        self._view_mode_swap_button._set_icon_file_path_(
            utl_core.Icon.get(['list_mode', 'grid_mode'][self.view._get_is_grid_mode_()])
        )

    def set_list_mode(self):
        self.view._set_list_mode_()

    def set_grid_mode(self):
        self.view._set_grid_mode_()
    #
    def set_item_frame_size(self, w, h):
        self.view._set_item_frame_size_(w, h)

    def set_item_frame_draw_enable(self, boolean):
        self.view._set_item_frame_draw_enable_(boolean)

    def set_item_icon_frame_size(self, w, h):
        self.view._set_item_icon_frame_size_(w, h)
        self.view._set_item_icon_size_(w-4, h-4)

    def set_item_icon_size(self, w, h):
        self.view._set_item_icon_size_(w, h)

    def set_item_icon_frame_draw_enable(self, boolean):
        self.view._set_item_icon_frame_draw_enable_(boolean)

    def set_item_name_frame_size(self, w, h):
        self.view._set_item_name_frame_size_(w, h)
        self.view._set_item_name_size_(w-4, h-4)

    def set_item_name_size(self, w, h):
        self.view._set_item_name_size_(w, h)

    def set_item_name_frame_draw_enable(self, boolean):
        self.view._set_item_name_frame_draw_enable_(boolean)

    def set_item_image_frame_draw_enable(self, boolean):
        self.view._set_item_image_frame_draw_enable_(boolean)
    #
    def set_item_add(self, *args, **kwargs):
        item_widget_prx = _utl_gui_prx_wgt_item.PrxListItem()
        item_widget_prx.set_view(self)
        self.view._set_item_widget_add_(item_widget_prx.widget, **kwargs)
        return item_widget_prx

    def set_visible_tgt_raw_clear(self):
        self.set_visible_tgt_raw({})

    def set_visible_tgt_raw_update(self):
        dic = {}
        item_prxes = self.get_all_items()
        for item_prx in item_prxes:
            tgt_key = item_prx.get_visible_tgt_key()
            if tgt_key is not None:
                dic.setdefault(
                    tgt_key, []
                ).append(item_prx)
        #
        self.set_visible_tgt_raw(dic)

    def set_visible_tgt_raw(self, raw):
        self.set_gui_attribute(
            'visible_tgt_raw',
            raw
        )

    def get_visible_tgt_raw(self):
        return self.get_gui_attribute('visible_tgt_raw')

    def set_clear(self):
        self.view._set_clear_()

    def _get_view_items_(self):
        return self.view._get_view_items_()

    def get_all_items(self):
        return [i._get_item_widget_().gui_proxy for i in self.view._get_view_items_()]

    def set_loading_update(self):
        self.view._set_loading_update_()


class PrxGuideBar(
    utl_gui_prx_abstract.AbsPrxWidget,
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_view._QtGuideBar
    def __init__(self, *args, **kwargs):
        super(PrxGuideBar, self).__init__(*args, **kwargs)

    def set_path_args(self, path_args):
        self.widget._set_view_path_args_(path_args)

    def set_item_contents_at(self, content, index=0):
        self.widget._set_choose_item_content_at_(content, index)

    def get_current_path(self):
        return self.widget._get_view_guide_current_path_()

    def set_item_clicked_connect_to(self, fnc):
        self.widget.guide_item_clicked.connect(fnc)

    def set_item_double_clicked_connect_to(self, fnc):
        self.widget.guide_item_double_clicked.connect(fnc)

    def set_item_changed_connect_to(self, fnc):
        self.widget.choose_item_changed.connect(fnc)

    def set_clear(self):
        self.widget._set_view_guide_and_choose_clear_()

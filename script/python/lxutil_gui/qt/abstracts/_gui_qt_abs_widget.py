# coding:utf-8
from lxutil_gui.qt.abstracts._gui_qt_abs_basic import *


class AbsQtTreeWidget(
    QtWidgets.QTreeWidget,
    AbsQtMenuDef,
    #
    AbsQtViewFilterDef,
    #
    AbsQtViewStateDef,
    AbsQtViewVisibleConnectionDef,
    #
    AbsQtViewScrollActionDef,
    AbsQtBuildViewDef,
    AbsQtShowForViewDef
):
    def __init__(self, *args, **kwargs):
        super(AbsQtTreeWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._set_menu_def_init_()
        #
        self._set_view_filter_def_init_()
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()

        self._set_view_scroll_action_def_init_()
        # noinspection PyUnresolvedReferences
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._refresh_view_all_items_viewport_showable_auto_
        )
        #
        self._set_build_view_def_init_()
        self._set_build_view_setup_(self)

        self._set_show_for_view_def_init_(self)

    def _get_all_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                lis.append(self.itemFromIndex(index_))
            #
            for i_row in range(row_count):
                if index_ is None:
                    _index = model.index(i_row, column)
                else:
                    _index = index_.child(i_row, index_.column())
                #
                if _index.isValid():
                    _rcs_fnc(_index)

        lis = []
        model = self.model()

        _rcs_fnc(None)
        return lis

    def _get_all_checked_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
            #
            for i_row in range(row_count):
                if index_ is None:
                    _i_index = model.index(i_row, column)
                else:
                    _i_index = index_.child(i_row, index_.column())
                #
                if _i_index.isValid():
                    if _i_index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
                        list_.append(self.itemFromIndex(_i_index))
                        _rcs_fnc(_i_index)

        list_ = []
        model = self.model()

        _rcs_fnc(None)
        return list_

    def _set_view_header_(self, raw, max_width=0):
        texts, width_ps = zip(*raw)
        count = len(texts)
        #
        self.setColumnCount(count)
        self.setHeaderLabels(texts)
        set_column_enable = count > 1
        w = 0
        if set_column_enable is True:
            max_division = sum(width_ps)
            w = int(max_width/max_division)
        #
        for index in range(0, count):
            if set_column_enable is True:
                self.setColumnWidth(index, w*(width_ps[index]))
            #
            icon = QtGui.QIcon()
            p = QtGui.QPixmap(16, 16)
            p.load(utl_gui_core.RscIconFile.get('qt-style/line-v'))
            icon.addPixmap(
                p,
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
            #
            self.headerItem().setBackground(index, Brush.BACKGROUND_NORMAL)
            self.headerItem().setForeground(index, QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
            self.headerItem().setFont(index, Font.NAME)
            # todo: in katana will make text display error, PyQt?
            if LOAD_INDEX == 1:
                self.headerItem().setIcon(index, icon)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_selection_disable_(self):
        self.setSelectionMode(
            self.NoSelection
        )

    def _set_filter_style_(self):
        pass


class AbsQtListWidget(
    QtWidgets.QListWidget,
    #
    AbsQtViewSelectActionDef,
    AbsQtViewScrollActionDef,
    #
    AbsQtViewFilterDef,
    AbsQtViewStateDef,
    AbsQtViewVisibleConnectionDef,
    AbsQtBuildViewDef,
    AbsQtShowForViewDef
):
    item_show_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(AbsQtListWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._set_view_select_action_def_init_()
        self._set_view_scroll_action_def_init_()
        #
        self._set_view_filter_def_init_()
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()
        #
        self.itemSelectionChanged.connect(self._set_item_select_update_)
        self.itemSelectionChanged.connect(self._set_item_widget_selected_update_)
        # noinspection PyUnresolvedReferences
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._refresh_view_all_items_viewport_showable_auto_
        )
        self._viewport_rect = QtCore.QRect()
        self._item_rects = []
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QListView')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        #
        self._set_build_view_def_init_()
        self._set_build_view_setup_(self)

        self._set_show_for_view_def_init_(self)

    def _set_drag_enable_(self, boolean):
        super(AbsQtListWidget, self)._set_drag_enable_(boolean)
        # self.acceptDrops()
        # self.setDragEnabled(True)
        self.setDragDropMode(self.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_view_item_selected_(self, item, boolean):
        self.setItemSelected(item, boolean)

    def _get_selected_items_(self):
        return self.selectedItems()

    def _set_item_widget_selected_(self, item, boolean):
        item_widget = self.itemWidget(item)
        if item_widget:
            item_widget._set_selected_(boolean)
    # select
    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _get_selected_item_widget_(self):
        item_widgets = self._get_selected_item_widgets_()
        if item_widgets:
            return item_widgets[-1]

    def _get_checked_item_widgets_(self):
        return [i for i in self._get_all_item_widgets_() if i._get_is_checked_() is True]

    def _set_item_select_update_(self):
        pass

    def _set_item_widget_selected_update_(self):
        if self._pre_selected_items:
            [self._set_item_widget_selected_(i, False) for i in self._pre_selected_items]
        #
        selected_items = self._get_selected_items_()
        if selected_items:
            [self._set_item_widget_selected_(i, True) for i in selected_items]
            self._pre_selected_items = selected_items

    # scroll
    def _set_scroll_to_item_top_(self, item):
        self.scrollToItem(item, self.PositionAtTop)

    def _set_scroll_to_selected_item_top_(self):
        selected_items = self._get_selected_items_()
        if selected_items:
            item = selected_items[-1]
            self._set_scroll_to_item_top_(item)

    def _get_grid_size_(self):
        s = self.gridSize()
        return s.width(), s.width()

    def _refresh_widget_draw_(self):
        self.update()
        self.viewport().update()
    #
    def _get_viewport_size_(self):
        return self.viewport().width(), self.viewport().height()

    def _get_all_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _get_all_item_count_(self):
        return self.count()

    def _get_all_item_widgets_(self):
        return [self.itemWidget(self.item(i)) for i in range(self.count())]

    def _get_selected_visible_items_(self):
        return [i for i in self.selectedItems() if i.isHidden() is False]

    def _get_selected_visible_indices_(self):
        return [self.indexFromItem(i) for i in self._get_selected_visible_items_()]

    def _set_all_items_selected_(self, boolean):
        for i in range(self.count()):
            i_item = self.item(i)
            i_item.setSelected(boolean)
            self.itemWidget(i_item)._set_selected_(boolean)

    def _get_visible_items_(self):
        return [i for i in self._get_all_items_() if i.isHidden() is False]

    def _get_visible_indices_(self):
        return [self.indexFromItem(i) for i in self._get_visible_items_() if i.isHidden() is False]

    def _set_loading_update_(self):
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._set_item_show_kill_all_()
            i._set_item_show_stop_all_()
        #
        self._pre_selected_items = []
        #
        self.clear()

    def _set_scroll_to_pre_item_(self):
        # use visible indices for filter by visible
        indices = self._get_visible_indices_()
        if indices:
            selected_indices = self._get_selected_visible_indices_()
            if selected_indices:
                index_values = [i.row() for i in indices]
                selected_index_values = [i.row() for i in selected_indices]
                #
                idx = index_values.index(selected_index_values[0])
                idx_max, idx_min = len(indices) - 1, 0
                #
                idx = max(min(idx, idx_max), 0)
                #
                if idx == idx_min:
                    idx = idx_max
                else:
                    idx -= 1
                #
                idx_pre = max(min(idx, idx_max), 0)
                index_pre = indices[idx_pre]
                item_pre = self.itemFromIndex(index_pre)
                item_pre.setSelected(True)
                self._set_scroll_to_item_top_(item_pre)
            else:
                item = self.itemFromIndex(indices[0])
                item.setSelected(True)
                self._set_scroll_to_item_top_(item)
                return

    def _set_scroll_to_next_item_(self):
        indices = self._get_visible_indices_()
        if indices:
            selected_indices = self._get_selected_visible_indices_()
            if selected_indices:
                index_values = [i.row() for i in indices]
                selected_index_values = [i.row() for i in selected_indices]
                #
                idx = index_values.index(selected_index_values[0])
                idx_max, idx_min = len(indices) - 1, 0
                #
                idx = max(min(idx, idx_max), 0)
                if idx == idx_max:
                    idx = idx_min
                else:
                    idx += 1
                idx_next = max(min(idx, idx_max), 0)
                index_next = indices[idx_next]
                item_next = self.itemFromIndex(index_next)
                item_next.setSelected(True)
                self._set_scroll_to_item_top_(item_next)
            else:
                item = self.itemFromIndex(indices[0])
                item.setSelected(True)
                self._set_scroll_to_item_top_(item)
                return

    def _set_item_widget_delete_(self, item):
        item_widget = self.itemWidget(item)
        if item_widget:
            item_widget.deleteLater()

    def _set_item_delete_(self, item):
        print item.index()

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )

    def _get_item_current_(self):
        return self.currentItem()

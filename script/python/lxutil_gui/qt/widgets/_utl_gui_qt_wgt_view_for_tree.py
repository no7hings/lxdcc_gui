# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui import utl_gui_core


class QtTreeWidget(
    utl_gui_qt_abstract.AbsQtTreeWidget
):
    PEN_BRANCH = QtGui.QPen(Brush.tree_branch, DpiScale(1))
    PEN_BRANCH_HIGHLIGHT = QtGui.QPen(Brush.tree_branch_highlight, DpiScale(1))
    cachedAncestors = None
    _is_expand_descendants = False
    #
    item_checked = qt_signal()
    item_toggled = qt_signal(bool)
    #
    filter_changed = qt_signal()
    #
    ctrl_f_key_pressed = qt_signal()
    f5_key_pressed = qt_signal()
    f_key_pressed = qt_signal()
    #
    item_expanded = qt_signal(str)
    item_extend_expanded = qt_signal(list)
    def __init__(self, *args, **kwargs):
        super(QtTreeWidget, self).__init__(*args, **kwargs)
        self.setIndentation(20)
        self.setAutoFillBackground(True)
        self.setSortingEnabled(True)
        self.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.setDragEnabled(True)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setVerticalScrollMode(self.ScrollPerItem)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(self.ScrollPerItem)
        self.setAllColumnsShowFocus(True)
        self.setUniformRowHeights(True)
        self.setExpandsOnDoubleClick(False)
        self.setEditTriggers(self.NoEditTriggers)
        self.setDragDropMode(self.DragOnly)
        self.setSelectionMode(self.ExtendedSelection)
        # self.setWordWrap(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setItemDelegate(
            _utl_gui_qt_wgt_utility.QtStyledItemDelegate()
        )
        #
        self.setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QTreeView')
        )
        # header view
        self.header().setFixedHeight(16)
        # self.header().setStretchLastSection(False)
        self.header().setHighlightSections(True)
        self.header().setSortIndicatorShown(True)
        self.header().setCascadingSectionResizes(True)
        # self.header().setResizeContentsPrecision(True)
        self.header().setPalette(QtDccMtd.get_palette())
        # self.header().setSectionResizeMode(self.header().ResizeToContents)
        self.header().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QHeaderView')
        )
        self.header().setFont(Font.NAME)
        self.header().setAutoFillBackground(True)
        # noinspection PyUnresolvedReferences
        self.header().sortIndicatorChanged.connect(
            self._refresh_view_items_viewport_showable_by_sort_
        )
        # self.setAlternatingRowColors(True)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        # self.setAutoFillBackground(True)
        #
        self.cachedAncestors = set()
        # font
        self.setFont(Font.NAME)
        #
        self._selected_indices = []
        self._selected_indirect_indices = []
        #
        self.expanded.connect(self._set_item_action_expand_execute_at_)
        self.collapsed.connect(self._set_item_action_collapse_execute_at_)
        #
        self.itemSelectionChanged.connect(self._set_item_selected_update_)
        # self.itemChanged.connect(self._set_item_changed_update_)
        #
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._item_expand_method_dic = {}
        #
        self.verticalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QScrollBar')
        )

        self.itemDoubleClicked.connect(
            self._set_item_db_clicked_emit_send_
        )
        self.itemClicked.connect(
            self._set_item_clicked_emit_send_
        )

    def drawBranches(self, painter, rect, index):
        # Get the indention level of the row
        level = 0
        tmpIndex = index.parent()
        while tmpIndex.isValid():
            level += 1
            tmpIndex = tmpIndex.parent()

        # Is the row highlighted (selected) ?
        highlight = self.selectionModel().isSelected(index)

        # Line width
        lineWidth = DpiScale(1)

        # Cell width
        cellWidth = int(rect.width() / (level + 1))

        # Current cell to draw in
        x = rect.x() + cellWidth * level
        y = rect.y()
        w = cellWidth
        h = rect.height()

        # Center of the cell
        cx = x + int(w / 2) - int(lineWidth / 2)
        cy = y + int(h / 2) - int(lineWidth / 2)

        # Backup the old pen
        oldPen = painter.pen()

        # Draw the branch indicator on the right most
        if self._get_item_has_visible_children_by_index_(index):
            # Branch icon properties
            rectRadius = DpiScale(4)
            crossMargin = DpiScale(1)
            # Is the row expanded ?
            isExpanded = self.isExpanded(index)
            # [+] and [-] are using different color when highlighted
            painter.setPen(self.PEN_BRANCH_HIGHLIGHT if highlight else self.PEN_BRANCH)
            # Draw a rectangle [ ] as the branch indicator
            painter.drawRect(
                cx - rectRadius,
                cy - rectRadius,
                rectRadius * 2,
                rectRadius * 2
            )
            # Draw the '-' into the rectangle. i.e. [-]
            painter.drawLine(
                cx - rectRadius + crossMargin + lineWidth,
                cy,
                cx + rectRadius - crossMargin - lineWidth,
                cy
            )
            # Draw the '|' into the rectangle. i.e. [+]
            if not isExpanded:
                painter.drawLine(
                    cx,
                    cy - rectRadius + crossMargin + lineWidth,
                    cx,
                    cy + rectRadius - crossMargin - lineWidth
                )

            # Other ornaments are not highlighted
            painter.setPen(self.PEN_BRANCH)
            # Draw the '|' on the bottom. i.e. [-]
            #                                   |
            if isExpanded:
                painter.drawLine(
                    cx,
                    cy + rectRadius + crossMargin + lineWidth,
                    cx,
                    y + h
                )

            # Draw more ornaments when the row is not a top level row
            if level > 0:
                # Draw the '-' on the left. i.e. --[+]
                painter.drawLine(
                    x,
                    cy,
                    cx - rectRadius - crossMargin - lineWidth,
                    cy
                )
        else:
            # Circle is not highlighted
            painter.setPen(self.PEN_BRANCH)
            # Draw the line and circle. i.e. --o
            if level > 0:
                painter.drawLine(x, cy, cx, cy)
                # Backup the old brush
                oldBrush = painter.brush()
                painter.setBrush(self.PEN_BRANCH.brush())
                # A filled circle
                circleRadius = DpiScale(2)
                painter.drawEllipse(
                    cx - circleRadius,
                    cy - circleRadius,
                    circleRadius * 2,
                    circleRadius * 2
                )

                # Restore the old brush
                painter.setBrush(oldBrush)
        # Draw other vertical and horizental lines on the left of the indicator
        if level > 0:
            # Move cell window to the left
            x -= cellWidth
            cx -= cellWidth
            _below_is_visible = self._get_item_below_is_visible_by_index_(index)
            if _below_is_visible is True:
                # The row has more siblings. i.e. |
                #                                 |--
                #                                 |
                painter.drawLine(cx, y, cx, y + h)
                painter.drawLine(cx, cy, x + w, cy)
            else:
                # The row is the last row.   i.e. |
                #                                 L--
                painter.drawLine(cx, y, cx, cy)
                painter.drawLine(cx, cy, x + w, cy)
            # More vertical lines on the left. i.e. ||||-
            tmpIndex = index.parent()
            for i in range(0, level - 1):
                # Move the cell window to the left
                x -= cellWidth
                cx -= cellWidth
                # Draw vertical line if the row has silbings at this level
                _below_is_visible = self._get_item_below_is_visible_by_index_(tmpIndex)
                if _below_is_visible is True:
                    painter.drawLine(cx, y, cx, y + h)
                tmpIndex = tmpIndex.parent()
        # Restore the old pen
        painter.setPen(oldPen)

    def drawRow(self, painter, option, index):
        #
        if index in self._selected_indices:
            painter.fillRect(option.rect, QtBackgroundColors.ItemSelected)
        elif index in self._selected_indirect_indices:
            painter.fillRect(option.rect, QtBackgroundColors.ItemSelectedIndirect)
        #
        super(QtTreeWidget, self).drawRow(painter, option, index)
        #
        QtTreeMtd._set_item_row_draw_(painter, option, index)

    def keyPressEvent(self, event):
        # override space action
        if event.key() == QtCore.Qt.Key_Space:
            pass
        else:
            super(QtTreeWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self._is_expand_descendants = True
        #
        super(QtTreeWidget, self).mousePressEvent(event)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                pass
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
                    self.ctrl_f_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_F:
                    self.f_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Space:
                    pass
                elif event.key() == QtCore.Qt.Key_F5:
                    self.f5_key_pressed.emit()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility.QtEntryFrame):
                    parent._set_focused_(False)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_view_all_items_viewport_showable_()
        return False

    def mouseReleaseEvent(self, event):
        # Handle mouse release event
        super(QtTreeWidget, self).mouseReleaseEvent(event)
        # Reset flags
        self._is_expand_descendants = False

    def paintEvent(self, event):
        if not self.topLevelItemCount():
            painter = QtPainter(self.viewport())
            painter._set_empty_draw_by_rect_(
                self.rect()
            )
        #
        super(QtTreeWidget, self).paintEvent(event)
    @classmethod
    def _set_item_db_clicked_emit_send_(cls, item, column):
        item._signals.press_db_clicked.emit(item, column)
    @classmethod
    def _set_item_clicked_emit_send_(cls, item, column):
        item._signals.press_clicked.emit(item, column)

    def _set_size_policy_height_fixed_mode_(self):
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

    def _get_item_visible_children_by_index_(self, index):
        list_ = []
        row_count = self.model().rowCount(index)
        for i_row in range(row_count):
            i_index = index.child(i_row, index.column())
            i_item = self.itemFromIndex(i_index)
            if i_item is not None:
                if i_item.isHidden() is True:
                    continue
                list_.append(i_item)
        return list_

    def _get_item_children_by_index_(self, index):
        list_ = []
        row_count = self.model().rowCount(index)
        for i_row in range(row_count):
            i_index = index.child(i_row, index.column())
            i_item = self.itemFromIndex(i_index)
            if i_item is not None:
                list_.append(i_item)
        return list_

    def _get_item_juxtaposed_by_index_(self, index):
        parent_index = index.parent()
        if parent_index.isValid():
            return self._get_item_children_by_index_(parent_index)
        else:
            return []

    def _get_all_expanded_items_(self, index):
        def rcs_fnc_(index_):
            _row_count = self.model().rowCount(index_)
            for _i_row in range(_row_count):
                _i_index = index_.child(_i_row, index_.column())
                _i_item = self.itemFromIndex(_i_index)
                if _i_item is not None:
                    list_.append(_i_item)
                    if _i_item.isExpanded() is True:
                        rcs_fnc_(_i_index)

        list_ = []
        parent_index = index.parent()
        if parent_index.isValid():
            rcs_fnc_(parent_index)
        else:
            indices = [self.indexFromItem(self.topLevelItem(i)) for i in range(self.topLevelItemCount())]
            [rcs_fnc_(i) for i in indices]
        return list_

    def _get_item_has_visible_children_by_index_(self, index):
        row_count = self.model().rowCount(index)
        for i_row in range(row_count):
            i_index = index.child(i_row, index.column())
            if i_index.isValid():
                if self.itemFromIndex(i_index).isHidden() is False:
                    return True
        return False

    def _get_item_is_visible_by_index_(self, index):
        if index.isValid():
            return not self.itemFromIndex(index).isHidden()
        return False

    def _get_item_below_is_visible_by_index_(self, index):
        def _rcs_fnc(_index):
            _nxt_index = index.sibling(_index.row() + 1, _index.column())
            if _nxt_index.isValid():
                if self.itemFromIndex(_nxt_index).isHidden() is True:
                    return _rcs_fnc(_nxt_index)
                return True
            return False
        return _rcs_fnc(index)

    def _set_selected_indices_update_(self):
        self._selected_indices = self.selectionModel().selectedIndexes() or []

    def _set_selected_indirect_indices_update_(self):
        self._selected_indirect_indices = []
        for index in self._selected_indices:
            all_parent_indices = QtTreeMtd._get_index_ancestor_indices_(index)
            [
                self._selected_indirect_indices.append(i)
                for i in all_parent_indices if
                i not in self._selected_indirect_indices
                and i not in self._selected_indices
            ]

    def _get_items_selected_(self):
        return [self.itemFromIndex(i) for i in self._selected_indices]

    def _get_items_by_keyword_filter_(self, keyword, match_case=False, match_word=False):
        list_ = []
        if keyword:
            column_count = self.columnCount()
            #
            i_ids = []
            for column in range(column_count):
                qt_match_flags = QtCore.Qt.MatchRecursive | QtCore.Qt.MatchContains
                match_flags = [match_case, match_word]
                if match_flags == [False, False]:
                    qt_match_flags = QtCore.Qt.MatchRecursive | QtCore.Qt.MatchContains
                if match_flags == [False, True]:
                    qt_match_flags = QtCore.Qt.MatchRecursive | QtCore.Qt.MatchFixedString
                elif match_flags == [True, False]:
                    qt_match_flags = QtCore.Qt.MatchRecursive | QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchContains
                elif match_flags == [True, True]:
                    qt_match_flags = QtCore.Qt.MatchRecursive | QtCore.Qt.MatchExactly
                #
                items = self.findItems(
                    keyword,
                    qt_match_flags,
                    column=column
                )
                for item in items:
                    i_index = self.indexFromItem(item, column=column)
                    i_id = i_index.internalId()
                    if not i_id in i_ids:
                        i_ids.append(i_id)
                        list_.append(item)
        else:
            pass
        return list_

    def _set_item_selected_update_(self):
        if self.selectionModel().hasSelection():
            self._set_selected_indices_update_()
            self._set_selected_indirect_indices_update_()
        else:
            self._selected_indices = []
            self._selected_indirect_indices = []
        #
        self.update()

    def _set_item_changed_update_(self, item, column=0):
        pass

    def _set_item_action_expand_execute_at_(self, index):
        def fnc_():
            method()
            timer.stop()
        #
        if self._is_expand_descendants:
            self._is_expand_descendants = False
            self._set_item_extend_expanded_at__(index, True)
        #
        item = self.itemFromIndex(index)
        if item in self._item_expand_method_dic:
            method, time = self._item_expand_method_dic[item]
            if time == 0:
                method()
            else:
                timer = QtCore.QTimer(self)
                timer.timeout.connect(fnc_)
                timer.start(time)
        #
        self._set_item_expanded_update_at_(index)

    def _set_item_action_collapse_execute_at_(self, index):
        if self._is_expand_descendants:
            self._is_expand_descendants = False
            self._set_item_extend_expanded_at__(index, False)

        self._set_item_collapse_at_(index)

        self._set_item_expanded_update_at_(index)

    def _set_item_extend_expanded_at__(self, index, boolean):
        for i in range(0, index.model().rowCount(index)):
            i_child_index = index.child(i, 0)
            self.setExpanded(i_child_index, boolean)
            self._set_item_extend_expanded_at__(i_child_index, boolean)

    def _set_item_extend_expanded_at_(self, index, boolean):
        indices = self._get_descendant_indices_at_(index)
        [self.setExpanded(i, boolean) for i in indices]
    @classmethod
    def _get_descendant_indices_at_(cls, index):
        def rcs_fnc_(list__, index_):
            for _i in range(0, index.model().rowCount(index_)):
                _i_child_index = index.child(_i, 0)
                list__.append(_i_child_index)

        list_ = []
        rcs_fnc_(list_, index)
        return list_

    def _set_item_expanded_update_at_(self, index):
        list_ = self._get_all_expanded_items_(index)
        for i in list_:
            i._set_item_show_start_auto_()

    def _set_item_collapse_at_(self, index):
        list_ = []

        item = self.itemFromIndex(index)
        parent = item.parent()
        if parent is not None:
            list_.extend(
                parent._get_children_()
            )
        else:
            list_.extend(
                [self.topLevelItem(i) for i in range(self.topLevelItemCount())]
            )

        for i in list_:
            i._set_item_show_start_auto_()

    def _set_item_expand_connect_to_(self, item, method, time):
        self._item_expand_method_dic[item] = method, time

    def _set_item_check_action_run_(self, item, column):
        if item._get_emit_send_enable_() is True:
            # noinspection PyUnresolvedReferences
            self.item_checked.emit()

    def _set_item_toggle_emit_send_(self, item, column, boolean):
        if item._get_emit_send_enable_() is True:
            # noinspection PyUnresolvedReferences
            self.item_toggled.emit(boolean)

    def _set_filter_emit_send_(self):
        self.filter_changed.emit()

    def _get_all_leaf_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                if row_count == 0:
                    list_.append(self.itemFromIndex(index_))
            #
            for i_row in range(row_count):
                if index_ is None:
                    _index = model.index(i_row, column)
                else:
                    _index = index_.child(i_row, index_.column())
                if _index.isValid():
                    _rcs_fnc(_index)

        list_ = []
        model = self.model()

        _rcs_fnc(None)
        return list_

    def _get_items_by_depth_(self, depth, column=0):
        def _rcs_fnc(index_, cur_depth_):
            if cur_depth_ <= depth:
                if index_ is None:
                    row_count = model.rowCount()
                else:
                    row_count = model.rowCount(index_)
                    list_.append(self.itemFromIndex(index_))
                #
                for i_row in range(row_count):
                    if index_ is None:
                        _index = model.index(i_row, column)
                    else:
                        _index = index_.child(i_row, index_.column())
                    #
                    if _index.isValid():
                        _rcs_fnc(_index, cur_depth_+1)

        list_ = []
        model = self.model()
        _rcs_fnc(None, 0)
        return list_

    def _set_scroll_to_item_top_(self, item):
        self.scrollToItem(item, self.PositionAtTop)
        self.setCurrentItem(item)

    def _set_item_add_(self):
        pass

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._set_item_show_kill_all_()
            i._set_item_show_stop_all_()
        #
        self.clear()
        self._item_expand_method_dic = {}

    def _get_sort_order_(self):
        return self.header().sortIndicatorOrder()

    def _refresh_view_items_viewport_showable_by_sort_(self, *args, **kwargs):
        self._refresh_view_all_items_viewport_showable_()
# coding=utf-8
import collections
#
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

from lxutil_gui.qt import utl_gui_qt_core, utl_gui_qt_abstract


class _AbsQtSplitter(QtWidgets.QWidget):
    QT_HANDLE_CLASS = None
    #
    QT_ORIENTATION = None
    #
    HANDLE_WIDTH = 12
    def __init__(self, *args, **kwargs):
        super(_AbsQtSplitter, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._handle_list = []
        self._widget_list = []
        self._rect_list = []
        #
        self._spacing = 4
        self._contents_margins = 0, 0, 0, 0
        #
        self._size_dict = collections.OrderedDict()
        self._pos_dict = collections.OrderedDict()
        self._sizes = []

    def addWidget(self, widget):
        index = len(self._handle_list)
        #
        widget.setParent(self)
        self._widget_list.append(widget)
        # widget.hide()
        #
        handle = self.QT_HANDLE_CLASS()
        handle.setParent(self)
        self._handle_list.append(handle)
        #
        if index not in self._size_dict:
            self._size_dict[index] = 1
        #
        self._rect_list.append(QtCore.QRect())

    def resizeEvent(self, event):
        self._set_update_()

    def _set_update_(self):
        self._set_update_by_size_()
        self._set_widget_geometry_update_()

    def _set_update_by_size_(self):
        ss = self._size_dict
        maximum_size = sum(ss.values())
        if maximum_size > 0:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [w*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + x
                    self._size_dict[idx] = size
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [h*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + y
                    self._size_dict[idx] = size
            else:
                raise TypeError()

    def _set_widget_geometry_update_(self):
        w, h = self.width(), self.height()
        c = len(self._handle_list)
        h_f_w = self.HANDLE_WIDTH
        for idx in range(c):
            handle = self._handle_list[idx]
            widget = self._widget_list[idx]
            rect = self._rect_list[idx]
            #
            p = self._pos_dict[idx]
            s = self._size_dict[idx]
            ps = self._size_dict.get(idx-1)
            ns = self._size_dict.get(idx+1)
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                # handle
                hx, hy = p, 0
                hw, hh = h_f_w, h
                if idx == 0:
                    hx, hy = p-h_f_w, 0
                else:
                    if s == 0:
                        hx, hy = p-h_f_w, 0
                handle.setGeometry(
                    hx, hy, hw, hh
                )
                # print hx, hy, hw, hh
                rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = p+h_f_w, 0
                ww, wh = s-h_f_w, h
                if idx == 0:
                    wx, wy = p, 0
                    ww, wh = s, h
                if ns == 0:
                    ww, wh = s-h_f_w, h
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                # handle
                hx, hy = 0, p
                hw, hh = w, h_f_w
                if idx == 0:
                    hx, hy = 0, p-h_f_w
                if s == 0:
                    hx, hy = 0, p-h_f_w
                handle.setGeometry(
                    hx, hy, hw, hh
                )
                rect.setRect(
                    hx, hy, hw, hh
                )
                # widget
                wx, wy = 0, p+h_f_w
                ww, wh = w, s-h_f_w
                if idx == 0:
                    wx, wy = 0, p
                    ww, wh = w, s
                if ns == 0:
                    ww, wh = w, s-h_f_w
                #
                widget.setGeometry(
                    wx, wy, ww, wh
                )

    def _get_size_(self, index):
        return self._size_dict[index]

    def _set_size_(self, index, size):
        self._size_dict[index] = size
        #
        self._set_update_()

    def _get_sizes_(self, indices=None):
        if indices is not None:
            return [self._size_dict[i] for i in indices]
        return [i for i in self._size_dict.values()]

    def _set_adjacent_sizes_(self, indices, sizes):
        i_l, i_r = indices[:indices[0]], indices[indices[1]:]
        #
        h_f_w = self.HANDLE_WIDTH
        if self._get_orientation_() == QtCore.Qt.Horizontal:
            size_min, size_max = 0 + len(i_l)*h_f_w, self.width() - len(i_r)*h_f_w
        elif self._get_orientation_() == QtCore.Qt.Vertical:
            size_min, size_max = 0 + len(i_l)*h_f_w, self.height() - len(i_r)*h_f_w
        else:
            raise TypeError()
        for seq, size in enumerate(sizes):
            # clamp size
            if size <= size_min:
                size = size_min
            elif size >= size_max:
                size = size_max
            idx = indices[seq]
            self._size_dict[idx] = size
        #
        self._set_update_()

    def _get_indices_(self):
        return self._size_dict.keys()

    def _get_widgets_(self):
        return self._widget_list

    def _get_widget_(self, index):
        return self._widget_list[index]

    def _get_cur_index_(self, qt_point):
        for idx, rect in enumerate(self._rect_list):
            if rect.contains(qt_point) is True:
                return idx

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _set_stretch_factor_(self, index, size):
        self._size_dict[index] = size

    def _get_stretch_factor_(self, index):
        return self._size_dict[index]

    def setSizes(self, sizes):
        pass

    def widget(self, index):
        return self._widget_list[index]

    def indexOf(self, handle):
        return self._handle_list.index(handle)

    def setCollapsible(self, index, boolean):
        pass


class _QtHSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _utl_gui_qt_wgt_item._QtHSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Horizontal
    def __init__(self, *args, **kwargs):
        super(_QtHSplitter, self).__init__(*args, **kwargs)


class _QtVSplitter(_AbsQtSplitter):
    QT_HANDLE_CLASS = _utl_gui_qt_wgt_item._QtVSplitterHandle
    QT_ORIENTATION = QtCore.Qt.Vertical
    def __init__(self, *args, **kwargs):
        super(_QtVSplitter, self).__init__(*args, **kwargs)


class QtTreeWidget(
    QtWidgets.QTreeWidget,
    utl_gui_qt_abstract._QtMenuDef
):
    COLOR_BACKGROUND = QtGui.QColor(54, 54, 54)
    PEN_BRANCH = QtGui.QPen(Brush.tree_branch, DpiScale(1))
    PEN_BRANCH_HIGHLIGHT = QtGui.QPen(Brush.tree_branch_highlight, DpiScale(1))
    headerView = None
    iconDelegate = None
    textDelegate = None
    cachedAncestors = None
    _is_expand_descendants = False
    mimeType = None
    dropIndicatorRect = QtCore.QRect()
    #
    itemChecked = qt_signal()
    itemToggled = qt_signal(bool)
    #
    filterChanged = qt_signal()
    #
    ctrl_f_key_pressed = qt_signal()
    f_key_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtTreeWidget, self).__init__(*args, **kwargs)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.sortByColumn(1, QtCore.Qt.SortOrder())
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
        self.setWordWrap(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setItemDelegate(_utl_gui_qt_wgt_utility.QtStyledItemDelegate())
        # header view
        # set stylesheet
        set_qt_header_view_style(self.header())
        # self.setAlternatingRowColors(True)
        qt_palette = QtDccMtd.get_qt_palette()
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
        self.collapsed.connect(self.onCollapsed)
        self.expanded.connect(self.onExpanded)
        self.itemSelectionChanged.connect(self._set_item_selected_update_)
        # self.itemChanged.connect(self._set_item_changed_update_)
        #
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.installEventFilter(self)
        #
        self._item_expand_method_dic = {}
        #
        self._set_menu_def_init_()

    def _get_item_visible_children_by_index_(self, index):
        lis = []
        raw_count = self.model().rowCount(index)
        for row in range(raw_count):
            child_index = index.child(row, index.column())
            child_item = self.itemFromIndex(child_index)
            if child_item is not None:
                if child_item.isHidden() is True:
                    continue
                lis.append(child_item)
        return lis

    def _get_item_has_visible_children_by_index_(self, index):
        raw_count = self.model().rowCount(index)
        for row in range(raw_count):
            child_index = index.child(row, index.column())
            if child_index.isValid():
                if self.itemFromIndex(child_index).isHidden() is False:
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

    def _get_items_by_keyword_filter_(self, keyword, match_case=False, match_word=False):
        lis = []
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
                        lis.append(item)
        else:
            pass
        return lis

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
        super(QtTreeWidget, self).drawRow(painter, option, index)
        #
        if index in self._selected_indices:
            painter.fillRect(option.rect, Brush.tree_item_selected)
        elif index in self._selected_indirect_indices:
            painter.fillRect(option.rect, Brush.tree_item_selected_indirect)
        #
        QtTreeMtd._set_item_row_draw_(painter, option, index)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            pass
        elif event.key() == QtCore.Qt.Key_F:
            if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                self.ctrl_f_key_pressed.emit()
            else:
                self.f_key_pressed.emit()
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
                pass
        return False

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

    def mouseReleaseEvent(self, event):
        # Handle mouse release event
        super(QtTreeWidget, self).mouseReleaseEvent(event)
        # Reset flags
        self._is_expand_descendants = False

    def onCollapsed(self, index):
        if self._is_expand_descendants:
            self._is_expand_descendants = False
            self._set_item_descendants_expanded_at_(index, False)

    def onExpanded(self, index):
        def fnc_():
            method()
            timer.stop()
        #
        if self._is_expand_descendants:
            self._is_expand_descendants = False
            self._set_item_descendants_expanded_at_(index, True)
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
        self._set_item_show_update_at_(item)
    @classmethod
    def _set_item_show_update_at_(cls, item):
        children = item._get_children_()
        for i in children:
            i._set_item_show_start_()

    def _set_item_descendants_expanded_at_(self, index, expanded):
        for i in range(0, index.model().rowCount(index)):
            child_index = index.child(i, 0)
            self.setExpanded(child_index, expanded)
            self._set_item_descendants_expanded_at_(child_index, expanded)

    def _set_item_expand_connect_to_(self, item, method, time):
        self._item_expand_method_dic[item] = method, time

    def _set_item_check_action_run_(self, item, column):
        if item._get_emit_send_enable_() is True:
            # noinspection PyUnresolvedReferences
            self.itemChecked.emit()

    def _set_item_toggle_emit_send_(self, item, column, boolean):
        if item._get_emit_send_enable_() is True:
            # noinspection PyUnresolvedReferences
            self.itemToggled.emit(boolean)

    def _set_filter_emit_send_(self):
        self.filterChanged.emit()

    def _get_all_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                lis.append(self.itemFromIndex(index_))
            #
            for row in range(row_count):
                if index_ is None:
                    _index = model.index(row, column)
                else:
                    _index = index_.child(row, index_.column())
                if _index.isValid():
                    _rcs_fnc(_index)
        lis = []
        model = self.model()

        _rcs_fnc(None)
        return lis

    def _get_all_leaf_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                if row_count == 0:
                    lis.append(self.itemFromIndex(index_))
            #
            for row in range(row_count):
                if index_ is None:
                    _index = model.index(row, column)
                else:
                    _index = index_.child(row, index_.column())
                if _index.isValid():
                    _rcs_fnc(_index)

        lis = []
        model = self.model()

        _rcs_fnc(None)
        return lis

    def _get_items_by_depth_(self, depth, column=0):
        def _rcs_fnc(index_, cur_depth_):
            if cur_depth_ <= depth:
                if index_ is None:
                    row_count = model.rowCount()
                else:
                    row_count = model.rowCount(index_)
                    lis.append(self.itemFromIndex(index_))
                #
                for row in range(row_count):
                    if index_ is None:
                        _index = model.index(row, column)
                    else:
                        _index = index_.child(row, index_.column())
                    #
                    if _index.isValid():
                        _rcs_fnc(_index, cur_depth_+1)

        lis = []
        model = self.model()
        _rcs_fnc(None, 0)
        return lis

    def _set_scroll_to_item_top_(self, item):
        self.scrollToItem(item, self.PositionAtTop)
        self.setCurrentItem(item)

    def _set_item_add_(self):
        pass

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._set_item_show_stop_()
        #
        self.clear()
        self._item_expand_method_dic = {}


class QtStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(QtStyledItemDelegate, self).__init__(parent)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QtListWidget(utl_gui_qt_abstract._QtAbsListWidget):
    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
        # self.setViewMode(self.IconMode)
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(self.SingleSelection)
        #
        self.setResizeMode(self.Adjust)
        self.setItemDelegate(QtStyledItemDelegate())
        #
        self._item_side = 4
        self._item_spacing = 2
        self._item_frame_icon_width, self._item_frame_icon_height = 40, 128
        self._item_frame_image_width, self._item_frame_image_height = 128, 128
        self._item_frame_name_width, self._item_frame_name_height = 128, 40
        #
        self._item_width, self._item_height = self._get_item_frame_size_()
        #
        self._set_grid_mode_()

    def eventFilter(self, *args):
        widget, event = args
        # if widget == self:
        #     if event.type() == QtCore.QEvent.Resize:
        #         self._set_items_show_update_()
        if widget == self.verticalScrollBar():
            if event.type() == QtCore.QEvent.Resize:
                self._set_items_show_update_()
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self.viewport())
        # for i in self._item_rects:
        #     painter._set_frame_draw_by_rect_(
        #         i, border_color=(255, 0, 0), background_color=Color.TRANSPARENT
        #     )

    def _get_item_frame_size_(self):
        if self._get_is_grid_mode_():
            w, h = (
                self._item_frame_icon_width + self._item_spacing + self._item_frame_image_width + self._item_side*2,
                self._item_frame_image_height + self._item_side*2 + self._item_spacing + self._item_frame_name_height
            )
            return w, h
        else:
            w, h = (
                self._item_frame_image_width + self._item_spacing + self._item_frame_image_width + self._item_side*2,
                self._item_frame_image_height + self._item_side*2
            )
            return w, h

    def _set_item_size_update_(self):
        w, h = self._get_item_frame_size_()
        self.setGridSize(QtCore.QSize(w, h))
        [i.setSizeHint(QtCore.QSize(w, h)) for i in self._get_all_items_()]
        self.verticalScrollBar().setSingleStep(h)

    def _set_item_size_(self, w, h):
        self._item_width, self._item_height = w, h
        self._set_item_size_update_()

    def _set_item_frame_icon_size_(self, w, h):
        self._item_frame_icon_width, self._item_frame_icon_height = w, h
        self._set_item_size_update_()

    def _set_item_frame_image_size_(self, w, h):
        self._item_frame_image_width, self._item_frame_image_height = w, h
        self._set_item_size_update_()

    def _set_item_frame_name_size_(self, w, h):
        self._item_frame_name_width, self._item_frame_name_height = w, h
        self._set_item_size_update_()

    def _set_grid_mode_(self):
        self.setViewMode(self.IconMode)
        self._set_item_size_update_()

    def _set_list_mode_(self):
        self.setViewMode(self.ListMode)
        self._set_item_size_update_()

    def _get_item_count_(self):
        return self.count()

    def _get_all_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _set_view_mode_swap_(self):
        if self._get_is_grid_mode_() is True:
            self._set_list_mode_()
        else:
            self._set_grid_mode_()

    def _get_is_grid_mode_(self):
        return self.viewMode() == self.IconMode

    def _set_item_widget_add_(self, item_widget, *args, **kwargs):
        view = self
        #
        item = _utl_gui_qt_wgt_item.QtListWidgetItem('', view)
        w, h = self._get_item_frame_size_()
        item.setSizeHint(QtCore.QSize(w, h))
        item.gui_proxy = item_widget.gui_proxy
        #
        view.addItem(item)
        view.setItemWidget(item, item_widget)
        item._set_item_show_connect_()
        item_widget._set_view_(view)
        item_widget._set_list_widget_item_(item)
        item_widget._set_index_(view._get_item_count_())
        #
        item_widget._set_frame_icon_size_(
            self._item_frame_icon_width, self._item_frame_icon_height
        )
        item_widget._set_frame_image_size_(
            self._item_frame_image_width, self._item_frame_image_height
        )
        item_widget._set_frame_name_size_(
            self._item_frame_name_width, self._item_frame_name_height
        )

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._set_item_show_stop_()
        #
        self._pre_selected_item = None
        self.clear()


class _QtGuideRect(
    utl_gui_qt_abstract._QtIconDef,
    utl_gui_qt_abstract._QtTypeDef,
    utl_gui_qt_abstract._QtNameDef,
    utl_gui_qt_abstract._QtPathDef,
    utl_gui_qt_abstract._QtFrameDef,
    utl_gui_qt_abstract._QtItemChooseActionDef,
):
    def _set_widget_update_(self):
        pass

    def __init__(self, *args, **kwargs):
        self._set_icon_def_init_()
        self._set_type_def_init_()
        self._set_name_def_init_()
        self._set_path_def_init_()
        self._set_frame_def_init_()
        self._set_item_choose_def_init_()
        #
        self._set_file_icon_path_(
            self._choose_collapse_icon_file_path
        )

    def _get_icon_file_path_(self):
        return [
            self._choose_collapse_icon_file_path,
            self._choose_expand_icon_file_path
        ][self._get_is_choose_dropped_()]


class _QtGuideBar(
    QtWidgets.QWidget,
    #
    utl_gui_qt_abstract._QtMenuDef,
    #
    utl_gui_qt_abstract._QtItemDef,
    utl_gui_qt_abstract._QtItemActionDef,
    utl_gui_qt_abstract._QtItemPressActionDef,
    utl_gui_qt_abstract._QtEntryActionDef,
    #
    utl_gui_qt_abstract._QtViewGuideActionDef,
    utl_gui_qt_abstract._QtViewChooseActionDef,
):
    CHOOSE_RECT_CLS = _QtGuideRect
    #
    CHOOSE_DROP_WIDGET_CLS = _utl_gui_qt_wgt_item._QtChooseDropWidget
    def __init__(self, *args, **kwargs):
        super(_QtGuideBar, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setFont(Font.title)
        #
        self.setMaximumHeight(24)
        self.setMinimumHeight(24)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self._choose_icon_file_path = utl_core.Icon.get('choose_close')
        #
        self._set_menu_def_init_()
        #
        self._set_item_def_init_()
        self._set_item_action_def_init_()
        self._set_item_press_action_def_init_()
        self._set_entry_action_def_init_()
        #
        self._set_view_guide_action_def_init_()
        self._set_view_choose_action_def_init_()
        #
        self._view_guide_current_index = None

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._set_item_geometries_update_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._item_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._item_is_hovered = False
                self._set_choose_current_clear_()
                self._set_guide_current_clear_()
                self.update()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_choose_current_clear_()
                self._set_guide_current_clear_()
                if self._is_entered is False:
                    self._set_current_index_update_(event)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_current_index_update_(event)
                    if self._view_choose_current_index is not None:
                        self._set_item_action_flag_(self.CHOOSE_FLAG)
                    elif self._view_guide_current_index is not None:
                        self._set_item_action_flag_(self.PRESS_CLICK_FLAG)
                    else:
                        self._set_entered_(True)
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_item_is_click_flag_() is True:
                        self._set_item_click_emit_send_()
                        self._set_guide_item_clicked_emit_send_()
                    elif self._get_is_choose_flag_() is True:
                        self._set_choose_item_drop_at_(self._view_choose_current_index)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._set_item_action_flag_clear_()
                #
                self._item_is_hovered = False
                self.update()
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                pass
            elif event.type() == QtCore.QEvent.FocusOut:
                self._set_entered_(False)
        return False

    def paintEvent(self, event):
        painter = _utl_gui_qt_wgt_utility.QtPainter(self)
        bdr_color = [Color.ENTRY_BORDER_ENTRY_OFF, Color.ENTRY_BORDER_ENTRY_ON][self._is_entered]
        bkg_color = [Color.ENTRY_BACKGROUND_ENTRY_OFF, Color.ENTRY_BACKGROUND_ENTRY_ON][self._is_entered]
        painter._set_frame_draw_by_rect_(
            self._entry_frame_rect,
            border_color=bdr_color,
            background_color=bkg_color,
            border_radius=4
        )
        if self._is_entered is True:
            if self._get_choose_item_indices_():
                painter._set_text_draw_by_rect_(
                    self._entry_frame_rect,
                    text=self._get_choose_item_at_(-1)._path_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    color=Color.TEXT_NORMAL,
                    font=get_font(size=10)
                )
        else:
            for index in self._get_choose_item_indices_():
                item = self._get_choose_item_at_(index)
                icon_offset = 0
                name_offset = 0
                if index == self._view_choose_current_index:
                    icon_offset = [0, 2][self._get_item_action_flag_() is not None]
                    painter._set_frame_draw_by_rect_(
                        item._icon_frame_rect,
                        border_color=Color.TRANSPARENT,
                        background_color=Color.ITEM_BACKGROUND_HOVER,
                        border_radius=4,
                        offset=icon_offset
                    )
                elif index == self._view_guide_current_index:
                    name_offset = [0, 2][self._get_item_action_flag_() is not None]
                    painter._set_frame_draw_by_rect_(
                        item._frame_name_rect,
                        border_color=Color.TRANSPARENT,
                        background_color=Color.ITEM_BACKGROUND_HOVER,
                        border_radius=4,
                        offset=name_offset
                    )
                #
                painter._set_file_icon_draw_by_rect_(
                    item._file_icon_rect,
                    file_path=item._get_icon_file_path_(),
                    offset=icon_offset
                )
                #
                type_text = item._type_text
                painter._set_text_draw_by_rect_(
                    item._type_rect,
                    text=type_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    color=bsc_core.TextOpt(type_text).to_rgb(),
                    font=get_font(size=10, italic=True),
                    offset=name_offset
                )
                #
                name_text = item._name_text
                painter._set_text_draw_by_rect_(
                    item._name_rect,
                    text=name_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    font=get_font(size=12, italic=True),
                    offset=name_offset
                )

    def _set_widget_update_(self):
        self.update()

    def _set_current_index_update_(self, event):
        p = event.pos()
        #
        self._set_choose_current_clear_()
        self._set_guide_current_clear_()
        for index in self._get_choose_item_indices_():
            item = self._get_choose_item_at_(index)
            if item._icon_frame_rect.contains(p) is True:
                self._set_choose_current_(index)
                break
            elif item._frame_name_rect.contains(p) is True:
                self._set_guide_current_(index)
                break
        #
        self.update()

    def _get_text_width_(self, text):
        return self.fontMetrics().width(text)

    def _set_path_args_(self, path_args):
        self._set_choose_clear_()
        self._set_guide_clear_()
        #
        path_values = path_args.values()
        for index, (k, v) in enumerate(path_args.items()):
            item = self._set_choose_item_create_()
            #
            path = '/' + '/'.join(path_values[:index+1])
            item._set_path_text_(path)
            item._set_type_text_(k)
            item._set_name_text_(v)
        #
        self._set_item_geometries_update_()
        self.update()

    def _set_item_geometries_update_(self):
        side = 2
        spacing = 2
        x, y = 0, 0
        w, h = self.width()-1, self.height()-1
        self._set_entry_frame_rect_(x, y, w, h)
        #
        i_x, i_y = x + 1, y + 1
        i_f_w, i_f_h = h-2, h-2
        i_i_w, i_i_h = 16, 16
        #
        for index in self._get_choose_item_indices_():
            item = self._get_choose_item_at_(index)
            item._set_frame_icon_rect_(
                i_x, i_y, i_f_w, i_f_h
            )
            item._set_file_icon_rect_(
                i_x+(i_f_w-i_i_w)/2, i_y+(i_f_h-i_i_h)/2, i_i_w, i_i_h
            )
            i_x += i_f_w + spacing
            #
            i_path_key = item._type_text
            i_path_value = item._name_text
            #
            # i_path_w = self._get_text_width_(i_path_key + i_path_value) + spacing*4
            i_path_w_0, i_path_h_0 = utl_gui_qt_core.TextMtd.get_size(10, i_path_key)
            i_path_w_1, i_path_h_1 = utl_gui_qt_core.TextMtd.get_size(12, i_path_value)
            i_path_w = i_path_w_0 + i_path_w_1 + spacing*8
            item._set_frame_name_rect_(
                i_x-spacing*2, i_y, i_path_w, h
            )
            #
            i_path_key_w = i_path_w_0 + spacing*4
            item._set_type_rect_(
                i_x, i_y, i_path_key_w, h
            )
            i_x += i_path_key_w
            #
            i_path_value_w = i_path_w_1 + spacing*4
            item._set_name_rect_(
                i_x, i_y, i_path_value_w, h
            )
            #
            i_x += i_path_value_w

    def _set_clear_(self):
        self._set_path_args_({})

    def _get_guide_items_(self):
        return self._get_choose_items_()

    def _get_choose_pos_at_(self, index=0):
        item = self._get_choose_item_at_(index)
        rect = item._icon_frame_rect
        return self.mapToGlobal(rect.center())

    def _get_choose_size_at_(self, index=0):
        item = self._get_choose_item_at_(index)
        rect = item._icon_frame_rect
        return rect.width(), rect.height()

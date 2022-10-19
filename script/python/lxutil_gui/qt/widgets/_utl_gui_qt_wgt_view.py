# coding=utf-8
import collections
#
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_item

from lxutil_gui.qt import utl_gui_qt_core, utl_gui_qt_abstract

from lxutil_gui import utl_gui_core


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

    def paintEvent(self, event):
        # painter = QtPainter(self)
        # painter._set_background_color_(255, 0, 0)
        # painter.drawRect(
        #     QtCore.QRect(
        #         0, 0, self.width(), self.height()
        #     )
        # )
        pass

    def _set_update_(self):
        self._set_update_by_size_()
        self._refresh_widget_draw_geometry_()

    def _set_update_by_size_(self):
        ss = self._size_dict
        maximum_size = sum(ss.values())
        # print self.QT_ORIENTATION, maximum_size, self._widget_list, self._handle_list
        if maximum_size > 0:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [w*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, i_size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + x
                    self._size_dict[idx] = i_size
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                x, y = 0, 0
                w, h = self.width(), self.height()
                _ = [h*(float(ss[i])/float(maximum_size)) for i in range(len(self._handle_list))]
                for idx, i_size in enumerate(_):
                    self._pos_dict[idx] = sum(_[:idx]) + y
                    self._size_dict[idx] = i_size
            else:
                raise TypeError()

    def _refresh_widget_draw_geometry_(self):
        w, h = self.width(), self.height()
        c = len(self._handle_list)
        h_f_w = self.HANDLE_WIDTH
        for idx in range(c):
            i_handle = self._handle_list[idx]
            widget = self._widget_list[idx]
            i_rect = self._rect_list[idx]
            #
            p = self._pos_dict[idx]
            s = self._size_dict[idx]
            ps = self._size_dict.get(idx-1)
            ns = self._size_dict.get(idx+1)
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                # i_handle
                hx, hy = p, 0
                hw, hh = h_f_w, h
                if idx == 0:
                    hx, hy = p-h_f_w, 0
                else:
                    if s == 0:
                        hx, hy = p-h_f_w, 0
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                # print hx, hy, hw, hh
                i_rect.setRect(
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
                # i_handle
                hx, hy = 0, p
                hw, hh = w, h_f_w
                if idx == 0:
                    hx, hy = 0, p-h_f_w
                if s == 0:
                    hx, hy = 0, p-h_f_w
                i_handle.setGeometry(
                    hx, hy, hw, hh
                )
                # print i_handle.geometry()
                i_rect.setRect(
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

        for seq, i_size in enumerate(sizes):
            # clamp size
            if i_size <= size_min:
                i_size = size_min
            elif i_size >= size_max:
                i_size = size_max
            #
            idx = indices[seq]
            self._size_dict[idx] = i_size
        #
        self._set_update_()

    def _get_indices_(self):
        return self._size_dict.keys()

    def _get_widgets_(self):
        return self._widget_list

    def _get_widget_(self, index):
        return self._widget_list[index]

    def _set_widget_hide_at_(self, index):
        handle = self._get_handle_at_(index+1)
        handle._set_contract_l_switch_()

    def _get_cur_index_(self, qt_point):
        for idx, i_rect in enumerate(self._rect_list):
            if i_rect.contains(qt_point) is True:
                return idx

    def _get_orientation_(self):
        return self.QT_ORIENTATION

    def _set_stretch_factor_(self, index, size):
        self._size_dict[index] = size

    def _get_stretch_factor_(self, index):
        return self._size_dict[index]

    def setSizes(self, sizes):
        pass

    def _set_sizes_(self, sizes):
        self._sizes = sizes

    def _get_handle_at_(self, index):
        return self._handle_list[index]

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


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_items_def_init_(self, widget):
        self._widget = widget

        self._items = []
        self._item_index_current = 0
        self._item_index_hovered = None

        self._item_rects = []
        self._item_name_texts = []
        self._item_icon_name_texts = []

    def _set_item_current_index_(self, index):
        pass


class _QtTabView(
    QtWidgets.QWidget,
    AbsQtItemsDef,
    utl_gui_qt_abstract.AbsQtWgtDef,
):
    current_changed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(_QtTabView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._set_items_def_init_(self)
        self._set_wgt_def_init_(self)

        self._tab_w, self._tab_h = 48, 24

        self.setFont(
            get_font(size=10)
        )

    def _set_item_add_(self, widget, *args, **kwargs):
        widget.setParent(self)
        #
        self._items.append(widget)
        self._item_rects.append(QtCore.QRect())
        if 'name' in kwargs:
            self._item_name_texts.append(kwargs['name'])
        else:
            self._item_name_texts.append(None)
        #
        if 'icon_name_text' in kwargs:
            self._item_icon_name_texts.append(kwargs['icon_name_text'])
        else:
            self._item_icon_name_texts.append(None)
        #
        widget.installEventFilter(self)

        self._refresh_widget_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_(self):
        self._set_wgt_update_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _set_wgt_update_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        t_w, t_h = self._tab_w, self._tab_h
        #
        c_x = x
        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            if i_name_text is not None:
                i_text_width = self._get_text_draw_width_(
                    i_name_text
                )
            else:
                i_text_width = t_w
            #
            i_icon_name_text = self._item_icon_name_texts[i_index]
            if i_icon_name_text is not None:
                i_icon_w = t_h
            else:
                i_icon_w = 0
            #
            i_t_w = i_text_width+i_icon_w+t_h*2
            #
            i_item_rect.setRect(
                c_x, y, i_t_w, t_h
            )
            c_x += i_t_w
        # widget
        for i_index, i_item in enumerate(self._items):
            if i_index == self._item_index_current:
                if i_item is not None:
                    i_item.show()
                    i_item.setGeometry(
                        x, y+t_h, w, h-t_h
                    )
            else:
                i_item.hide()

    def _set_item_hovered_clear_(self):
        self._item_index_hovered = None
        self._refresh_widget_draw_()

    def _set_item_current_index_(self, index):
        if index != self._item_index_current:
            self._item_index_current = index
            self._refresh_widget_()
            self.current_changed.emit()

    def _set_item_current_changed_connect_to_(self, fnc):
        self.current_changed.connect(fnc)

    def _set_action_hover_execute_(self, event):
        point = event.pos()
        self._item_index_hovered = None

        for i_index, i in enumerate(self._item_rects):
            if i.contains(point):
                self._item_index_hovered = i_index
                break

        self._refresh_widget_draw_()

    def _get_current_name_text_(self):
        return self._item_name_texts[self._item_index_current]

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._set_item_hovered_clear_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._set_action_hover_execute_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._item_index_hovered is not None:
                        self._set_item_current_index_(self._item_index_hovered)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
        else:
            if event.type() == QtCore.QEvent.Enter:
                self._set_item_hovered_clear_()
            if event.type() == QtCore.QEvent.Leave:
                self._set_item_hovered_clear_()
        return False

    def paintEvent(self, event):
        painter = QtPainter(self)

        painter.setRenderHints(
            painter.Antialiasing
        )
        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            i_icon_name_text = self._item_icon_name_texts[i_index]
            is_current = i_index == self._item_index_current
            is_hovered = i_index == self._item_index_hovered
            if is_current is False:
                painter._set_tab_button_draw_(
                    i_item_rect,
                    icon_name_text=i_icon_name_text,
                    name_text=i_name_text,
                    is_hovered=is_hovered,
                    is_current=is_current,
                )

        for i_index, i_item_rect in enumerate(self._item_rects):
            i_name_text = self._item_name_texts[i_index]
            i_icon_name_text = self._item_icon_name_texts[i_index]
            is_current = i_index == self._item_index_current
            is_hovered = i_index == self._item_index_hovered
            if is_current is True:
                painter._set_tab_button_draw_(
                    i_item_rect,
                    icon_name_text=i_icon_name_text,
                    name_text=i_name_text,
                    is_hovered=is_hovered,
                    is_current=is_current,
                )


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
        self.header().setPalette(QtDccMtd.get_qt_palette())
        # self.header().setSectionResizeMode(self.header().ResizeToContents)
        self.header().setStyleSheet(
            utl_gui_core.QtStyleMtd.get('QHeaderView')
        )
        self.header().setFont(Font.NAME)
        self.header().setAutoFillBackground(True)
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
            painter.fillRect(option.rect, QtBackgroundColor.ItemSelected)
        elif index in self._selected_indirect_indices:
            painter.fillRect(option.rect, QtBackgroundColor.ItemSelectedIndirect)
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
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(False)
            elif event.type() == QtCore.QEvent.Resize:
                self._set_show_view_items_update_()
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


class QtStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(QtStyledItemDelegate, self).__init__(parent)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QtListWidget(
    utl_gui_qt_abstract.AbsQtListWidget
):
    ctrl_f_key_pressed = qt_signal()
    f5_key_pressed = qt_signal()
    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
        qt_palette = QtDccMtd.get_qt_palette()
        self.setPalette(qt_palette)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(self.SingleSelection)
        #
        self.setResizeMode(self.Adjust)
        self.setItemDelegate(QtStyledItemDelegate())
        #
        self._item_frame_icon_width, self._item_frame_icon_height = 40, 128
        self._item_frame_image_width, self._item_frame_image_height = 128, 128
        self._item_frame_name_width, self._item_frame_name_height = 128, 40
        #
        self._grid_size = 128, 128
        #
        self._item_side = 4
        self._item_spacing = 2
        #
        self._item_frame_size = 128, 128
        self._item_frame_draw_enable = False
        #
        self._item_icon_frame_size = 20, 20
        self._item_icon_size = 16, 16
        self._item_icon_frame_draw_enable = False
        #
        self._item_name_frame_size = 16, 16
        self._item_name_size = 12, 12
        self._item_name_frame_draw_enable = False
        #
        self._item_image_frame_draw_enable = False
        #
        self._set_grid_mode_()
        #
        self._action_control_flag = False

    def _execute_action_wheel_(self, event):
        if self._action_control_flag is True:
            delta = event.angleDelta().y()
            step = 4
            pre_item_frame_w, pre_item_frame_h = self._item_frame_size
            if delta > 0:
                item_frame_w = pre_item_frame_w+step
            else:
                item_frame_w = pre_item_frame_w-step
            #
            item_frame_w = max(min(item_frame_w, 480), 28)
            if item_frame_w != pre_item_frame_w:
                item_frame_h = int(float(pre_item_frame_h)/float(pre_item_frame_w)*item_frame_w)
                self._set_item_frame_size_(item_frame_w, item_frame_h)
                self._set_all_item_widgets_update_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
                    self.ctrl_f_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_F5:
                    self.f5_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = True
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
            elif event.type() == QtCore.QEvent.Wheel:
                self._execute_action_wheel_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._set_show_view_items_update_()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _utl_gui_qt_wgt_utility._QtEntryFrame):
                    parent._set_focused_(False)
            elif event.type() == QtCore.QEvent.Drop:
                print 'AAAA'
        if widget == self.verticalScrollBar():
            pass
        return False

    def paintEvent(self, event):
        # painter = QtPainter(self.viewport())
        # for i in self._item_rects:
        #     painter._set_frame_draw_by_rect_(
        #         i, border_color=(255, 0, 0), background_color=QtBackgroundColor.Transparent
        #     )
        pass

    def _set_grid_size_(self, w, h):
        self._grid_size = w, h
        self._set_grid_size_update_()

    def _set_grid_size_update_(self):
        w, h = self._get_grid_size_()
        self.setGridSize(QtCore.QSize(w, h))
        [i.setSizeHint(QtCore.QSize(w, h)) for i in self._get_all_items_()]
        self.verticalScrollBar().setSingleStep(h)

    def _set_grid_size_change_update_(self):
        w, h = self._get_grid_size_()
        self.verticalScrollBar().setSingleStep(h)

    def _set_grid_size_update_by_view_mode_(self):
        item = self.item(0)
        if item is not None:
            item_widget = self.itemWidget(item)
            if item_widget:
                if item_widget._get_has_image_():
                    print item_widget._get_image_frame_rect_()

    def _get_grid_size_(self):
        return self._grid_size

    def _get_item_frame_size_(self):
        if self._get_is_grid_mode_():
            w, h = (
                self._item_frame_icon_width + self._item_spacing + self._item_frame_image_width + self._item_side*2,
                self._item_frame_image_height + self._item_spacing + self._item_frame_name_height + self._item_side*2
            )
            return w, h
        else:
            w, h = (
                self._item_frame_image_width + self._item_spacing + self._item_frame_image_width + self._item_side*2,
                self._item_frame_image_height + self._item_side*2
            )
            return w, h
    #
    def _set_item_frame_size_(self, w, h):
        self._item_frame_size = w, h
        _w, _h = w+self._item_side*2, h+self._item_side*2
        #
        self._set_grid_size_(_w, _h)

    def _set_item_frame_draw_enable_(self, boolean):
        self._item_frame_draw_enable = boolean

    def _set_item_icon_frame_size_(self, w, h):
        self._item_icon_frame_size = w, h

    def _set_item_icon_size_(self, w, h):
        self._item_icon_size = w, h

    def _set_item_icon_frame_draw_enable_(self, boolean):
        self._item_icon_frame_draw_enable = boolean

    def _set_item_name_frame_size_(self, w, h):
        self._item_name_frame_size = w, h

    def _set_item_name_size_(self, w, h):
        self._item_name_size = w, h

    def _set_item_name_frame_draw_enable_(self, boolean):
        self._item_name_frame_draw_enable = boolean

    def _set_item_image_frame_draw_enable_(self, boolean):
        self._item_image_frame_draw_enable = boolean
    #
    def _set_grid_mode_(self):
        self.setViewMode(self.IconMode)
        # self._set_grid_size_update_by_view_mode_()
        self._set_grid_size_change_update_()

    def _set_list_mode_(self):
        self.setViewMode(self.ListMode)
        # self._set_grid_size_update_by_view_mode_()
        self._set_grid_size_change_update_()

    def _get_item_count_(self):
        return self.count()

    def _get_all_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _get_all_item_widgets_(self):
        return [self.itemWidget(self.item(i)) for i in range(self.count())]

    def _set_all_item_widgets_update_(self):
        [(i._set_frame_size_(*self._item_frame_size), i._refresh_widget_draw_geometry_()) for i in self._get_all_item_widgets_()]

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
        item = _utl_gui_qt_wgt_utility.QtListWidgetItem('', view)
        item.setSizeHint(QtCore.QSize(*self._grid_size))
        item.gui_proxy = item_widget.gui_proxy
        #
        view.addItem(item)
        view.setItemWidget(item, item_widget)
        item._set_item_show_connect_()
        item_widget._set_view_(view)
        item_widget._set_item_(item)
        item_widget._set_index_(view._get_item_count_())
        #
        item_widget._set_frame_size_(
            *self._item_frame_size
        )
        item_widget._set_frame_draw_enable_(
            self._item_frame_draw_enable
        )
        #
        item_widget._set_icon_frame_size_(
            *self._item_icon_frame_size
        )
        item_widget._set_icon_size_(
            *self._item_icon_size
        )
        item_widget._set_icon_frame_draw_enable_(
            self._item_icon_frame_draw_enable
        )
        #
        item_widget._set_name_frame_size_(
            *self._item_name_frame_size
        )
        item_widget._set_name_size_(
            *self._item_name_size
        )
        item_widget._set_name_frame_draw_enable_(
            self._item_name_frame_draw_enable
        )
        #
        item_widget._set_image_frame_draw_enable_(
            self._item_image_frame_draw_enable
        )

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._set_item_show_kill_all_()
            i._set_item_show_stop_all_()
        #
        self._pre_selected_items = []
        #
        self.clear()


class _QtGuideBar(
    _utl_gui_qt_wgt_utility._QtEntryFrame,
    #
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtValueEntryDef,
    #
    utl_gui_qt_abstract.AbsQtActionDef,
    utl_gui_qt_abstract.AbsQtActionHoverDef,
    utl_gui_qt_abstract.AbsQtActionPressDef,
    utl_gui_qt_abstract.AbsQtEntryActionDef,
    #
    utl_gui_qt_abstract.AbsQtGuideActionDef,
    utl_gui_qt_abstract.AbsQtGuideChooseActionDef,
):
    CHOOSE_RECT_CLS = _utl_gui_qt_wgt_item._QtGuideRect
    CHOOSE_FRAME_CLASS = _utl_gui_qt_wgt_utility._QtPopupGuideFrame
    #
    QT_VALUE_ENTRY_CLASS = _utl_gui_qt_wgt_utility.QtLineEdit_
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
        self._set_value_entry_def_init_(self)
        self._build_entry_(str)
        #
        self._choose_icon_file_path = utl_core.Icon.get('choose_close')
        #
        self._set_menu_def_init_()
        #
        self._set_action_hover_def_init_()
        self._set_action_def_init_(self)
        self._set_action_press_def_init_()
        self._set_action_entry_def_init_()
        #
        self._set_guide_action_def_init_()
        self._set_guide_choose_action_def_init_(self)

        self._enter_is_enable = False

    def eventFilter(self, *args):
        super(_QtGuideBar, self).eventFilter(*args)
        #
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_guide_draw_geometry_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._action_is_hovered = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._action_is_hovered = False
                self._clear_guide_choose_current_()
                self._clear_guide_current_()
                self.update()
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._enter_is_enable is False:
                    self._refresh_guide_current_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._refresh_guide_current_(event)
                    #
                    if self._guide_choose_current_index is not None:
                        self._set_action_flag_(self.ActionFlag.ChooseClick)
                    elif self._guide_current_index is not None:
                        self._set_action_flag_(self.ActionFlag.PressClick)
                    else:
                        self._set_entry_enable_(True)
                if event.button() == QtCore.Qt.RightButton:
                    self._set_menu_show_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.db_clicked.emit()
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_press_flag_is_click_() is True:
                        self._send_action_press_click_emit_()
                        self._send_action_guide_item_press_clicked_emit_()
                    elif self._get_is_choose_flag_() is True:
                        self._start_guide_choose_item_popup_at_(self._guide_choose_current_index)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                #
                self._set_action_flag_clear_()
                #
                self._action_is_hovered = False
                self._refresh_widget_draw_()
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._set_focused_(False)
                self._set_entry_enable_(False)
        return False

    def paintEvent(self, event):
        super(_QtGuideBar, self).paintEvent(event)
        painter = QtPainter(self)
        if self._enter_is_enable is True:
            pass
            # if self._get_guide_choose_item_indices_():
            #     painter._set_text_draw_by_rect_(
            #         self._entry_frame_draw_rect,
            #         text=self._get_guide_choose_item_at_(-1)._path_text,
            #         text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            #         font_color=QtFontColor.Basic,
            #         font=get_font(size=10)
            #     )
        else:
            for index in self._get_guide_choose_item_indices_():
                i_item = self._get_guide_choose_item_at_(index)
                i_icon_offset = 0
                name_offset = 0
                choose_is_hovered = index == self._guide_choose_current_index
                guide_is_hovered = index == self._guide_current_index
                if index == self._guide_choose_current_index:
                    i_icon_offset = [0, 2][self._get_action_flag_() is not None]
                    background_color = painter._get_item_background_color_1_by_rect_(
                        i_item._icon_frame_rect,
                        is_hovered=choose_is_hovered,
                        is_actioned=self._get_is_actioned_(),
                    )
                    painter._set_frame_draw_by_rect_(
                        i_item._icon_frame_rect,
                        border_color=QtBackgroundColor.Transparent,
                        background_color=background_color,
                        border_radius=4,
                        offset=i_icon_offset
                    )
                elif index == self._guide_current_index:
                    background_color = painter._get_item_background_color_1_by_rect_(
                        i_item._name_frame_rect,
                        is_hovered=guide_is_hovered,
                        is_actioned=self._get_is_actioned_(),
                    )
                    name_offset = [0, 2][self._get_action_flag_() is not None]
                    painter._set_frame_draw_by_rect_(
                        i_item._name_frame_rect,
                        border_color=QtBackgroundColor.Transparent,
                        background_color=background_color,
                        border_radius=4,
                        offset=name_offset
                    )
                #
                painter._set_icon_file_draw_by_rect_(
                    i_item._icon_file_draw_rect,
                    file_path=i_item._get_icon_file_path_(),
                    offset=i_icon_offset
                )
                #
                i_type_text = i_item._type_text
                painter._set_text_draw_by_rect_(
                    i_item._type_rect,
                    text=i_type_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    font_color=bsc_core.TextOpt(i_type_text).to_rgb(),
                    font=get_font(size=10, italic=True),
                    offset=name_offset
                )
                #
                i_name_text = i_item._name_text
                painter._set_text_draw_by_rect_(
                    i_item._name_draw_rect,
                    text=i_name_text,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                    font=get_font(size=12),
                    offset=name_offset,
                    is_hovered=guide_is_hovered,
                )

    def _set_entry_enable_(self, boolean):
        self._enter_is_enable = boolean
        if self._value_entry is not None:
            self._value_entry.setVisible(boolean)
            self._value_entry._set_value_(
                self._get_guide_path_()
            )
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _build_entry_(self, *args, **kwargs):
        self._item_value_type = args[0]
        #
        self._value_entry_layout = QtHBoxLayout(self)
        self._value_entry_layout.setContentsMargins(0, 0, 0, 0)
        self._value_entry_layout.setSpacing(4)
        #
        self._value_entry = self.QT_VALUE_ENTRY_CLASS()
        self._value_entry.hide()
        self._value_entry.setFocusProxy(self)
        self._value_entry_layout.addWidget(self._value_entry)
        self._value_entry._set_value_type_(self._item_value_type)
        #
        self._entry_history_button = _utl_gui_qt_wgt_item._QtIconPressItem(self)
        #
        self._entry_history_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get('history')
        )
        self._entry_history_button._set_sub_icon_file_path_(
            utl_gui_core.RscIconFile.get('down')
        )

    def _refresh_guide_current_(self, event):
        p = event.pos()
        #
        self._clear_guide_choose_current_()
        self._clear_guide_current_()
        if self._enter_is_enable is False:
            for index in self._get_guide_choose_item_indices_():
                i_item = self._get_guide_choose_item_at_(index)
                if i_item._icon_frame_rect.contains(p) is True:
                    self._set_guide_choose_current_index_(index)
                    break
                elif i_item._name_frame_rect.contains(p) is True:
                    self._set_view_guide_current_index_(index)
                    break
        #
        self._refresh_widget_draw_()

    def _set_view_path_args_(self, path_args):
        self._set_guide_choose_clear_()
        self._set_view_guide_clear_()
        #
        path_values = path_args.values()
        for index, (k, v) in enumerate(path_args.items()):
            i_item = self._set_guide_choose_item_create_()
            #
            i_path = '/' + '/'.join(path_values[:index+1])
            i_item._set_path_text_(i_path)
            i_item._set_type_text_(k)
            i_item._set_name_text_(v)
        #
        self._refresh_guide_draw_geometry_()
        self.update()

    def _refresh_guide_draw_geometry_(self):
        side = 2
        spacing = 2
        x, y = 0, 0
        w, h = self.width()-1, self.height()-1
        self._set_entry_frame_draw_rect_(x, y, w, h)
        #
        i_f_w, i_f_h = h-4, h-4
        i_i_w, i_i_h = 16, 16
        #
        i_x, i_y = x + 1, (h-i_f_h)/2

        frm_w, frm_h = 20, 20

        self._entry_history_button.setGeometry(
            w-frm_w, y+(h-frm_h)/2, frm_w, frm_h
        )
        #
        for index in self._get_guide_choose_item_indices_():
            i_item = self._get_guide_choose_item_at_(index)
            i_item._set_icon_frame_rect_(
                i_x, i_y, i_f_w, i_f_h
            )
            i_item._set_icon_file_draw_rect_(
                i_x+(i_f_w-i_i_w)/2, i_y+(i_f_h-i_i_h)/2, i_i_w, i_i_h
            )
            i_x += i_f_w + spacing
            #
            i_path_key = i_item._type_text
            i_path_value = i_item._name_text
            #
            i_path_w_0, i_path_h_0 = utl_gui_qt_core.TextMtd.get_size(10, i_path_key)
            i_path_w_1, i_path_h_1 = utl_gui_qt_core.TextMtd.get_size(12, i_path_value)
            i_path_w = i_path_w_0 + i_path_w_1 + spacing*8
            i_item._set_name_frame_rect_(
                i_x-spacing*2, i_y, i_path_w, i_f_h
            )
            #
            i_path_key_w = i_path_w_0 + spacing*4
            i_item._set_type_rect_(
                i_x, i_y, i_path_key_w, i_f_h
            )
            i_x += i_path_key_w
            #
            i_path_value_w = i_path_w_1 + spacing*4
            i_item._set_name_draw_geometry_(
                i_x, i_y, i_path_value_w, i_f_h
            )
            #
            i_x += i_path_value_w

    def _set_view_guide_and_choose_clear_(self):
        self._set_view_path_args_({})

    def _get_view_guide_items_(self):
        return self._get_guide_choose_items_()

    def _get_guide_choose_item_point_at_(self, index=0):
        item = self._get_guide_choose_item_at_(index)
        rect = item._icon_frame_rect
        return self.mapToGlobal(rect.center())

    def _get_guide_choose_item_rect_at_(self, index=0):
        item = self._get_guide_choose_item_at_(index)
        rect = item._icon_frame_rect
        return rect

    def _get_guide_path_(self):
        item = self._get_guide_choose_item_at_(-1)
        if item:
            return item._path_text


class _QtMenuBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(_QtMenuBar, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)

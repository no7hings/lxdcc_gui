# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract


class QtListWidget(
    utl_gui_qt_abstract.AbsQtListWidget
):
    ctrl_f_key_pressed = qt_signal()
    f5_key_pressed = qt_signal()
    item_checked = qt_signal(object, int)
    info_changed = qt_signal(str)
    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
        qt_palette = QtDccMtd.get_palette()
        self.setPalette(qt_palette)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(self.SingleSelection)
        #
        self.setResizeMode(self.Adjust)
        # self.setItemDelegate(QtStyledItemDelegate())
        self.setVerticalScrollMode(self.ScrollPerItem)
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

        self.item_checked.connect(
            self._refresh_info_
        )

        self._info = ''

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
                self._refresh_view_all_items_viewport_showable_()
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
            elif event.type() == QtCore.QEvent.Drop:
                print 'AAAA'
        if widget == self.verticalScrollBar():
            pass
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = QtPainter(self.viewport())
            painter._set_empty_draw_by_rect_(
                self.rect()
            )

    def _refresh_info_(self, *args, **kwargs):
        c = sum([self.item(i)._get_is_checked_() for i in range(self.count())])
        if c:
            info = '{} item is checked ...'.format(c)
        else:
            info = ''
        if info != self._info:
            self.info_changed.emit(info)
            self._info = info

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
        [
            (i._set_frame_size_(*self._item_frame_size), i._refresh_widget_draw_geometry_())
            for i in self._get_all_item_widgets_()]

    def _set_all_item_widgets_checked_(self, boolean):
        [
            i._set_checked_(boolean)
            for i in self._get_all_item_widgets_()
        ]

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
        item_widget.check_toggled.connect(
            item._set_checked_
        )
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
        item_widget._set_icon_frame_draw_size_(
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

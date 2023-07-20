# coding:utf-8
from lxutil_gui.qt.utl_gui_qt_core import *


class GuiItem(object):
    def __init__(self, widget):
        self._widget = widget
        self._name_text = None
        self._icon_text = None
        self._rect = QtCore.QRect()
        self._popup_rect = QtCore.QRect()

    def get_widget(self):
        return self._widget
    widget = property(get_widget)

    def set_name_text(self, text):
        self._name_text = text

    def get_name_text(self):
        return self._name_text
    name_text = property(get_name_text)

    def set_icon_text(self, text):
        self._icon_text = text

    def get_icon_text(self):
        return self._icon_text
    icon_text = property(get_icon_text)

    def get_rect(self):
        return self._rect
    rect = property(get_rect)

    def get_popup_rect(self):
        return self._popup_rect
    rect_popup = property(get_popup_rect)

    def delete(self):
        self._widget.close()
        self._widget.deleteLater()


class GuiItemStack(object):
    ITEM_CLS = GuiItem
    def __init__(self):
        self._count = 0
        self._item_list = []

    def create_item(self, widget):
        item = self.ITEM_CLS(widget)
        self._item_list.append(item)
        #
        self._count += 1
        return item

    def get_item_at(self, index):
        if self._item_list:
            return self._item_list[index]

    def delete_item_at(self, index):
        item = self._item_list[index]
        item.delete()
        self._item_list.pop(index)
        self._count -= 1

    def delete_item(self, item):
        index = self._item_list.index(item)
        item.delete()
        self._item_list.pop(index)
        self._count -= 1

    def get_index_by_name_text(self, text):
        for i_index, i_item in enumerate(self._item_list):
            if i_item.name_text == text:
                return i_index

    def get_name_text_at(self, index):
        item = self.get_item_at(index)
        if item:
            return self.get_item_at(index).name_text

    def get_count(self):
        return self._count

    def get_index_maximum(self):
        return self._count - 1

    def get_items(self):
        return self._item_list


class GuiScroll(object):
    def __init__(self):
        self._is_valid = False
        #
        self._w = 0
        self._abs_w = 0
        self._maximum = 0
        self._minimum = 0
        self._value = 0
        self._step = 0

    def set_w(self, v):
        self._w = v

    def set_abs_w(self, v):
        self._abs_w = v

    def get_is_valid(self):
        return self._is_valid

    def set_step(self, v):
        self._step = v

    def step_to_previous(self):
        return self.adjust_value(-self._step)

    def step_to_next(self):
        return self.adjust_value(self._step)

    def adjust_value(self, v):
        return self.accept_value(self._value+v)

    def accept_value(self, v):
        if self._is_valid:
            value_pre = self._value
            self._value = int(max(min(v, self._maximum), self._minimum))
            if self._value != value_pre:
                return True
            return False
        #
        self._value = 0
        return False

    def get_value(self):
        return self._value

    def update(self):
        if self._abs_w > self._w:
            self._maximum = self._abs_w-self._w
            self._is_valid = True
            self.accept_value(self._value)
        else:
            self._maximum = 0
            self._value = 0
            self._is_valid = False

    def get_is_maximum(self):
        return self._value == self._maximum

    def get_is_minimum(self):
        return self._value == self._minimum


class GuiGridBase(object):
    @staticmethod
    def _to_column_count(w, item_w):
        if item_w > 0:
            return max(int(w/item_w), 1)
        return 1
    @staticmethod
    def _to_row_count(h, item_h):
        if item_h > 0:
            return max(int(h/item_h), 1)
        return 1
    @staticmethod
    def _get_row_count(item_count, column_count):
        return int((item_count+column_count-1)/column_count)
    @staticmethod
    def _get_index_between(column, row, column_count):
        return int(column+row*column_count)
    @staticmethod
    def _get_column_loc(x, item_w):
        return int(x/item_w)
    @staticmethod
    def _get_column_at(index, column_count):
        return int(index % column_count)
    @staticmethod
    def _get_row_loc(y, item_h):
        return int(y/item_h)
    @staticmethod
    def _get_row_at(index, column_count):
        return int(index/column_count)
    @staticmethod
    def _map_to_item_pos(x, y, item_w, item_h, offset_x, offset_y, column, row):
        return int(x+offset_x-column*item_w), int(y+offset_y-row*item_h)
    @classmethod
    def _get_abs_size(cls, item_w, item_h, column_count, row_count):
        return column_count*item_w, row_count*item_h


class GuiGridLayout(GuiGridBase):
    def __init__(self):
        self._item_count = 0
        self._x, self._y = 0, 0
        self._w, self._h = 48, 48
        self._item_w, self._item_h = 48, 48
        self._column_count, self._row_count = 1, 1
        self._abs_w, self._abs_h = 48, 48
        # left，top，right，bottom
        self._item_margins = 2, 2, 2, 2

    def get_item_column_at(self, index):
        return self._get_column_at(index, self._column_count)

    def get_item_row_at(self, index):
        return self._get_row_at(index, self._column_count)

    def get_pos_at(self, index, offset_x=0, offset_y=0):
        m_l, m_t, m_r, m_b = self._item_margins
        item_w, item_h = self._item_w+m_l+m_r, self._item_h+m_t+m_b
        return (
            self._x+self.get_item_column_at(index)*item_w-offset_x+m_l,
            self._y+self.get_item_row_at(index)*item_h-offset_y+m_t
        )

    def set_item_count(self, value):
        self._item_count = value

    def set_item_size(self, item_w, item_h):
        self._item_w, self._item_h = item_w, item_h

    def set_pos(self, x, y):
        self._x, self._y = x, y

    def set_size(self, w, h):
        self._w, self._h = w, h

    def update(self):
        # left，top，right，bottom
        if self._item_count:
            m_l, m_t, m_r, m_b = self._item_margins
            item_w, item_h = self._item_w+m_l+m_r, self._item_h+m_t+m_b
            self._column_count = self._to_column_count(self._w, item_w)
            self._column_count = min(self._column_count, self._item_count)
            self._row_count = self._get_row_count(self._item_count, self._column_count)
            self._abs_w, self._abs_h = self._get_abs_size(item_w, item_h, self._column_count, self._row_count)

    def get_geometry_at(self, index):
        x, y = self.get_pos_at(index)
        w, h = self._item_w, self._item_h
        return x, y, w, h

    def get_abs_size(self):
        return self._abs_w, self._abs_h

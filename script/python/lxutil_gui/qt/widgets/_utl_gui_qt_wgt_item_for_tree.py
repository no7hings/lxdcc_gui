# coding=utf-8
from lxutil_gui.qt.utl_gui_qt_core import *

import lxutil_gui.qt.abstracts as utl_gui_qt_abstract

from lxutil_gui.qt import utl_gui_qt_core


class QtTreeWidgetItem(
    QtWidgets.QTreeWidgetItem,
    utl_gui_qt_abstract.AbsQtItemDagLoading,
    #
    utl_gui_qt_abstract.AbsQtNameDef,
    #
    utl_gui_qt_abstract.AbsQtIconDef,
    utl_gui_qt_abstract.AbsQtShowForItemDef,
    utl_gui_qt_abstract.AbsQtMenuDef,
    #
    utl_gui_qt_abstract.AbsQtItemFilterDef,
    #
    utl_gui_qt_abstract.AbsQtStateDef,
    #
    utl_gui_qt_abstract.AbsQtDagDef,
    utl_gui_qt_abstract.AbsQtVisibleDef,
    #
    utl_gui_qt_abstract.AbsQtItemVisibleConnectionDef,
):
    ValidatorStatus = bsc_configure.ValidatorStatus
    def __init__(self, *args, **kwargs):
        super(QtTreeWidgetItem, self).__init__(*args, **kwargs)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        #
        self._set_item_dag_loading_def_init_(self)
        self._set_show_for_item_def_init_(self)
        #
        self._check_action_is_enable = True
        self._emit_send_enable = False
        #
        self._set_name_def_init_()
        self._set_icon_def_init_()
        self._set_menu_def_init_()
        #
        self._set_item_filter_def_init_()
        #
        self._set_state_def_init_()
        #
        self._set_dag_def_init_()
        self._set_visible_def_init_()
        #
        self._set_item_visible_connection_def_init_()

        self._signals = QtItemSignals()

        self._status = self.ValidatorStatus.Normal

    def setCheckState(self, column, state):
        self.setData(column, QtCore.Qt.CheckStateRole, state, emit_send_enable=False)

    def checkState(self, column):
        if self._check_action_is_enable is True:
            return self.data(column, QtCore.Qt.CheckStateRole)
        return QtCore.Qt.Unchecked

    def setData(self, column, role, value, **kwargs):
        emit_send_enable = False
        tree_widget = self.treeWidget()
        if role == QtCore.Qt.CheckStateRole:
            if self._check_action_is_enable is False:
                value = QtCore.Qt.Unchecked
            #
            emit_send_enable = kwargs.get('emit_send_enable', True)
        #
        super(QtTreeWidgetItem, self).setData(column, role, value)
        #
        if emit_send_enable is True:
            self._set_check_state_extra_(column)
            #
            check_state = self.checkState(column)
            checked = [False, True][check_state == QtCore.Qt.Checked]
            #
            tree_widget._set_item_check_action_run_(self, column)
            tree_widget._set_item_toggle_emit_send_(self, column, checked)
            tree_widget.update()

    def _set_child_add_(self):
        item = self.__class__()
        self.addChild(item)
        item._set_item_show_connect_()
        return item

    def _get_item_is_hidden_(self):
        return self.isHidden()

    def _refresh_widget_draw_(self):
        self._get_view_().update()

    def _set_icon_(self, icon, column=0):
        self._icon = icon
        self.setIcon(column, self._icon)

    def _set_icon_file_path_(self, file_path, column=0):
        self._icon_file_path = file_path
        self._icon = QtGui.QIcon()
        self._icon.addPixmap(
            QtGui.QPixmap(self._icon_file_path),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, self._icon)

    def _set_color_icon_rgb_(self, rgb, column=0):
        self.setIcon(
            column,
            utl_gui_qt_core.QtUtilMtd.get_color_icon(rgb)
        )

    def _set_icon_name_text_(self, text, column=0):
        self._icon_name_text = text
        icon = QtGui.QIcon()
        pixmap = QtPixmapMtd.get_by_name(
            self._icon_name_text,
            size=(14, 14)
        )
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.setIcon(column, icon)

    def _set_icon_state_update_(self, column=0):
        if column == 0:
            icon = QtGui.QIcon()
            pixmap = None
            if self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._icon_name_text is not None:
                pixmap = QtPixmapMtd.get_by_name(
                    self._icon_name_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                if self._icon_state in [
                    utl_gui_core.State.ENABLE,
                    utl_gui_core.State.DISABLE,
                    utl_gui_core.State.WARNING,
                    utl_gui_core.State.ERROR,
                    utl_gui_core.State.LOCKED,
                    utl_gui_core.State.LOST
                ]:
                    if self._icon_state == utl_gui_core.State.ENABLE:
                        background_color = Color.ENABLE
                    elif self._icon_state == utl_gui_core.State.DISABLE:
                        background_color = Color.DISABLE
                    elif self._icon_state == utl_gui_core.State.WARNING:
                        background_color = Color.WARNING
                    elif self._icon_state == utl_gui_core.State.ERROR:
                        background_color = Color.ERROR
                    elif self._icon_state == utl_gui_core.State.LOCKED:
                        background_color = Color.LOCKED
                    elif self._icon_state == utl_gui_core.State.LOST:
                        background_color = Color.LOST
                    else:
                        raise TypeError()
                    #
                    painter = QtPainter(pixmap)
                    rect = pixmap.rect()
                    x, y = rect.x(), rect.y()
                    w, h = rect.width(), rect.height()
                    #
                    border_color = QtBorderColors.Icon
                    #
                    s_w, s_h = w*.5, h*.5
                    state_rect = QtCore.QRect(
                        x, y+h-s_h, s_w, s_h
                    )
                    if self._icon_state == utl_gui_core.State.LOCKED:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=utl_gui_core.RscIconFile.get(
                                'state-locked'
                            )
                        )
                        painter.end()
                    elif self._icon_state == utl_gui_core.State.LOST:
                        painter._draw_icon_file_by_rect_(
                            state_rect,
                            file_path=utl_gui_core.RscIconFile.get(
                                'state-lost'
                            )
                        )
                        painter.end()
                    else:
                        painter._draw_frame_by_rect_(
                            state_rect,
                            border_color=border_color,
                            background_color=background_color,
                            border_radius=w/2
                        )
                        painter.end()
                #
                icon.addPixmap(
                    pixmap,
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.On
                )
                self.setIcon(column, icon)

    def _set_state_(self, state, column=0):
        self._icon_state = state
        #
        self._set_icon_state_update_(column)
        #
        if state == utl_gui_core.State.NORMAL:
            self.setForeground(
                column, QtGui.QBrush(Color.NORMAL)
            )
        elif state == utl_gui_core.State.ENABLE:
            self.setForeground(column, QtGui.QBrush(Color.ENABLE))
        elif state == utl_gui_core.State.DISABLE:
            self.setForeground(column, QtGui.QBrush(Color.DISABLE))
        elif state == utl_gui_core.State.WARNING:
            self.setForeground(column, QtGui.QBrush(Color.WARNING))
        elif state == utl_gui_core.State.ERROR:
            self.setForeground(column, QtGui.QBrush(Color.ERROR))
        elif state == utl_gui_core.State.LOCKED:
            self.setForeground(column, QtGui.QBrush(Color.LOCKED))
        elif state == utl_gui_core.State.LOST:
            self.setForeground(column, QtGui.QBrush(Color.LOST))
    # status
    def _set_status_(self, status, column=0):
        if status != self._status:
            self._status = status

            self._set_name_status_(status, column)
            #
            self._update_wgt_icon_(status, column)

    def _set_menu_content_(self, content):
        super(QtTreeWidgetItem, self)._set_menu_content_(content)
        self._update_wgt_icon_(status=None)

    def _set_name_status_(self, status, column=0):
        font = get_font()
        if status == self.ValidatorStatus.Normal:
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.NORMAL))
        elif status == self.ValidatorStatus.Correct:
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.CORRECT))
        elif status == self.ValidatorStatus.Warning:
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.WARNING))
        elif status == self.ValidatorStatus.Error:
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.ERROR))
        elif status == self.ValidatorStatus.Active:
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.ACTIVE))
        elif status == self.ValidatorStatus.Disable:
            font.setItalic(True)
            self.setFont(column, font)
            self.setForeground(column, QtGui.QBrush(Color.DISABLE))
        else:
            raise TypeError()

    def _update_wgt_icon_(self, status, column=0):
        if column == 0:
            icon = QtGui.QIcon()
            pixmap = None
            if self._icon:
                pixmap = self._icon.pixmap(20, 20)
            elif self._icon_file_path is not None:
                pixmap = QtGui.QPixmap(self._icon_file_path)
            elif self._icon_name_text is not None:
                pixmap = QtPixmapMtd.get_by_name(
                    self._icon_name_text,
                    size=(14, 14)
                )
            #
            if pixmap:
                painter = QtPainter(pixmap)
                rect = pixmap.rect()
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                #
                if status is not None:
                    draw_status = True
                    if status == self.ValidatorStatus.Normal:
                        draw_status = False
                        background_color = Color.NORMAL
                    elif status == self.ValidatorStatus.Correct:
                        background_color = Color.CORRECT
                    elif status == self.ValidatorStatus.Warning:
                        background_color = Color.WARNING
                    elif status == self.ValidatorStatus.Error:
                        background_color = Color.ERROR
                    elif status == self.ValidatorStatus.Active:
                        background_color = Color.ACTIVE
                    elif status == self.ValidatorStatus.Disable:
                        background_color = Color.DISABLE
                    else:
                        raise TypeError()
                    #
                    if draw_status is True:
                        border_color = QtBorderColors.Icon
                        #
                        s_w, s_h = w * .25, h * .25
                        status_rect = QtCore.QRect(
                            x + w - s_w - 1, y + h - s_h - 1, s_w, s_h
                        )
                        # draw status
                        painter._draw_frame_by_rect_(
                            rect=status_rect,
                            border_color=border_color,
                            background_color=background_color,
                            border_width=2,
                            border_radius=w / 2
                        )
                #
                if self._menu_content is not None:
                    m_w, m_h = w/2, h/2
                    menu_mark_rect = QtCore.QRect(
                        x, y, m_w, m_h
                    )
                    painter._draw_icon_file_by_rect_(
                        rect=menu_mark_rect,
                        file_path=utl_gui_core.RscIconFile.get('menu_mark'),
                    )

                painter.end()
            #
            icon.addPixmap(
                pixmap,
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
            self.setIcon(column, icon)

    def _get_status_(self, column=0):
        return self._status

    def _set_update_(self):
        tree_widget = self.treeWidget()
        tree_widget.update()

    def _set_user_data_(self, key, value, column=0):
        raw = self.data(column, QtCore.Qt.UserRole) or {}
        raw[key] = value
        self.setData(
            column, QtCore.Qt.UserRole, raw
        )

    def _get_user_data_(self, key, column=0):
        pass

    def _set_check_enable_(self, boolean, column=0):
        self._check_action_is_enable = boolean
        self.setData(column, QtCore.Qt.CheckStateRole, self.checkState(column))

    def _get_check_action_is_enable_(self):
        return self._check_action_is_enable

    def _set_emit_send_enable_(self, boolean):
        self._emit_send_enable = boolean

    def _get_emit_send_enable_(self):
        return self._emit_send_enable

    def _set_check_state_(self, boolean, column=0):
        self.setCheckState(
            column, [utl_gui_qt_core.QtCore.Qt.Unchecked, utl_gui_qt_core.QtCore.Qt.Checked][boolean]
        )

    def _set_check_state_extra_(self, column=0):
        if self._check_action_is_enable is True:
            check_state = self.checkState(column)
            descendants = self._get_descendants_()
            [i.setData(column, QtCore.Qt.CheckStateRole, check_state, emit_send_enable=False) for i in descendants]
            ancestors = self._get_ancestors_()
            [i.setData(column, QtCore.Qt.CheckStateRole, i._get_check_state_by_descendants(column), emit_send_enable=False) for i in ancestors]

    def _get_check_state_by_descendants(self, column):
        for i in self._get_descendants_():
            if i.checkState(column) == QtCore.Qt.Checked:
                return QtCore.Qt.Checked
        return QtCore.Qt.Unchecked

    def _get_children_(self):
        lis = []
        count = self.childCount()
        for i_index in range(count):
            i_item = self.child(i_index)
            lis.append(i_item)
        return lis

    def _get_descendants_(self):
        def _rcs_fnc(item_):
            _child_count = item_.childCount()
            for _child_index in range(_child_count):
                _child_item = item_.child(_child_index)
                lis.append(_child_item)
                _rcs_fnc(_child_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_ancestors_(self):
        def _rcs_fnc(item_):
            _parent_item = item_.parent()
            if _parent_item is not None:
                lis.append(_parent_item)
                _rcs_fnc(_parent_item)

        lis = []
        _rcs_fnc(self)
        return lis

    def _get_is_hidden_(self, ancestors=False):
        if ancestors is True:
            if self.isHidden():
                return True
            qt_tree_widget, qt_tree_widget_item = self.treeWidget(), self
            return QtTreeMtd.get_item_is_ancestor_hidden(qt_tree_widget, qt_tree_widget_item)
        else:
            return self.isHidden()

    def _get_name_texts_(self):
        column_count = self.treeWidget().columnCount()
        return [self.text(i) for i in range(column_count)]

    def _get_name_text_(self, column=0):
        return self.text(column)
    # show
    def _set_view_(self, widget):
        self._tree_widget = widget

    def _set_item_show_connect_(self):
        self._set_item_show_def_setup_(self.treeWidget())

    def _get_view_(self):
        return self.treeWidget()

    def _get_item_is_viewport_showable_(self):
        item = self
        view = self.treeWidget()
        parent = self.parent()
        if parent is None:
            return view._get_view_item_viewport_showable_(item)
        else:
            if parent.isExpanded():
                return view._get_view_item_viewport_showable_(item)
        return False

    def _set_item_widget_visible_(self, boolean):
        pass
        # self.setVisible(boolean)

    def _set_name_text_(self, text, column=0):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 1:
                    _ = '; '.join(('{}.{}'.format(seq+1, i) for seq, i in enumerate(text)))
                elif len(text) == 1:
                    _ = text[0]
                else:
                    _ = ''
            else:
                _ = unicode(text)
            #
            self.setText(column, _)
            self.setFont(column, utl_gui_qt_core.Font.NAME)

    def _set_tool_tip_(self, raw, column=0):
        if raw is not None:
            if isinstance(raw, (tuple, list)):
                _ = u'\n'.join(raw)
            elif isinstance(raw, six.string_types):
                _ = raw
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(
                _,
                column,
            )

    def _set_tool_tip_text_(self, text, column=0):
        if hasattr(self, 'setToolTip'):
            css = u'<html>\n<body>\n<style>.no_wrap{white-space:nowrap;}</style>\n<style>.no_warp_and_center{white-space:nowrap;text-align: center;}</style>\n'
            name_text_orig = self._get_name_text_orig_()
            if name_text_orig is not None:
                title_text = name_text_orig
            else:
                title_text = self._get_name_text_(column)
            #
            title_text = title_text.replace(u'<', u'&lt;').replace(u'>', u'&gt;')
            css += u'<h3><p class="no_warp_and_center">{}</p></h3>\n'.format(title_text)
            #
            css += u'<p><hr></p>\n'
            if isinstance(text, six.string_types):
                texts = text.split('\n')
            else:
                texts = text
            #
            for i in texts:
                css += u'<ul><li><i><p class="no_wrap">{}</p></i></li></ul>\n'.format(i)

            css += u'</body>\n</html>'
            # noinspection PyCallingNonCallable
            self.setToolTip(column, css)

    def _get_item_widget_(self):
        pass

    def _get_state_color_(self):
        return self.foreground(0)

    def _set_hidden_(self, boolean, ancestors=False):
        self.setHidden(boolean)
        if ancestors is True:
            [i.set_visible_by_has_visible_children() for i in self.get_ancestors()]
        #
        self._set_item_visible_connection_refresh_()
        if hasattr(self, 'gui_proxy'):
            self.gui_proxy.set_visible_connection_refresh()

    def _set_expanded_(self, boolean, ancestors=False):
        self.setExpanded(boolean)
        self._set_item_show_start_auto_()
        #
        if ancestors is True:
            [i._set_expanded_(boolean) for i in self._get_ancestors_()]

    def _clear_(self):
        self.takeChildren()

    def __str__(self):
        return '{}(names="{}")'.format(
            self.__class__.__name__, ', '.join(self._get_name_texts_())
        )

    def __repr__(self):
        return self.__str__()
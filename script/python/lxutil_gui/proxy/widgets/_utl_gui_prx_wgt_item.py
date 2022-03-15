# coding:utf-8
from lxutil import utl_core

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_item

from lxutil_gui.qt import utl_gui_qt_core


class AbsPrxTreeDef(object):
    def _set_prx_tree_def_init_(self):
        pass
    @classmethod
    def _set_item_add_(cls, add_method, *args, **kwargs):
        if kwargs:
            if 'name' in kwargs:
                _name = kwargs['name']
                if isinstance(_name, (tuple, list)):
                    name = _name
                else:
                    name = [_name]
            else:
                name = None
            #
            if 'item_class' in kwargs:
                item_class = kwargs['item_class']
            else:
                item_class = PrxTreeItem
            #
            if 'tool_tip' in kwargs:
                _tool_tip = kwargs['tool_tip']
                if isinstance(_tool_tip, (tuple, list)):
                    tool_tip = _tool_tip
                else:
                    tool_tip = [_tool_tip]
            else:
                tool_tip = None
            #
            if 'icon' in kwargs:
                _file_icon = kwargs['icon']
                if isinstance(_file_icon, (tuple, list)):
                    file_icons = _file_icon
                else:
                    file_icons = [_file_icon]
            else:
                file_icons = None
            #
            if 'name_icon' in kwargs:
                _name_icon = kwargs['name_icon']
                if isinstance(_name_icon, (tuple, list)):
                    name_icons = _name_icon
                else:
                    name_icons = [_name_icon]
            else:
                name_icons = None
            #
            if 'menu' in kwargs:
                menu = kwargs['menu']
            else:
                menu = None
        else:
            name = None
            item_class = PrxTreeItem
            tool_tip = None
            file_icons = None
            name_icons = None
            menu = None
        #
        if args:
            name = args
        #
        item_prx = item_class()
        #
        if name is not None:
            for column, name_ in enumerate(name):
                item_prx.set_name(name_, column)
        #
        if tool_tip is not None:
            for column, tool_tip_ in enumerate(tool_tip):
                item_prx.set_tool_tip(tool_tip_, column)
        #
        if file_icons is not None:
            for column, i_file_icon in enumerate(file_icons):
                if i_file_icon is not None:
                    item_prx.set_file_icon(i_file_icon, column)
        #
        if name_icons is not None:
            for column, i_name_icon in enumerate(name_icons):
                if i_name_icon is not None:
                    item_prx.set_icon_by_name(i_name_icon, column)
        #
        if name is not None:
            pass
        #
        if menu is not None:
            item_prx.set_gui_menu_raw(menu)
        #
        add_method(item_prx.widget)
        item_prx.widget._set_item_show_connect_()
        #
        if 'filter_key' in kwargs:
            _filter_key = kwargs['filter_key']
            view_prx = item_prx.get_view()
            view_prx._item_dict[_filter_key] = item_prx
        return item_prx


class PrxTreeItemCheckState(object):
    def __init__(self, prx_tree_item):
        self._item_prx = prx_tree_item
    @property
    def widget(self):
        return self._item_prx.widget
    @property
    def item(self):
        return self._item_prx

    def set(self, check_tag, column=0):
        if 'ignore' in check_tag:
            self.set_ignored(column)
        elif 'error' in check_tag:
            self.set_error(column)
        elif 'warning' in check_tag:
            self.set_warning(column)
        else:
            self.set_passed(column)

    def set_normal(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.default_text)
        self._item_prx.set_gui_attribute(
            'state', 'normal'
        )

    def set_error(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.error_text)
        self._item_prx.set_gui_attribute(
            'state', 'error'
        )

    def set_warning(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.warning_text)
        self._item_prx.set_gui_attribute(
            'state', 'warning'
        )

    def set_passed(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.adopt_text)
        self._item_prx.set_gui_attribute(
            'state', 'adopt'
        )

    def set_ignored(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.temporary_text)
        self._item_prx.set_gui_attribute(
            'state', 'temporary'
        )


class PrxTreeItem(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxMenuDef,
    AbsPrxTreeDef,
    utl_gui_prx_abstract._PrxStateDef,
    #
    utl_gui_prx_abstract.AbsPrxItemFilterTgtDef,
    utl_gui_prx_abstract.AbsPrxItemVisibleConnectionDef
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item.QtTreeWidgetItem
    def __init__(self, *args, **kwargs):
        super(PrxTreeItem, self).__init__(*args, **kwargs)
        self._set_prx_tree_def_init_()
        #
        self._gui_menu_raw = []
        self._menu_title = None

        self._loading_item_prx = None
    @property
    def item(self):
        return self._qt_widget

    def set_name(self, text, column=0):
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
            self.widget.setText(column, _)
            self.widget.setFont(column, utl_gui_qt_core.Font.NAME)

    def get_name(self, column=0):
        return self.widget.text(column)

    def get_names(self):
        qt_tree_widget = self.widget.treeWidget()
        column_count = qt_tree_widget.columnCount()
        return [self.get_name(i) for i in range(column_count)]

    def set_names(self, texts):
        for column, text in enumerate(texts):
            self.set_name(text, column)

    def get_path(self):
        parent = self.get_parent()
        if parent:
            if parent.get_name() != '/':
                return '{}/{}'.format(parent.get_path(), self.get_name())
            return '/{}'.format(self.get_name())
        return '/'

    def set_file_icon(self, icon, column=0):
        if isinstance(icon, (str, unicode)):
            self.widget._set_icon_file_path_(icon, column)
        elif isinstance(icon, utl_gui_qt_core.QtGui.QIcon):
            qt_icon = icon
            self.widget.setIcon(column, qt_icon)

    def set_color_icon(self, color, column=0):
        self.widget._set_color_icon_rgb_(color, column)

    def set_icon_by_name(self, text, column=0):
        self.widget._set_name_icon_text_(text, column)

    def get_parent(self):
        _ = self.widget.parent()
        if _ is not None:
            return _.gui_proxy

    def get_ancestors(self):
        return [i.gui_proxy for i in self.item._get_ancestors_()]

    def set_child_add(self, *args, **kwargs):
        return self._set_item_add_(
            self.widget.addChild,
            *args, **kwargs
        )

    def set_children_clear(self):
        self.widget.takeChildren()

    def get_children(self):
        lis = []
        count = self.widget.childCount()
        if count:
            for i in range(count):
                qt_tree_item = self.widget.child(i)
                lis.append(qt_tree_item.gui_proxy)
        return lis

    def get_descendants(self):
        return [i.gui_proxy for i in self.widget._get_descendants_()]

    def get_gui_menu_raw(self):
        return self._gui_menu_raw

    def set_gui_menu_raw(self, raw):
        if isinstance(raw, list):
            self._gui_menu_raw = raw

    def set_gui_menu_raw_append(self, raw):
        self._gui_menu_raw.append(raw)

    def set_gui_menu_raw_extend(self, raw):
        self._gui_menu_raw.extend(raw)

    def set_tool_tip(self, text, column=0):
        if text is not None:
            if isinstance(text, (tuple, list)):
                if len(text) > 0:
                    _ = u'\n'.join((u'{}'.format(i) for seq, i in enumerate(text)))
                elif len(text) == 1:
                    _ = text[0]
                else:
                    _ = u''
            else:
                _ = unicode(text)
            #
            self.widget.setToolTip(column, _)

    def set_tool_tips(self, texts):
        for column, text in enumerate(texts):
            self.set_tool_tip(text, column)
    # checked
    def set_checked(self, boolean=True, extra=False, column=0):
        self.widget.setCheckState(column, [utl_gui_qt_core.QtCore.Qt.Unchecked, utl_gui_qt_core.QtCore.Qt.Checked][boolean])
        if extra is True:
            self.widget._set_check_state_extra_(column)

    def get_check_enable(self):
        return self.widget._get_item_is_check_enable_()

    def set_check_enable(self, boolean, descendants=False, column=0):
        self.widget.setDisabled(not boolean)
        self.widget.setForeground(column, [utl_gui_qt_core.Brush.temporary_text, utl_gui_qt_core.Brush.default_text][boolean])
        self.widget._set_check_enable_(boolean, column=column)
        if descendants is True:
            [i.set_check_enable(boolean, column=column) for i in self.get_descendants()]

    def get_is_checked(self, column=0):
        return [False, True][self.widget.checkState(column) == utl_gui_qt_core.QtCore.Qt.Checked]
    # expanded
    def set_expanded(self, boolean=True, ancestors=False):
        self.widget.setExpanded(boolean)
        if ancestors is True:
            [i.set_expanded(boolean) for i in self.get_ancestors()]
    # expand
    def set_expand(self, ancestors=False):
        self.widget.setExpanded(True)
        if ancestors is True:
            [i.widget.setExpanded(True) for i in self.get_ancestors()]

    def set_ancestors_expand(self):
        [i.widget.setExpanded(True) for i in self.get_ancestors()]

    def set_expand_branch(self):
        self.set_expand()
        descendants = self.get_descendants()
        [i.set_expand() for i in descendants]

    def set_expand_branch_by_condition(self, condition_fnc, conditions):
        self.set_expand()
        match_prx_items = []
        descendants = self.get_descendants()
        for i in descendants:
            i_condition = condition_fnc(i)
            if i_condition in conditions:
                match_prx_items.append(i)
            i.set_collapse()
        #
        [i.set_ancestors_expand() for i in match_prx_items]
    # collapse
    def set_collapse(self):
        self.widget.setExpanded(False)

    def set_collapse_branch(self):
        self.set_collapse()
        descendants = self.get_descendants()
        [i.set_collapse() for i in descendants]
    # select
    def set_select(self):
        self.widget.setSelected(True)
    # hidden
    def set_hidden(self, boolean=True, ancestors=False):
        self.widget.setHidden(boolean)
        self.set_gui_attribute('visible', not boolean)
        if ancestors is True:
            [i.set_visible_by_has_visible_children() for i in self.get_ancestors()]
        #
        self.set_visible_connection_refresh()

    def get_is_hidden(self, ancestors=False):
        return self.widget._get_is_hidden_(ancestors=ancestors)

    def set_emit_send_enable(self, boolean):
        self.widget._set_emit_send_enable_(boolean)

    def set_visible(self, boolean, ancestors=False):
        self.set_hidden(not boolean, ancestors=ancestors)

    def get_is_visible(self):
        pass

    def set_force_hidden(self, boolean):
        self.set_gui_attribute('force_hidden', boolean)
        self.set_hidden(boolean)

    def get_is_force_hidden(self):
        return self.get_gui_attribute('force_hidden') or False

    def set_tag_filter_tgt_key_add(self, key, ancestors=False):
        utl_gui_prx_abstract.AbsPrxItemFilterTgtDef.set_tag_filter_tgt_key_add(
            self, key
        )
        if ancestors is True:
            self._set_tag_filter_tgt_ancestors_update_()

    def _set_tag_filter_tgt_ancestors_update_(self):
        parent_item_prxes = self.get_ancestors()
        tag_filter_tgt_mode = self.get_tag_filter_tgt_mode()
        tag_filter_tgt_keys = self.get_tag_filter_tgt_keys()
        for parent_item_prx in parent_item_prxes:
            for tag_filter_tgt_key in tag_filter_tgt_keys:
                parent_item_prx.set_tag_filter_tgt_key_add(tag_filter_tgt_key)
            #
            parent_item_prx.set_tag_filter_tgt_mode(tag_filter_tgt_mode)
            parent_item_prx.set_tag_filter_tgt_statistic_enable(False)

    def set_tag_filter_src_key_add(self, key):
        lis = self.get_gui_attribute(
            'tag_filter_src_keys',
            default=[]
        )
        if key not in lis:
            lis.append(key)
        #
        self.set_gui_attribute('tag_filter_src_keys', lis)

    def get_tag_filter_src_keys(self):
        return self.get_gui_attribute(
            'tag_filter_src_keys',
            default=[]
        )

    def _set_tag_filter_hidden_(self, boolean):
        self.set_gui_attribute('tag_filter_hidden', boolean)

    def get_is_tag_filter_hidden(self):
        return self.get_gui_attribute('tag_filter_hidden') or False
    # keyword-filter
    def set_keyword_filter_enable(self, boolean):
        self.set_gui_attribute('keyword_filter_enable', boolean)

    def get_keyword_filter_enable(self):
        return self.get_gui_attribute('keyword_filter_enable', default=False)

    def _set_keyword_filter_hidden_(self, boolean):
        self.set_gui_attribute('keyword_filter_hidden', boolean)

    def get_is_keyword_filter_hidden(self):
        return self.get_gui_attribute('keyword_filter_hidden') or False

    def get_has_visible_children(self):
        return utl_gui_qt_core.QtTreeMtd._get_item_has_visible_children_(
            self.widget.treeWidget(),
            self.widget
        )

    def set_visible_by_has_visible_children(self):
        self.set_visible(
            self.get_has_visible_children()
        )

    def _get_all_branch_items_(self):
        def _rcs_fnc(item_proxy_):
            lis.append(item_proxy_)
            _parent = item_proxy_.get_parent()
            if _parent is not None:
                _rcs_fnc(_parent)

        lis = []
        _rcs_fnc(self)
        return lis

    def set_foregrounds_raw(self, raw, column=0):
        _ = self.widget.data(column, utl_gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        #
        user_data['foregrounds'] = raw
        self.widget.setData(column, utl_gui_qt_core.QtCore.Qt.UserRole, user_data)

    def set_states_raw(self, raw, column=0):
        _ = self.widget.data(column, utl_gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        user_data['states'] = raw
        self.widget.setData(
            column,
            utl_gui_qt_core.QtCore.Qt.UserRole,
            user_data
        )
    # noinspection PyUnusedLocal
    def get_state(self, column=0):
        return self.get_gui_attribute(
            'state', 'normal'
        )
    # noinspection PyUnusedLocal
    def set_state(self, state, column=0):
        self.set_gui_attribute(
            'state', state
        )
        self.widget._set_state_(state, column)

    def get_view(self):
        qt_tree_view = self.widget.treeWidget()
        return qt_tree_view.gui_proxy

    def _set_filter_keyword_(self, keyword, column=0):
        _ = self.widget.data(column, utl_gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        #
        user_data['filter_keyword'] = keyword
        self.widget.setData(
            column, utl_gui_qt_core.QtCore.Qt.UserRole,
            user_data
        )

    def _set_filter_occurrence_(self, boolean, column=0):
        _ = self.widget.data(column, utl_gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        #
        user_data['filter_occurrence'] = boolean
        self.widget.setData(
            column, utl_gui_qt_core.QtCore.Qt.UserRole,
            user_data
        )
    #
    def set_visible_connect_to(self, key, prx_item_tgt):
        self.set_visible_src_key(key)
        self.set_visible_tgt_view(prx_item_tgt.get_view())
        # print self, self.get_visible_src_key(), "AAA"
        prx_item_tgt.set_visible_tgt_key(key)
        prx_item_tgt.set_hidden(self.get_is_hidden())

    def set_visible_tgt_view(self, view_prx):
        self.set_gui_attribute(
            'visible_tgt_view',
            view_prx
        )

    def get_visible_tgt_view(self):
        return self.get_gui_attribute('visible_tgt_view')

    def set_visible_connection_refresh(self):
        src_item_prx = self
        src_key = src_item_prx.get_visible_src_key()
        if src_key is not None:
            tgt_view_prx = src_item_prx.get_visible_tgt_view()
            if tgt_view_prx is not None:
                tgt_raw = tgt_view_prx.get_visible_tgt_raw()
                if src_key in tgt_raw:
                    tgt_item_prxes = tgt_raw[src_key]
                    for prx_item_tgt in tgt_item_prxes:
                        prx_item_tgt.set_hidden(self.get_is_hidden())
                        prx_item_tgt.widget._get_list_widget_item_()._set_item_show_update_()

    def set_loading_start(self):
        view = self.get_view()
        item_prx = self.set_child_add(
            'loading',
            icon=utl_core.Icon.get('refresh')
        )
        self._loading_item_prx = item_prx
        view.set_loading_item_add(self._loading_item_prx)

    def set_loading_end(self):
        if self._loading_item_prx is not None:
            view = self.get_view()
            self.widget.takeChild(
                self.widget.indexOfChild(self._loading_item_prx.widget)
            )
            self._loading_item_prx = None
            view.set_loading_item_remove(self._loading_item_prx)

    def set_show_method(self, method):
        self.widget._set_item_show_method_(method)

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(self.get_names())
        )

    def __repr__(self):
        return self.__str__()


class PrxLabelTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxLabelTreeItem, self).__init__(*args, **kwargs)
        self.set_normal_state()

    def set_normal_state(self):
        self.set_file_icon(utl_core.Icon.get('tag'))
        self.set_foreground_update(utl_gui_qt_core.Brush.default_text)

    def set_error_state(self):
        self.set_file_icon(utl_core.Icon.get('error'))
        self.set_foreground_update(utl_gui_qt_core.Brush.error_text)

    def set_warning_state(self):
        self.set_file_icon(utl_core.Icon.get('warning'))
        self.set_foreground_update(utl_gui_qt_core.Brush.warning_text)

    def set_adopt_state(self):
        self.set_file_icon(utl_core.Icon.get('adopt'))
        self.set_foreground_update(utl_gui_qt_core.Brush.adopt_text)

    def set_disable_state(self):
        self.set_file_icon(utl_core.Icon.get('disable'))
        self.set_foreground_update(utl_gui_qt_core.Brush.disable_text)

    def set_temporary_state(self):
        self.set_file_icon(utl_core.Icon.get('temporary'))
        self.set_foreground_update(utl_gui_qt_core.Brush.temporary_text)

    def set_foreground_update(self, qt_brush):
        qt_tree_widget = self.widget.treeWidget()
        if qt_tree_widget is not None:
            for column in range(qt_tree_widget.columnCount()):
                self.widget.setForeground(column, qt_brush)
        else:
            self.widget.setForeground(0, qt_brush)


class PrxLoadingTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxLoadingTreeItem, self).__init__(*args, **kwargs)
        self.set_name('loading ...')
        self.set_file_icon(utl_core.Icon.get('refresh'))


class PrxObjTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxObjTreeItem, self).__init__(*args, **kwargs)
        self.widget.setForeground(0, utl_gui_qt_core.Brush.default_text)
        # self.set_file_icon(utl_core.Icon.get('tag'))
        self.set_normal_state()
    @property
    def check_state(self):
        return PrxTreeItemCheckState(self)

    def set_temporary_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.temporary_text)
        self.set_gui_attribute(
            'state', 'temporary'
        )

    def set_normal_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.default_text)
        self.set_gui_attribute(
            'state', 'normal'
        )

    def set_error_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.error_text)
        self.set_gui_attribute(
            'state', 'error'
        )

    def set_warning_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.warning_text)
        self.set_gui_attribute(
            'state', 'warning'
        )

    def set_adopt_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.adopt_text)
        self.set_gui_attribute(
            'state', 'adopt'
        )

    def set_current_state(self, column=0):
        self.widget.setForeground(column, utl_gui_qt_core.Brush.current_text)
        self.set_gui_attribute(
            'state', 'current'
        )


class PrxDccObjTreeItem(PrxObjTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxDccObjTreeItem, self).__init__(*args, **kwargs)


class PrxStgObjTreeItem(PrxObjTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxStgObjTreeItem, self).__init__(*args, **kwargs)
        # self.widget.setForeground(0, utl_gui_qt_core.Brush.default_text)


class PrxListItem(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxMenuDef,
    #
    utl_gui_prx_abstract.AbsPrxItemFilterTgtDef,
    utl_gui_prx_abstract.AbsPrxItemVisibleConnectionDef
):
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_item._QtListItemWidget
    def __init__(self, *args, **kwargs):
        super(PrxListItem, self).__init__(*args, **kwargs)
        self._visible_tgt_key = None
    @property
    def item(self):
        return self._qt_widget._get_item_()

    def set_gui_menu_raw(self, raw):
        self.widget._set_menu_raw_(raw)

    def set_index(self, index):
        self.widget._set_index_(index)

    def set_pixmap_icons(self, icons):
        self.widget._set_pixmap_icons_(icons)

    def set_file_icon(self, icon_name=None, icon_file_path=None):
        if icon_file_path is not None:
            self.widget._set_icon_file_path_(
                icon_file_path
            )
        elif icon_name is not None:
            self.widget._set_name_icon_text_(
                utl_core.Icon.get(icon_name)
            )

    def set_file_icons(self, icon_names=None, icon_file_paths=None):
        if isinstance(icon_names, (tuple, list)):
            self.widget._set_icon_file_paths_(
                [utl_core.Icon.get(i) for i in icon_names]
            )
        elif isinstance(icon_file_paths, (tuple, list)):
            self.widget._set_icon_file_paths_(icon_file_paths)

    def set_file_icon_add(self, icon_name):
        self.widget._set_icon_file_path_add_(
            utl_core.Icon.get(icon_name)
        )

    def set_icon_by_name(self, text):
        self.widget._set_name_icon_text_(
            text
        )

    def set_icon_frame_size(self, w, h):
        self.widget._set_icon_frame_size_(w, h)

    def set_icon_size(self, w, h):
        self.widget._set_icon_size_(w, h)

    def set_name(self, name_text):
        self.widget._set_name_text_(name_text)

    def set_names(self, name_texts):
        self.widget._set_name_texts_(name_texts)

    def get_names(self):
        return self.widget._get_name_texts_()

    def set_name_frame_border_color(self, color):
        return self.widget._set_name_frame_border_color_(color)

    def set_name_frame_background_color(self, color):
        return self.widget._set_name_frame_background_color_(color)

    def set_image(self, file_path):
        self.widget._set_image_file_path_(file_path)

    def set_image_by_name(self, text):
        self.widget._set_image_name_text_(text)

    def set_image_by_file(self, file_path):
        self.widget._set_image_file_path_(file_path)

    def set_image_size(self, size):
        pass

    def set_image_show_sub_process(self, sub_process):
        self.widget._get_item_()._set_item_show_sub_process_(sub_process)

    def set_visible_tgt_key(self, key):
        self.set_gui_attribute(
            'visible_tgt_key',
            key
        )

    def get_visible_tgt_key(self):
        return self.get_gui_attribute('visible_tgt_key')

    def get_view(self):
        return self.get_gui_attribute(
            'view_prx'
        )

    def set_view(self, view_prx):
        self.set_gui_attribute(
            'view_prx',
            view_prx
        )

    def set_hidden(self, boolean=True):
        self.widget.setHidden(boolean)
        self.widget._get_list_widget_item_().setHidden(boolean)

    def set_force_hidden(self, boolean):
        self.set_gui_attribute('force_hidden', boolean)
        self.set_hidden(boolean)

    def set_tool_tip(self, text):
        self.widget._set_tool_tip_(text)

    def set_border_color(self, color):
        self.widget._set_border_color_(color)

    def set_show_method(self, method):
        self.widget._get_item_()._set_item_show_method_(method)

    def set_image_loading_start(self):
        self.widget._get_item_()._set_item_show_image_loading_start_()

    def set_press_clicked_connect_to(self, fnc):
        self.widget.press_clicked.connect(fnc)

    def set_press_db_clicked_connect_to(self, fnc):
        self.widget.press_db_clicked.connect(fnc)

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(self.get_names())
        )

    def __repr__(self):
        return self.__str__()

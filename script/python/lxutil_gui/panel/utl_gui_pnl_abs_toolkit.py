# coding:utf-8
import six

import fnmatch

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxbasic.objects as bsc_objects

import lxutil_gui.qt.widgets as qt_widgets


class AbsToolkitPanel(prx_widgets.PrxToolWindow):
    CONFIGURE_FILE_PATH = None
    #
    COLUMN_COUNT = 2
    def __init__(self, *args, **kwargs):
        super(AbsToolkitPanel, self).__init__(*args, **kwargs)
        self._toolkit_configure = bsc_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        #
        self.set_window_title(self._toolkit_configure.get('window.name'))
        self.set_definition_window_size(self._toolkit_configure.get('window.size'))
        #
        self.get_log_bar().set_expanded(True)
        #
        self._item_prxes = []

    def _set_build_by_configure_(self, configure):
        self._prx_widgets_module = bsc_objects.PyModule('lxutil_gui.proxy.widgets')
        group_keys = configure.get_branch_keys('central.groups')
        for group_key in group_keys:
            name = configure.get('central.groups.{}.name'.format(group_key))
            prx_type = configure.get('central.groups.{}.type'.format(group_key))
            prx_path = configure.get('central.groups.{}.path'.format(group_key))
            #
            prx_group_method = self._prx_widgets_module.get_method(prx_type)
            prx_group = prx_group_method()
            prx_group.set_name(name)
            prx_group.set_expanded(True)
            self.set_widget_add(prx_group)
            #
            qt_widget = qt_widgets.QtWidget()
            prx_group.set_widget_add(qt_widget)
            qt_layout = qt_widgets.QtGridLayout(qt_widget)
            qt_layout.setSpacing(4)
            #
            item_keys = configure.get_branch_keys('central.groups.{}.items'.format(group_key))
            count = len(item_keys)
            for seq, item_key in enumerate(item_keys):
                item_configure = configure.get_content(
                    'central.groups.{}.items.{}'.format(group_key, item_key)
                )
                r = int(seq/self.COLUMN_COUNT)
                c = seq % self.COLUMN_COUNT
                w, h = 1, 1
                #
                item_prx = self._set_item_prx_create_by_configure_(item_configure)
                qt_layout.addWidget(item_prx.widget, r, c, w, h)
        #
        button_keys = configure.get_branch_keys('bottom.buttons')
        for seq, button_key in enumerate(button_keys):
            item_configure = configure.get_content('bottom.buttons.{}'.format(button_key))
            name = item_configure.get('name')
            description = item_configure.get('description')
            prx_type = item_configure.get('type')
            click_method = item_configure.get('click_method')
            item_prx_cls = self._prx_widgets_module.get_method(prx_type)
            item_prx = item_prx_cls()
            item_prx.set_name(name)
            item_prx.set_icon_by_name_text(name)
            item_prx.set_tool_tip(description)
            item_prx.widget._set_progress_value_(5)
            self.set_button_add(item_prx)
            if click_method:
                if hasattr(self, click_method) is True:
                    method = self.__getattribute__(click_method)
                    item_prx.set_press_clicked_connect_to(
                        lambda *args, **kwargs: method(item_prx)
                    )
    @classmethod
    def _get_click_fnc_(cls, cmd_str):
        exec cmd_str

    def get_item_prxes(self):
        return self._item_prxes
    @utl_core.Modifier.exception_catch
    def _set_method_run_(self, method):
        method()

    @utl_core.Modifier.exception_catch
    def _set_method_run_with_status_(self, method, item_prx):
        method(item_prx)

    def _set_item_prx_create_by_configure_(self, item_configure):
        name = item_configure.get('name')
        icon = item_configure.get('icon')
        description = item_configure.get('description')
        check_enable = item_configure.get('check_enable') or False
        checked = item_configure.get('checked') or False
        prx_path = item_configure.get('path')
        prx_type = item_configure.get('type')
        #
        click_method = item_configure.get('click_method')
        click_status_enable = item_configure.get('click_status_enable')
        click_command = item_configure.get('click_command')
        option_attributes = item_configure.get('option.attributes')
        #
        item_prx_cls = self._prx_widgets_module.get_method(prx_type)
        item_prx = item_prx_cls()
        #
        if check_enable is True:
            item_prx.set_check_enable(check_enable)
            item_prx.set_checked(checked)
        #
        item_prx.set_name(name)
        item_prx.set_icon_by_name_text(name)
        item_prx.set_tool_tip(description)
        if click_method:
            if hasattr(self, click_method) is True:
                method = self.__getattribute__(click_method)
                item_prx.set_enable(True)
                if option_attributes is not None:
                    item_prx.set_option_click_enable(True)
                    item_prx.set_press_clicked_connect_to(
                        lambda: self._set_option_create_(name, method, option_attributes)
                    )
                else:
                    if click_status_enable is True:
                        item_prx.set_press_clicked_connect_to(
                            lambda *args, **kwargs: self._set_method_run_with_status_(method, item_prx)
                        )
                    else:
                        item_prx.set_press_clicked_connect_to(
                            lambda *args, **kwargs: self._set_method_run_(method)
                        )
            else:
                item_prx.set_enable(False)
        #
        elif click_command:
            item_prx.set_press_clicked_connect_to(lambda *args, **kwargs: self._get_click_fnc_(click_command))
        else:
            item_prx.set_enable(False)
        #
        self._item_prxes.append(item_prx)
        return item_prx

    def _set_option_create_(self, name, method, attributes):
        prx_node_cls = self._prx_widgets_module.get_method('PrxNode')
        prx_node = prx_node_cls()
        self.set_option_unit_name(name)
        self.set_option_unit_show()
        self.set_option_unit_clear()
        #
        for k, v in attributes.items():
            key = k
            name = v['name']
            type_ = v['type']
            value = v['value']
            #
            if isinstance(value, six.string_types):
                if fnmatch.filter([value], 'fnc(*)'):
                    value = eval(value[4:-1])
            #
            prx_port_method = prx_node.get_port_cls(type_)
            prx_port = prx_port_method(key, name)
            prx_node.set_port_add(prx_port)
            prx_port.set(value)
        #
        self.get_option_unit_layout().addWidget(prx_node.widget)
        #
        widget = qt_widgets.QtWidget()
        widget.setMaximumHeight(24)
        widget.setMinimumHeight(24)
        self.get_option_unit_layout().addWidget(widget)
        layout = qt_widgets.QtHBoxLayout(widget)
        #
        apply_button = prx_widgets.PrxPressItem()
        layout.addWidget(apply_button.widget)
        apply_button.set_name('Apply')
        apply_button.set_icon_by_name_text('Apply')
        #
        apply_button.set_press_clicked_connect_to(
            lambda: method(**prx_node.get_as_kwargs())
        )
        apply_and_close_button = prx_widgets.PrxPressItem()
        layout.addWidget(apply_and_close_button.widget)
        apply_and_close_button.set_name('Apply and Close')
        apply_and_close_button.set_icon_by_name_text('Apply and Close')
        apply_and_close_button.set_press_clicked_connect_to(
            lambda: method(**prx_node.get_as_kwargs())
        )
        apply_and_close_button.set_press_clicked_connect_to(
            self.set_option_unit_hide
        )
        #
        close_button = prx_widgets.PrxPressItem()
        layout.addWidget(close_button.widget)
        close_button.set_name('Close')
        close_button.set_icon_by_name_text('Close')
        close_button.set_press_clicked_connect_to(
            self.set_option_unit_hide
        )

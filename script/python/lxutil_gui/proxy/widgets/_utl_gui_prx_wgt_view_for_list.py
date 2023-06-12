# coding:utf-8
import fnmatch

import collections

import functools

from lxbasic import bsc_core

from lxutil_gui import utl_gui_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_entry_base, _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_view_for_list

from lxutil_gui.proxy import utl_gui_prx_abstract

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_item


class PrxListView(
    utl_gui_prx_abstract.AbsPrxWidget,
    utl_gui_prx_abstract.AbsPrxViewDef,
    #
    utl_gui_prx_abstract.AbsPrxViewFilterTagDef,
    #
    utl_gui_prx_abstract.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLS = _utl_gui_qt_wgt_entry_base.QtEntryFrame
    QT_VIEW_CLS = _utl_gui_qt_wgt_view_for_list.QtListWidget
    #
    FILTER_MAXIMUM = 50
    def __init__(self, *args, **kwargs):
        super(PrxListView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._prx_top_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._prx_top_tool_bar.set_alignment_left()
        self._qt_layout_0.addWidget(self._prx_top_tool_bar.widget)
        self._prx_top_tool_bar.set_border_radius(1)
        # check
        self._prx_check_tool_box = _utl_gui_prx_wdt_utility.PrxHToolBox()
        self._prx_top_tool_bar.add_widget(self._prx_check_tool_box)
        self._prx_check_tool_box.set_expanded(True)
        self._prx_check_tool_box.set_visible(False)
        #
        self._check_all_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._check_all_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_checked'))
        self._prx_check_tool_box.add_widget(self._check_all_button)
        self._check_all_button.clicked.connect(self.__check_all_items)
        self._check_all_button._set_tool_tip_text_(
            '"LMB click" for checked all items'
        )
        #
        self._uncheck_all_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._uncheck_all_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_unchecked'))
        self._prx_check_tool_box.add_widget(self._uncheck_all_button)
        self._uncheck_all_button.clicked.connect(self.__uncheck_all_items)
        self._uncheck_all_button._set_tool_tip_text_(
            '"LMB click" for unchecked all items'
        )
        # mode switch
        self._prx_mode_switch_tool_box = _utl_gui_prx_wdt_utility.PrxHToolBox()
        self._prx_top_tool_bar.add_widget(self._prx_mode_switch_tool_box)
        self._prx_mode_switch_tool_box.set_expanded(True)
        #
        self._view_mode_swap_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._prx_mode_switch_tool_box.add_widget(self._view_mode_swap_button)
        self._view_mode_swap_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('grid_mode'))
        self._view_mode_swap_button.clicked.connect(self.__swap_view_mode)
        self._view_mode_swap_button._set_tool_tip_text_(
            '"LMB click" for switch view mode to "icon" / "list"'
        )
        # scale switch
        self._prx_scale_switch_tool_box = _utl_gui_prx_wdt_utility.PrxHToolBox()
        self._prx_top_tool_bar.add_widget(self._prx_scale_switch_tool_box)
        self._prx_scale_switch_tool_box.set_expanded(True)
        self._prx_scale_switch_tool_box.set_visible(False)
        # sort
        self._prx_sort_switch_tool_box = _utl_gui_prx_wdt_utility.PrxHToolBox()
        self._prx_top_tool_bar.add_widget(self._prx_sort_switch_tool_box)
        self._prx_sort_switch_tool_box.set_expanded(True)
        self._prx_sort_switch_tool_box.set_visible(False)
        # filter
        self._prx_filter_tool_box = _utl_gui_prx_wdt_utility.PrxHToolBox()
        self._prx_top_tool_bar.add_widget(self._prx_filter_tool_box)
        self._prx_filter_tool_box.set_expanded(True)
        self._prx_filter_tool_box.set_size_mode(1)
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_filter_tool_box.add_widget(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_layout_0.addWidget(self._qt_view)
        self._set_prx_view_def_init_(self._qt_view)
        self._qt_view._set_sort_enable_(True)
        #
        self._qt_info_chart = _utl_gui_qt_wgt_chart.QtInfoChart()
        self._qt_info_chart.hide()
        self._qt_layout_0.addWidget(self._qt_info_chart)
        self._qt_view.info_text_accepted.connect(
            self._qt_info_chart._set_info_text_
        )
        #
        self._prx_filter_bar = self._prx_filer_bar_0

        self._item_dict = collections.OrderedDict()
        self._filter_completion_cache = None

        self.__add_scale_switch_tools()
        self.__add_sort_mode_switch_tools()

        self._prx_filter_bar._qt_widget.user_entry_changed.connect(
            self.__keyword_filter_cbk
        )
        self._qt_view._set_view_keyword_filter_bar_(self._prx_filter_bar._qt_widget)
        self._prx_filter_bar._qt_widget._set_completion_extra_gain_fnc_(self.__keyword_filter_completion_gain_fnc)
        self._prx_filter_bar._qt_widget.user_choose_changed.connect(self._qt_view._execute_view_keyword_filter_occurrence_to_current_)
        self._prx_filter_bar._qt_widget.occurrence_previous_press_clicked.connect(self._qt_view._execute_view_keyword_filter_occurrence_to_previous_)
        self._prx_filter_bar._qt_widget.occurrence_next_press_clicked.connect(self._qt_view._execute_view_keyword_filter_occurrence_to_next_)
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def __keyword_filter_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            # cache fist
            if self._filter_completion_cache is None:
                self._filter_completion_cache = list(
                    set(
                        map(
                            lambda x: x.lower(),
                            [
                                j for i in self._qt_view._get_all_items_() for j in i._get_keyword_filter_keys_auto_as_split_()
                            ]
                        )
                    )
                )

            #
            _ = fnmatch.filter(
                self._filter_completion_cache, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.set_sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __keyword_filter_cbk(self):
        self._qt_view._set_view_keyword_filter_data_src_(
            self._prx_filter_bar.get_keywords()
        )
        self._qt_view._refresh_view_items_visible_by_any_filter_()
        self._qt_view._refresh_viewport_showable_auto_()

    def get_check_tool_box(self):
        return self._prx_check_tool_box

    def get_scale_switch_tool_box(self):
        return self._prx_scale_switch_tool_box

    def get_sort_switch_tool_box(self):
        return self._prx_sort_switch_tool_box

    def get_filter_tool_box(self):
        return self._prx_filter_tool_box

    def __add_scale_switch_tools(self):
        self._scale_switch_tools = []
        for i_key, i_scale in [
            ('small', .5), ('medium', 0.75), ('large', 1.0), ('super', 1.25)
        ]:
            i_tool = _utl_gui_prx_wdt_utility.PrxEnableItem()
            self._prx_scale_switch_tool_box.add_widget(i_tool)
            i_tool._qt_widget._set_size_(24, 24)
            i_tool._qt_widget._set_icon_frame_draw_size_(24, 24)
            i_tool._qt_widget._set_icon_file_draw_size_(20, 20)
            i_tool._qt_widget._set_exclusive_widgets_(self._scale_switch_tools)
            i_tool.set_name(i_key)
            i_tool.set_icon_name('tool/icon-{}'.format(i_key))
            i_tool.set_tool_tip('"LMB click" for switch to scale to "{}"'.format(i_key))
            self._scale_switch_tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self.__switch_view_scale, i_scale)
            )
        #
        self._scale_switch_tools[-2]._set_checked_(True)

    def __switch_view_scale(self, scale):
        self._qt_view._set_item_scale_percent_(scale)

    def __add_sort_mode_switch_tools(self):
        self._sort_mode_switch_tools = []
        for i_key, i_mode in [
            ('number', 0), ('name', 1)
        ]:
            i_tool = _utl_gui_prx_wdt_utility.PrxEnableItem()
            self._prx_sort_switch_tool_box.add_widget(i_tool)
            i_tool._qt_widget._set_size_(24, 24)
            i_tool._qt_widget._set_icon_frame_draw_size_(24, 24)
            i_tool._qt_widget._set_icon_file_draw_size_(20, 20)
            i_tool._qt_widget._set_exclusive_widgets_(self._sort_mode_switch_tools)
            i_tool.set_name(i_key)
            i_tool.set_icon_name('tool/sort-by-{}-ascend'.format(i_key))
            i_tool.set_tool_tip('"LMB click" for switch to sort mode to "{}"'.format(i_key))
            self._sort_mode_switch_tools.append(i_tool._qt_widget)
            #
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self.__switch_view_sort_mode, i_mode)
            )
            i_tool.connect_check_swapped_as_exclusive_to(
                self.__swap_view_sort_order
            )
        #
        self._sort_mode_switch_tools[0]._set_checked_(True)

    def __switch_view_sort_mode(self, mode):
        self._qt_view._set_item_sort_mode_(mode)

    def __swap_view_sort_order(self):
        self._qt_view._swap_item_sort_order_()
        order = ['ascend', 'descend'][self._qt_view._get_sort_order_()]
        for i in self._sort_mode_switch_tools:
            i_key = i._get_name_text_()
            i_icon_name = 'tool/sort-by-{}-{}'.format(i_key, order)
            i._set_icon_file_path_(
                utl_gui_core.RscIconFile.get(i_icon_name),
            )

    def __swap_view_mode(self):
        self._qt_view._swap_view_mode_()
        self._view_mode_swap_button._set_icon_file_path_(
            utl_gui_core.RscIconFile.get(['list_mode', 'grid_mode'][self.view._get_is_grid_mode_()])
        )

    def __check_all_items(self):
        self._qt_view._set_all_item_widgets_checked_(True)

    def __uncheck_all_items(self):
        self._qt_view._set_all_item_widgets_checked_(False)

    def set_view_list_mode(self):
        self._qt_view._set_list_mode_()

    def set_view_grid_mode(self):
        self._qt_view._set_grid_mode_()
    #
    def set_item_frame_size(self, w, h):
        self._qt_view._set_item_frame_size_(w, h)

    def set_item_frame_size_basic(self, w, h):
        self._qt_view._set_item_size_basic_(w, h)

    def set_item_frame_draw_enable(self, boolean):
        self._qt_view._set_item_frame_draw_enable_(boolean)

    def set_item_icon_frame_size(self, w, h):
        self._qt_view._set_item_icon_frame_size_(w, h)
        self._qt_view._set_item_icon_size_(w-4, h-4)

    def set_item_icon_size(self, w, h):
        self._qt_view._set_item_icon_size_(w, h)

    def set_item_icon_frame_draw_enable(self, boolean):
        self._qt_view._set_item_icon_frame_draw_enable_(boolean)

    def set_item_name_frame_size(self, w, h):
        self._qt_view._set_item_name_frame_size_(w, h)
        self._qt_view._set_item_name_size_(w-4, h-4)

    def set_item_name_size(self, w, h):
        self._qt_view._set_item_name_size_(w, h)

    def set_item_name_frame_draw_enable(self, boolean):
        self._qt_view._set_item_name_frame_draw_enable_(boolean)

    def set_item_names_draw_range(self, range_):
        self._qt_view._set_item_names_draw_range_(range_)

    def set_item_image_frame_draw_enable(self, boolean):
        self.view._set_item_image_frame_draw_enable_(boolean)
    #
    def set_item_add(self, *args, **kwargs):
        prx_item_widget = _utl_gui_prx_wgt_item.PrxListItem()
        prx_item_widget.set_view(self)
        self.view._add_item_widget_(prx_item_widget.widget, **kwargs)
        return prx_item_widget

    def set_visible_tgt_raw_clear(self):
        self.set_visible_tgt_raw({})

    def set_visible_tgt_raw_update(self):
        dic = {}
        prx_items = self.get_all_items()
        for item_prx in prx_items:
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
        self._item_dict.clear()
        self._filter_completion_cache = None
        self.view._set_clear_()

    def _get_all_items_(self):
        return self.view._get_all_items_()

    def get_all_items(self):
        return [i._get_item_widget_().gui_proxy for i in self.view._get_all_items_()]

    def set_loading_update(self):
        self.view._set_loading_update_()

    def connect_refresh_action_to(self, fnc):
        self._qt_view.f5_key_pressed.connect(fnc)

    def get_checked_items(self):
        return [i.gui_proxy for i in self._qt_view._get_checked_item_widgets_()]

    def restore_all(self):
        self.set_clear()

    def set_draw_enable(self, boolean):
        self._qt_view._set_drag_enable_(boolean)

    def gui_waiting(self):
        return self._qt_view._gui_waiting_()

    def get_top_tool_bar(self):
        return self._prx_top_tool_bar

    def refresh_viewport_showable_auto(self):
        self._qt_view._refresh_viewport_showable_auto_()

    def set_completion_gain_fnc(self, fnc):
        self._prx_filter_bar.set_completion_gain_fnc(fnc)

    def set_filter_entry_tip(self, text):
        self._prx_filter_bar.set_tip(text)


class PrxImageView(PrxListView):
    def __init__(self, *args, **kwargs):
        super(PrxImageView, self).__init__(*args, **kwargs)
        self.set_item_frame_size(225, 256)
        self.set_item_icon_frame_draw_enable(True)
        self.set_item_name_frame_draw_enable(True)
        self.set_item_image_frame_draw_enable(True)

    def set_textures(self, textures):
        for i_texture in textures:
            for j_texture_unit in i_texture.get_exists_files_():
                self._set_texture_show_(self.set_item_add(), j_texture_unit)

    def _set_texture_show_(self, prx_item, texture_unit):
        def cache_fnc_():
            return [
                prx_item, texture_unit
            ]

        def build_fnc_(data):
            self._set_texture_show_deferred_(data)

        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )

    def _set_texture_show_deferred_(self, data):
        prx_item, texture_unit = data

        info = texture_unit.get_info()
        show_info_dict = collections.OrderedDict(
            [
                ('name', texture_unit.name),
                ('size', '{width} x {height}'.format(**info)),
            ]
        )
        image_file_path, image_sub_process_cmds = bsc_core.ImgFileOpt(texture_unit.path).get_thumbnail_create_args()
        prx_item.set_image(image_file_path)
        prx_item.set_image_show_args(image_file_path, image_sub_process_cmds)
        prx_item.set_name_dict(show_info_dict)
        prx_item.set_tool_tip(
            ['{}={}'.format(k, v) for k, v in info.items()]
        )

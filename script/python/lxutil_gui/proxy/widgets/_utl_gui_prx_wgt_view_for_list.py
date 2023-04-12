# coding:utf-8
import collections

from lxbasic import bsc_core

from lxutil_gui import utl_gui_core

from lxutil_gui.qt.widgets import _utl_gui_qt_wgt_utility, _utl_gui_qt_wgt_chart, _utl_gui_qt_wgt_view_for_list

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
    QT_WIDGET_CLASS = _utl_gui_qt_wgt_utility.QtEntryFrame
    QT_VIEW_CLASS = _utl_gui_qt_wgt_view_for_list.QtListWidget
    def __init__(self, *args, **kwargs):
        super(PrxListView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _utl_gui_qt_wgt_utility.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._prx_h_tool_bar = _utl_gui_prx_wdt_utility.PrxHToolBar()
        self._qt_layout_0.addWidget(self._prx_h_tool_bar.widget)
        self._prx_h_tool_bar.set_border_radius(1)
        #
        self._view_mode_swap_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._prx_h_tool_bar.set_widget_add(self._view_mode_swap_button)
        self._view_mode_swap_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('grid_mode'))
        self._view_mode_swap_button.clicked.connect(self.__swap_view_mode)
        self._view_mode_swap_button._set_tool_tip_text_(
            '"LMB click" for switch view mode'
        )
        #
        self._check_all_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._check_all_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_checked'))
        self._prx_h_tool_bar.set_widget_add(self._check_all_button)
        self._check_all_button.clicked.connect(self.__check_all_items)
        self._check_all_button._set_tool_tip_text_(
            '"LMB click" for checked all items'
        )
        #
        self._uncheck_all_button = _utl_gui_qt_wgt_utility.QtIconPressItem()
        self._uncheck_all_button._set_icon_file_path_(utl_gui_core.RscIconFile.get('all_unchecked'))
        self._prx_h_tool_bar.set_widget_add(self._uncheck_all_button)
        self._uncheck_all_button.clicked.connect(self.__uncheck_all_items)
        self._uncheck_all_button._set_tool_tip_text_(
            '"LMB click" for unchecked all items'
        )
        #
        self._prx_filer_bar_0 = _utl_gui_prx_wdt_utility.PrxFilterBar()
        self._prx_h_tool_bar.set_widget_add(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLASS()
        self._qt_layout_0.addWidget(self._qt_view)
        self._set_prx_view_def_init_(self._qt_view)
        #
        self._qt_info_chart = _utl_gui_qt_wgt_chart.QtInfoChart()
        self._qt_info_chart.hide()
        self._qt_layout_0.addWidget(self._qt_info_chart)
        self._qt_view.info_changed.connect(
            self._qt_info_chart._set_info_text_
        )
        #
        self._prx_filter_bar = self._prx_filer_bar_0

        self._item_dict = collections.OrderedDict()
    @property
    def view(self):
        return self._qt_view
    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def __swap_view_mode(self):
        self._qt_view._set_view_mode_swap_()
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
        self.view._set_item_widget_add_(prx_item_widget.widget, **kwargs)
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

    def set_restore(self):
        self.set_clear()

    def set_filter_bar_visible(self, boolean):
        self._prx_filter_bar.set_visible(boolean)

    def set_draw_enable(self, boolean):
        self._qt_view._set_drag_enable_(boolean)


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

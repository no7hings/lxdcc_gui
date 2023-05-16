# coding:utf-8
import collections

from lxbasic import bsc_core

from lxutil_gui.qt import utl_gui_qt_core

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_utility, _utl_gui_prx_wgt_view_for_list


class TestWindow(_utl_gui_prx_wdt_utility.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        def add_fnc_(i_):
            def show_fnc_():
                thumbnail_file_path = bsc_core.ImgFileOpt(
                    '/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/09-ADVANCED/Del_Cracks_11_1_1_1.jpg'
                ).get_thumbnail()
                # wdt.set_loading_update()
                item_prx.set_image(thumbnail_file_path)
                if i_ % 2 == 0:
                    item_prx.set_icons_by_pixmap(
                        [
                            utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            utl_gui_qt_core.QtPixmapMtd.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            )
                        ]
                    )
                # item_prx.set_image_loading_start()

            item_prx = wdt.set_item_add()
            item_prx.set_show_method(show_fnc_)
            item_prx.set_check_enable(True)
            item_prx.set_drag_enable(True)
            item_prx.set_name_dict(
                collections.OrderedDict(
                    [
                        ('type', 'test'),
                        ('name', 'test'),
                        ('tag', 'test'),
                    ]
                )
            )
            item_prx.set_drag_data(
                {
                    # 'nodegraph/nodes': 'stained_concrete_wall_vdxicg2',
                    # 'nodegraph/noderefs': 'rootNode',
                    # 'python/text': 'NodegraphAPI.GetNode(\'worn_painted_wall_vjyifef\')',
                    # 'python/GetGeometryProducer': 'Nodes3DAPI.GetGeometryProducer(NodegraphAPI.GetNode(\'worn_painted_wall_vjyifef\'))',
                    'nodegraph/fileref': '/l/resource/td/asset/scene/empty.katana',
                    # 'application/x-maya-data': ''
                }
            )
            item_prx.connect_drag_pressed_to(
                self._drag_pressed_fnc_
            )
            item_prx.connect_drag_released_to(
                self._drag_released_fnc_
            )
        #
        wdt = _utl_gui_prx_wgt_view_for_list.PrxListView()
        wdt.get_top_tool_bar().set_expanded(True)
        # wdt.set_draw_enable(True)
        wdt.set_item_icon_frame_draw_enable(True)
        wdt.set_item_image_frame_draw_enable(True)
        wdt.set_item_name_frame_draw_enable(True)
        wdt.get_check_tool_box().set_visible(True)
        wdt.set_item_names_draw_range([None, 1])
        wdt.get_scale_switch_tool_box().set_visible(True)
        wdt.set_item_frame_size_basic(96, 72)
        wdt.set_item_icon_frame_size(20, 20)
        wdt.set_item_icon_size(20, 20)
        wdt.set_clear()
        self.set_widget_add(wdt)
        for i in range(10):
            add_fnc_(i)

    def _drag_pressed_fnc_(self, *args, **kwargs):
        print args[0]
        print 'failed'

    def _drag_released_fnc_(self, *args, **kwargs):
        flag, mime_data = args[0]
        print mime_data.data('nodegraph/noderefs').data()
        print 'completed'


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_definition_window_size((960, 480))
    w.set_window_show()
    w._test_()
    #
    sys.exit(app.exec_())

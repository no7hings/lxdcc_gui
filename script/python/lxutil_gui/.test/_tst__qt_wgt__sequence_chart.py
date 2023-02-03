# coding:utf-8
import collections

import functools

from lxbasic import bsc_configure, bsc_core

from lxutil import utl_core

import lxutil_gui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self._name_width = 240
        #
        self._configure_group = prx_widgets.PrxExpandedGroup()
        self.set_widget_add(self._configure_group)
        self._configure_group.set_expanded(True)
        self._configure_node = prx_widgets.PrxNode()
        self._configure_group.set_widget_add(self._configure_node)
        self._configure_node.set_name_width(self._name_width)
        self._directory_port = self._configure_node.set_port_add(
            prx_widgets.PrxDirectoryOpenPort(
                'directory', 'directory'
            )
        )
        self._name_pattern_port = self._configure_node.set_port_add(
            prx_widgets.PrxPortForString(
                'name-pattern', 'name-pattern'
            )
        )
        self._name_pattern_port.set('*.%04d.*exr')
        self._frame_range_port = self._configure_node.set_port_add(
            prx_widgets.PrxPortForIntegerTuple(
                'frame_range', 'frame-range'
            )
        )
        #
        self._frame_range_port.set_value_size(2)
        self._frame_range_port.set([1001, 1100])
        self._directory_port.set(
            '/data/f/sequence_chart_test'
        )
        #
        self._sequence_group = prx_widgets.PrxExpandedGroup()
        self._sequence_group.set_name('Sequence(s)')
        self._sequence_group.set_layout_alignment_to_top()
        self._sequence_group.set_expanded(True)
        self._sequence_group.set_size_mode(1)
        self._sequence_scroll_area = prx_widgets.PrxScrollArea()
        self.set_widget_add(self._sequence_group)
        self._sequence_group.set_widget_add(
            self._sequence_scroll_area
        )
        #
        self._check_button = prx_widgets.PrxPressItem()
        self._check_button.set_name('Check')
        self._check_button.set_press_clicked_connect_to(
            self._set_check_run_
        )
        self.set_button_add(self._check_button)
        #
        # self._directory_port.set_changed_connect_to(
        #     self._set_check_run_
        # )
    @classmethod
    def _get_check_dict_(cls, directory_path, name_pattern):
        array_dict = collections.OrderedDict()
        file_dict = collections.OrderedDict()
        _ = bsc_core.StgDirectoryMtd.get_all_file_paths__(directory_path)
        if _:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(_)
            )
            for i_file_path in _:
                g_p.set_update()
                i_opt = bsc_core.StgFileOpt(i_file_path)
                i_match_args = bsc_core.StgFileMultiplyMtd.get_match_args(
                    i_opt.name, name_pattern
                )
                if i_match_args:
                    i_pattern, i_numbers = i_match_args
                    if len(i_numbers) == 1:
                        i_relative_path_dir_path = bsc_core.StgDirectoryMtd.get_file_relative_path(
                            directory_path, i_opt.directory_path
                        )
                        i_key = '{}/{}'.format(
                            i_relative_path_dir_path, i_pattern
                        )
                        array_dict.setdefault(
                            i_key, []
                        ).append(i_numbers[0])
                        file_dict.setdefault(
                            i_key, []
                        ).append(i_file_path)
            #
            g_p.set_stop()
        return file_dict, array_dict

    def _get_data_build_(self, *args, **kwargs):
        directory_path = self._directory_port.get()
        name_pattern = self._name_pattern_port.get()
        #
        self._file_dict, self._array_dict = {}, {}
        if directory_path:
            self._file_dict, self._array_dict = self._get_check_dict_(
                directory_path,
                name_pattern=name_pattern
            )

    def _set_gui_build_(self, frame_range):
        def show_in_explorer_fnc_(file_path_):
            bsc_core.StgFileOpt(file_path_).set_open_in_system()

        def set_frame_range_fnc_(frame_range_):
            self._frame_range_port.set(frame_range_)
            self._set_gui_update_(frame_range_)
        #
        self._sequence_scroll_area.set_clear()
        #
        self._sequence_chart_dict = {}
        #
        self._check_button.set_status(bsc_configure.Status.Stopped)
        self._check_button.set_statuses([])
        #
        status = bsc_configure.Status.Completed
        element_statuses = []
        if self._array_dict:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(self._array_dict)
            )
            start_frame, end_frame = frame_range
            for k, i_frame_array in self._array_dict.items():
                g_p.set_update()
                if i_frame_array:
                    i_chart_data = (i_frame_array, frame_range, k)
                    i_s_c = prx_widgets.PrxSequenceChart()
                    i_s_c.set_name_width(self._name_width)
                    i_s_c.set_height(20)
                    #
                    self._sequence_scroll_area.set_widget_add(
                        i_s_c
                    )
                    i_s_c.set_chart_data(
                        i_chart_data
                    )
                    #
                    i_file_path = self._file_dict[k][0]
                    i_start_frame, i_end_frame = i_s_c.get_index_range()
                    i_s_c.set_menu_raw(
                        [
                            ('Show', ),
                            (
                                'Show in Explorer',
                                None,
                                functools.partial(show_in_explorer_fnc_, i_file_path)
                            ),
                            (
                                'Show in RV',
                                None,
                                functools.partial(utl_core.RvLauncher().set_file_open, i_file_path)
                            ),
                            ('Extend',),
                            (
                                'Use Start-frame',
                                None,
                                functools.partial(set_frame_range_fnc_, (i_start_frame, end_frame)),
                            ),
                            (
                                'Use End-frame',
                                None,
                                functools.partial(set_frame_range_fnc_, (i_start_frame, end_frame))
                            )
                        ]
                    )
                    #
                    i_status = i_s_c.get_status()
                    if i_status is bsc_configure.Status.Error:
                        status = i_status
                    #
                    element_statuses.append(i_status)
                    #
                    self._sequence_chart_dict[k] = i_s_c
                #
                g_p.set_stop()
        #
        if element_statuses:
            self._check_button.set_status(
                status
            )
            self._check_button.set_statuses(
                element_statuses
            )

    def _set_gui_update_(self, frame_range):
        if self._array_dict:
            pass

    def _set_check_run_(self):
        frame_range = self._frame_range_port.get()
        #
        method_args = [
            (self._get_data_build_, ()),
            (self._set_gui_build_, (frame_range, ))
        ]
        if method_args:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(method_args)
            )
            for method, args in method_args:
                g_p.set_update()
                method(*args)
            #
            g_p.set_stop()

    def test(self):
        pass


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((960, 640))
    w.set_window_show()
    #
    sys.exit(app.exec_())

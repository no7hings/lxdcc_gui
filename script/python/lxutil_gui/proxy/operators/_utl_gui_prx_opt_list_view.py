# coding:utf-8


class PrxRsvTaskListViewAddOpt(object):
    def __init__(self, prx_list_view, namespace):
        self._prx_list_view = prx_list_view

        self._namespace = namespace

        self._prx_list_view.set_view_list_mode()

    def restore_all(self):
        self._prx_list_view.set_clear()

    def set_add(self, rsv_task):
        def cache_fnc_():
            return [prx_item, rsv_task]

        def build_fnc_(data_):
            self._set_show_deferred_(data_)

        prx_item = self._prx_list_view.set_item_add()
        prx_item.set_gui_dcc_obj(
            rsv_task, namespace=self._namespace
        )
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return True, prx_item

    def _set_show_deferred_(self, data):
        prx_item, rsv_task = data
        print prx_item, rsv_task

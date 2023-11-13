# coding:utf-8
import lxtool.graph.gui.abstracts as grh_gui_abstracts


class PnlRezGraph(grh_gui_abstracts.AbsRezGraph):
    OPTION_HOOK_KEY = 'tool-panels/rez-graph'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(PnlRezGraph, self).__init__(hook_option, *args, **kwargs)

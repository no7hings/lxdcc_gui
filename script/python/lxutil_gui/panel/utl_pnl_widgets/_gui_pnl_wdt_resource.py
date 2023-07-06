# coding:utf-8
import lxutil_gui.panel.abstracts as gui_pnl_abstracts


class PnlResourceLibrary(gui_pnl_abstracts.AbsPnlAbsResourceLibrary):
    def __init__(self, session, *args, **kwargs):
        super(PnlResourceLibrary, self).__init__(session, *args, **kwargs)

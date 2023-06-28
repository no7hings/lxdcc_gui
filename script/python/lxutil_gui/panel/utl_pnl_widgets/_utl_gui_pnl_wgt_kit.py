# coding:utf-8
import lxutil_gui.panel.abstracts as utl_gui_pnl_abstracts


class PnlAppKit(utl_gui_pnl_abstracts.AbsPnlAppKit):
    def __init__(self, session, *args, **kwargs):
        super(PnlAppKit, self).__init__(session, *args, **kwargs)


class PnlToolKit(utl_gui_pnl_abstracts.AbsPnlToolKit):
    def __init__(self, session, *args, **kwargs):
        super(PnlToolKit, self).__init__(session, *args, **kwargs)

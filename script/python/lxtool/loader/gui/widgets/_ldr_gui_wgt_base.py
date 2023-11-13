# coding:utf-8
import lxtool.loader.gui.abstracts as ldr_gui_abstracts


class PnlRsvUnitLoader(ldr_gui_abstracts.AbsPnlRsvUnitLoader):
    def __init__(self, session, *args, **kwargs):
        super(PnlRsvUnitLoader, self).__init__(session, *args, **kwargs)

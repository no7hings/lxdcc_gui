# coding:utf-8
import lxtool.library.gui.abstracts as lib_gui_abstracts


class PnlResourceLibrary(lib_gui_abstracts.AbsPnlResourceLibrary):
    def __init__(self, session, *args, **kwargs):
        super(PnlResourceLibrary, self).__init__(session, *args, **kwargs)

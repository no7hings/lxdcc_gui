# coding:utf-8
import lxtool.library.gui.abstracts as lib_gui_abstracts


class PnlLibraryForResource(lib_gui_abstracts.AbsPnlLibraryForResource):
    def __init__(self, session, *args, **kwargs):
        super(PnlLibraryForResource, self).__init__(session, *args, **kwargs)

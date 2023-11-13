# coding:utf-8

import lxtool.launcher.gui.abstracts as lnc_gui_abstracts


class PnlDccLauncher(lnc_gui_abstracts.AbsPnlDccLauncher):
    def __init__(self, session, *args, **kwargs):
        super(PnlDccLauncher, self).__init__(session, *args, **kwargs)

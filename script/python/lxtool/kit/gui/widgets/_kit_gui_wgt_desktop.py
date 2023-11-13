# coding:utf-8
import lxtool.kit.gui.abstracts as kit_gui_abstracts


class DesktopToolKit(kit_gui_abstracts.AbsToolKitForDesktop):
    def __init__(self, session, *args, **kwargs):
        super(DesktopToolKit, self).__init__(session, *args, **kwargs)

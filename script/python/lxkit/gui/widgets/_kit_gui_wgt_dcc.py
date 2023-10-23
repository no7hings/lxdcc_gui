import lxkit.gui.abstracts as kit_gui_abstracts


class DccToolKit(kit_gui_abstracts.AbsToolKitForDcc):
    def __init__(self, session, *args, **kwargs):
        super(DccToolKit, self).__init__(session, *args, **kwargs)

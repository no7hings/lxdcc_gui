# coding:utf-8
import lxtool.loader.gui.abstracts as ldr_gui_abstracts


class PnlLoaderForRsvTask(ldr_gui_abstracts.AbsPnlLoaderForRsvTask):
    def __init__(self, session, *args, **kwargs):
        super(PnlLoaderForRsvTask, self).__init__(session, *args, **kwargs)

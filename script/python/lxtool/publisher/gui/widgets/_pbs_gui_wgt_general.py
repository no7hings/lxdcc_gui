# coding:utf-8
import lxtool.publisher.gui.abstracts as pbs_gui_abstracts


class PnlGeneralPublish(pbs_gui_abstracts.AbsPnlPublisherForGeneral):
    def __init__(self, session, *args, **kwargs):
        super(PnlGeneralPublish, self).__init__(session, *args, **kwargs)

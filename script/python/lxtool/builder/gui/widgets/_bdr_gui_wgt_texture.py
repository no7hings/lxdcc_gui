# coding:utf-8
import lxtool.builder.gui.abstracts as bdr_gui_abstracts


class PnlBuilderForTexture(bdr_gui_abstracts.AbsPnlBuilderForTexture):
    def __init__(self, session, *args, **kwargs):
        super(PnlBuilderForTexture, self).__init__(session, *args, **kwargs)

import json
import sys
from emoji import UNICODE_EMOJI
from config import ASSETS_PATH
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, \
                            QGraphicsItem, QGraphicsPixmapItem, QDockWidget, QPushButton
from PySide2.QtCore import QPointF, Signal


EMOJI_PNG_PATH = ASSETS_PATH.joinpath("emojis-24.png").resolve()
EMOJI_JSON_PATH = ASSETS_PATH.joinpath("emojis-png-locations-24.json").resolve()


class EmojiItem(QGraphicsPixmapItem):

    def __init__(self,*args, **kwargs):
        super(EmojiItem, self).__init__(*args, **kwargs)
        self.unicode = ''
        self.name ='no name'

    def set_unicode(self, emoji_unicode):
        self.unicode = emoji_unicode

    def set_name(self, emoji_name):
        self.name = emoji_name
        

class EmojiScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(EmojiScene, self).__init__(*args, **kwargs)

    def resizeEvent(self, event):
        print("current Scene size",event.size())
        super(EmojiScene, self).resizeEvent(event)

class EmojiView(QGraphicsView):
    mouse_released = Signal(str)

    def __init__(self, *args, **kwargs):
        super(EmojiView, self).__init__(*args, **kwargs)
        self._init_view()

    def mouseReleaseEvent(self, event):
        items = self.items(event.pos())
        if items:
            self.mouse_released.emit(items[0].unicode)
        super(EmojiView, self).mouseReleaseEvent(event)

    def _init_view(self):
        self._change_view(width=384)

    def _change_view(self, width=None):
        icon_size = 24
        space = 4

        columns = width//(icon_size+space)

        try:
            self.scene().clear()
            self.viewport().update()
        except Exception as e:
            scene = EmojiScene()
            self.setScene(scene)
        emoImage = QImage(str(EMOJI_PNG_PATH))
        emoPixmap = QPixmap.fromImage(emoImage)
        


        with open(str(EMOJI_JSON_PATH),'r',encoding='utf-8',errors='ignore') as json_file:
            db = json.load(json_file)
            y_view=0
            x_view=0
            emokeys = list(db.keys())
            col = 0
            for idx, emokey in enumerate(emokeys):
                emokey_refined = None
                try:
                    emoji_str = UNICODE_EMOJI['en'][emokey][:-1 ].replace("_"," ")
                except Exception as e:
                    emokey_refined = emokey.replace('\ufe0f','')
                    emoji_str = "no name"

                if emokey_refined :
                    try:
                        emoji_str = UNICODE_EMOJI['en'][emokey_refined][:-1 ].replace("_"," ")
                    except Exception as e:
                        print("Error emoji refined name :", e)

                x,y = list(db.values())[idx]

                emoticon = QPixmap(emoPixmap.copy(x, y, 24,24));
                item = EmojiItem(emoticon)
                item.set_unicode(emokey)
                item.set_name(emoji_str)

                x_view= icon_size*(idx % columns)
                if col >=1:
                    x_view=(col*space)+ (col*icon_size)
                item.setPos(x_view,y_view)
                item.setFlag(item.ItemIsSelectable)
                self.scene().addItem(item)
                col+=1
                if col == columns:
                    col = 0
                    y_view+=(1*(icon_size+space))

    def resizeEvent(self, event):
        size = event.size()
        self._change_view(size.width())
        super(EmojiView, self).resizeEvent(event)
        
class EmojiWidget(QDockWidget):
    """docstring for EmojiWidget"""
    def __init__(self, *args):
        super(EmojiWidget, self).__init__(*args)

    def resizeEvent(self, event):
        super(EmojiWidget, self).resizeEvent(event)


        
        


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     scene = EmojiScene()
#     # db = json.load("/home/farispriadi/opensource/github/WALeadApp/WALeadApp/assets/emojis-png-locations-24.json")
#     emoImage = QImage("/home/farispriadi/opensource/github/WALeadApp/WALeadApp/assets/emojis-24.png")
#     emoPixmap = QPixmap.fromImage(emoImage)
#     view = EmojiView(scene)

#     with open("/home/farispriadi/opensource/github/WALeadApp/WALeadApp/assets/emojis-png-locations-24.json") as json_file:
#         db = json.load(json_file)
#         for i in range(5):
#             emokey = list(db.keys())[i]
#             x,y = list(db.values())[i]

#             emoticon = QPixmap(emoPixmap.copy(x, y, 24,24));
#             item = EmojiItem(emoticon)
#             item.set_emoji_unicode(emokey)

#             item.setPos(x,y)
#             item.setFlag(item.ItemIsSelectable)
#             view.scene().addItem(item)
    
#     view.show()
#     sys.exit(app.exec_())


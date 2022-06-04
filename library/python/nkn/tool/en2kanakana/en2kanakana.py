import sys
import alkana
import string
import wanakana

from functools import partial

from PySide2.QtCore import (
    Qt,
    QRegExp,
)
from PySide2.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat, QFont,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTextEdit,
)

from nkn.core import (
    config,
    pipe as p,
)
from nkn.gui import (
    appearance,
)
from nkn.tool.en2kanakana.en2kanakana_ui import Ui_MainWindow
from nkn.tool.en2kanakana.jisho_ui import Ui_Form

APP_NAME = '英語2かなカナ'
__version__ = '0.1.1'

JISHO_CSV = config.ROOT_PATH.joinpath('data', 'jisho.csv')


def read_jisho() -> str:
    if JISHO_CSV.is_file():
        return JISHO_CSV.read_text()
    return ''


def jisho2dict() -> dict:
    return p.pipe(
        read_jisho(),
        p.call.split('\n'),
        p.map(p.call.split(',')),
        p.filter(lambda ss: len(ss) > 1),
        p.map(lambda ss: (ss[0].strip(), ','.join(ss[1:]).strip())),
        dict,
    )


def _get_kana(s: str):
    dct = {
        'a': 'ア',
        'i': 'アイ',
    }
    dct.update(jisho2dict())
    try:
        return dct[s.lower()]
    except KeyError:
        return alkana.get_kana(s)


def get_kana(s: str):
    dct = {
        '`s': 'ズ',
        's`': 'ズ',
        's': 'ス',
        '`re': 'ア',
        '`m': 'ム',
        '`ll': 'ル',
        '`ve': 'ブ',
        'n`t': 'ント',
        '`d': 'ド',
        'ing': 'イング',
    }
    r = _get_kana(s)
    for key in dct.keys():
        if r is None and s.endswith(key):
            r = _get_kana(s[:(-1 * len(key))])
            if r is not None:
                r += dct[key]
    return r


def check_str(s: str):
    return s.lower() in list(string.ascii_lowercase) + ['`']


class JishoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle('辞書')

        # event
        self.ui.saveButton.clicked.connect(self.save_jisho)
        self.ui.cancelButton.clicked.connect(self.close)

        #

    def load_jisho(self):
        self.ui.jishoTextEdit.setPlainText(read_jisho())

    def save_jisho(self):
        JISHO_CSV.write_text(self.ui.jishoTextEdit.toPlainText())
        self.close()

    def show(self):
        self.load_jisho()
        super().show()


class Highlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        _format = QTextCharFormat()
        _format.setFontWeight(QFont.Bold)
        _format.setForeground(Qt.red)
        # pattern = QString("\\b[A-Za-z]+\\b")
        expression = QRegExp('[A-Za-z]+')
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, _format)
            index = expression.indexIn(text, index + length)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s  其ノ%s' % (APP_NAME, __version__))
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(600, 700)
        self.setAcceptDrops(True)

        self.jisho_window = JishoWindow(self)
        #

        self.hi = Highlighter(self.ui.kanaTextEdit.document())
        self.hi2 = Highlighter(self.ui.kana2TextEdit.document())

        self.ui.enCopyButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.kanaCopyButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.kana2CopyButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.pasteButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.transButton.setStyleSheet(appearance.in_stylesheet)

        # event

        self.ui.transButton.clicked.connect(self.conv)
        self.ui.jishoButton.clicked.connect(self.jisho_window.show)
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.enCopyButton.clicked.connect(partial(self.copy2clipboard, self.ui.enPlainTextEdit))
        self.ui.pasteButton.clicked.connect(partial(self.paste_from_clipboard, self.ui.enPlainTextEdit))
        self.ui.kanaCopyButton.clicked.connect(partial(self.copy2clipboard, self.ui.kanaTextEdit))
        self.ui.kana2CopyButton.clicked.connect(partial(self.copy2clipboard, self.ui.kana2TextEdit))

    def copy2clipboard(self, w: QTextEdit):
        clipboard = QApplication.clipboard()
        clipboard.setText(w.toPlainText())

    def paste_from_clipboard(self, w: QTextEdit):
        clipboard = QApplication.clipboard()
        w.setPlainText(clipboard.text())

    def conv(self):
        s: str = self.ui.enPlainTextEdit.toPlainText().replace('’', '`')

        # 単語 区切り探し
        split_list = [0]
        for i in range(1, len(s)):
            w1 = check_str(s[i - 1])
            w2 = check_str(s[i])
            if (w1 and not w2) or (not w1 and w2):
                split_list.append(i)
        split_list.append(len(s))

        # 単語分割 カタカナ変換
        lst = []
        for i in range(1, len(split_list)):
            word: str = s[split_list[i - 1]: split_list[i]].strip()
            if len(word) == 0:
                continue
            kana = get_kana(word)
            if kana is None:
                kana = word
            lst.append(kana)

        # カタカナ
        r = ' '.join(lst).replace(' ,', ',')
        for c in ['.', '?', '!']:
            r = r.replace(' ' + c, c).replace(c, c + '\n').replace('\n ', '\n')
        self.ui.kanaTextEdit.setText(r)
        # かなカナ
        lst2 = lst.copy()
        for i, s in enumerate(lst2):
            if i % 2 == 1:
                if wanakana.is_katakana(s):
                    lst2[i] = wanakana.to_hiragana(s)
        r2 = ''.join(lst2)
        for c in ['.', '?', '!']:
            r2 = r2.replace(c, c + '\n')
        self.ui.kana2TextEdit.setText(r2)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

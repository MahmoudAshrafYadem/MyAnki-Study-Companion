import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QFileDialog,
    QStackedWidget, QRadioButton, QButtonGroup,
    QInputDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


# --- PDF EXPORT HELPER ---
def export_to_pdf(parent, title, data, mode="mcq"):
    path, _ = QFileDialog.getSaveFileName(parent, f"Save {title}", "", "PDF Files (*.pdf)")
    if not path: return
    c = canvas.Canvas(path, pagesize=letter)
    y = 10.5 * inch
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, y, f"Study Session: {title}")
    y -= 0.5 * inch
    for i, item in enumerate(data):
        if y < 1.5 * inch:
            c.showPage()
            y = 10.5 * inch
        if mode == "mcq":
            q, opts, corr = item
            c.setFont("Helvetica-Bold", 11)
            c.drawString(1 * inch, y, f"Q{i + 1}: {q[:90]}")
            y -= 0.2 * inch
            c.setFont("Helvetica", 10)
            c.drawString(1.2 * inch, y, f"Correct Answer: {opts[corr] if (corr is not None and corr != -1) else 'N/A'}")
            y -= 0.4 * inch
        else:
            f, b = item
            c.setFont("Helvetica-Bold", 11)
            c.drawString(1 * inch, y, f"Card {i + 1} Front: {f[:90]}")
            y -= 0.2 * inch
            c.setFont("Helvetica", 11)
            c.drawString(1.2 * inch, y, f"Back: {b[:90]}")
            y -= 0.5 * inch
    c.save()
    QMessageBox.information(parent, "Success", "PDF Saved Successfully!")


# --- SHARED STYLES ---
BOOK_STYLE = """
    QPushButton {{
        background-color: {color};
        color: white;
        font-size: 26px;
        font-weight: bold;
        border-left: 18px solid {dark_color};
        border-radius: 12px;
        text-align: left;
        padding-left: 35px;
        margin: 10px;
        min-height: 110px;
    }}
    QPushButton:hover {{
        background-color: {hover_color};
    }}
"""


# --- FLASHCARD PAGE ---
class FlashcardPage(QWidget):
    def __init__(self, cards, go_home):
        super().__init__()
        self.cards, self.current, self.flipped, self.go_home = cards, 0, False, go_home
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        self.card_frame = QFrame()
        self.card_frame.setStyleSheet("background: #fffcf2; border: 4px solid #22c55e; border-radius: 25px;")
        card_inner = QVBoxLayout(self.card_frame)
        self.side_label = QLabel("QUESTION")
        self.side_label.setStyleSheet("color: #16a34a; font-weight: bold; font-size: 22px;")
        self.side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content = QLabel()
        self.content.setWordWrap(True)
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.setStyleSheet("font-size: 34px; color: #1e293b; padding: 20px; font-family: 'Georgia';")
        card_inner.addWidget(self.side_label)
        card_inner.addWidget(self.content, stretch=1)
        layout.addWidget(self.card_frame, stretch=1)
        nav = QHBoxLayout()
        btns = [("Prev", self.prev, "#64748b"), ("Flip Card", self.flip, "#22c55e"),
                ("Next", self.next, "#64748b"),
                ("Save PDF", lambda: export_to_pdf(self, "Flashcards", self.cards, "flash"), "#10b981"),
                ("Home", self.go_home, "#ef4444")]
        for t, f, c in btns:
            b = QPushButton(t);
            b.setFixedHeight(60);
            b.setStyleSheet(f"background:{c}; color:white; border-radius:15px; font-weight:bold; min-width: 100px;")
            b.clicked.connect(f);
            nav.addWidget(b)
        layout.addLayout(nav)
        self.update_card()

    def update_card(self):
        f, b = self.cards[self.current]
        clean_text = re.sub(r'\bCard\s+\d+\b', '', b if self.flipped else f, flags=re.IGNORECASE).strip()
        self.content.setText(clean_text)
        self.side_label.setText("ANSWER" if self.flipped else f"QUESTION {self.current + 1}")
        self.side_label.setStyleSheet(
            f"color: {'#3b82f6' if self.flipped else '#16a34a'}; font-weight: bold; font-size: 22px;")

    def flip(self): self.flipped = not self.flipped; self.update_card()

    def prev(self): self.current = max(0, self.current - 1); self.flipped = False; self.update_card()

    def next(self): self.current = min(len(self.cards) - 1, self.current + 1); self.flipped = False; self.update_card()


# --- MCQ & EXAM PAGE ---
class PracticePage(QWidget):
    def __init__(self, questions, go_home, mode="mcq", duration=None):
        super().__init__()
        self.questions, self.current, self.go_home, self.mode = questions, 0, go_home, mode
        self.user_answers = [-1] * len(questions)
        self.time_left = duration * 60 if duration else None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 40, 80, 40)
        if self.time_left:
            self.timer_lbl = QLabel()
            self.timer_lbl.setStyleSheet(
                "font-size: 28px; color: #ef4444; font-weight: bold; background: #fee2e2; padding: 10px; border-radius: 15px;")
            layout.addWidget(self.timer_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            self.timer = QTimer(self);
            self.timer.timeout.connect(self.tick);
            self.timer.start(1000)
        self.q_label = QLabel()
        self.q_label.setWordWrap(True)
        self.q_label.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #1e40af; background: #fffbeb; padding: 40px; border-radius: 20px; border: 2px solid #fde68a;")
        layout.addWidget(self.q_label)
        self.bg = QButtonGroup(self)
        self.btns = []
        for i in range(4):
            rb = QRadioButton();
            self.btns.append(rb);
            self.bg.addButton(rb, i);
            layout.addWidget(rb)
        layout.addStretch()
        nav = QHBoxLayout()
        btns = [("Prev", self.prev, "#64748b"),
                ("Next", self.next, "#f59e0b" if mode == "mcq" else "#64748b"),
                ("Export PDF", lambda: export_to_pdf(self, "Questions", self.questions), "#10b981"),
                ("Submit" if mode == "exam" else "Home", self.submit if mode == "exam" else self.go_home, "#ef4444")]
        for t, f, c in btns:
            b = QPushButton(t);
            b.setFixedHeight(60);
            b.setStyleSheet(f"background:{c}; color:white; border-radius:15px; font-weight:bold; min-width: 140px;")
            b.clicked.connect(f);
            nav.addWidget(b)
        layout.addLayout(nav)
        self.load()

    def tick(self):
        self.time_left -= 1
        m, s = divmod(self.time_left, 60)
        self.timer_lbl.setText(f"⏳ {m:02d}:{s:02d}")
        if self.time_left <= 0: self.submit()

    def load(self):
        q, opts, corr = self.questions[self.current]
        self.q_label.setText(f"Question {self.current + 1}:\n{q}")
        self.bg.setExclusive(False)
        for i, b in enumerate(self.btns):
            if i < len(opts):
                b.setText(opts[i]);
                b.setVisible(True);
                b.setChecked(self.user_answers[self.current] == i)
                if self.mode == "mcq" and i == corr:
                    b.setStyleSheet(
                        "QRadioButton { font-size: 22px; padding: 20px; background-color: #dcfce7; color: #16a34a; font-weight: bold; border-radius: 12px; }")
                else:
                    b.setStyleSheet("QRadioButton { font-size: 22px; padding: 20px; color: #334155; }")
            else:
                b.setVisible(False)
        self.bg.setExclusive(True)

    def save_state(self):
        if self.bg.checkedId() != -1: self.user_answers[self.current] = self.bg.checkedId()

    def prev(self):
        self.save_state(); self.current = max(0, self.current - 1); self.load()

    def next(self):
        self.save_state(); self.current = min(len(self.questions) - 1, self.current + 1); self.load()

    def submit(self):
        self.save_state()
        score = sum(1 for i, (_, _, c) in enumerate(self.questions) if self.user_answers[i] == c)
        QMessageBox.information(self, "Result", f"Exam Completed!\nYour Score: {score} / {len(self.questions)}")
        self.go_home()


# --- MAIN WINDOW (UPDATED FOR FULLSCREEN) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Companion Pro")

        # 1. Start in Full Screen Mode
        self.showFullScreen()

        self.setStyleSheet("QMainWindow { background-color: #e7d8c9; }")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = QWidget()
        layout = QVBoxLayout(self.home_page)
        layout.setContentsMargins(150, 50, 150, 50)

        title = QLabel("Study Companion Library")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 48px; font-weight: bold; color: #5d4037; font-family: 'Georgia';")
        layout.addWidget(title)

        subtitle = QLabel("Choose a book to begin your session (Press ESC to exit Fullscreen)")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 20px; color: #8d6e63; margin-bottom: 40px;")
        layout.addWidget(subtitle)

        # Book Buttons
        self.btn_flash = QPushButton(" 📖  Flashcards Collection")
        self.btn_flash.setStyleSheet(BOOK_STYLE.format(color="#2e7d32", dark_color="#1b5e20", hover_color="#388e3c"))
        self.btn_mcq = QPushButton(" 📑  Practice MCQs Workbook")
        self.btn_mcq.setStyleSheet(BOOK_STYLE.format(color="#ef6c00", dark_color="#e65100", hover_color="#f57c00"))
        self.btn_exam = QPushButton(" 🎓  Final Exam Simulator")
        self.btn_exam.setStyleSheet(BOOK_STYLE.format(color="#c62828", dark_color="#b71c1c", hover_color="#d32f2f"))

        for b, m in [(self.btn_flash, "flash"), (self.btn_mcq, "mcq"), (self.btn_exam, "exam")]:
            b.clicked.connect(lambda _, mode=m: self.upload(mode))
            layout.addWidget(b)

        credit = QLabel("Made by Mahmoud Yadem")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet("font-size: 18px; color: #5d4037; font-weight: bold; margin-top: 30px;")
        layout.addWidget(credit)
        self.stack.addWidget(self.home_page)

    # 2. Add ESC Key support to toggle out of Full Screen if needed
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def upload(self, mode):
        path, _ = QFileDialog.getOpenFileName(self, "Select Study File", "", "Text Files (*.txt)")
        if not path: return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if mode == "flash":
                cards = self.parse_flash(content)
                self.page = FlashcardPage(cards, self.go_home)
            else:
                qs, _ = self.parse_mcq(content)
                if mode == "mcq":
                    self.page = PracticePage(qs, self.go_home, mode="mcq")
                else:
                    dur, ok = QInputDialog.getInt(self, "Exam", "Minutes:", 30, 5, 180)
                    if not ok: return
                    self.page = PracticePage(qs, self.go_home, mode="exam", duration=dur)
            self.stack.addWidget(self.page)
            self.stack.setCurrentWidget(self.page)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def go_home(self):
        self.stack.setCurrentIndex(0)

    def parse_flash(self, text):
        cards = []
        pattern = re.compile(r"Front:(.*?)Back:(.*?)(?=Front:|$)", re.DOTALL | re.IGNORECASE)
        for m in pattern.finditer(text):
            cards.append((m.group(1).strip(), m.group(2).strip()))
        return cards

    def parse_mcq(self, text):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        ans_map = {}
        for l in lines:
            if (',' in l or ';' in l) and re.match(r'^\d+', l):
                parts = re.split(r'[;,]', l.upper().replace(' ', ''))
                for i in range(0, len(parts), 2):
                    if i + 1 < len(parts): ans_map[int(parts[i])] = ord(parts[i + 1]) - ord('A')
                break
        qs, cq, co = [], None, []
        for l in lines:
            q_m = re.match(r'^(\d+)[\.\s]+(.+)', l)
            o_m = re.match(r'^([A-D])[\.\s]+(.+)', l, re.I)
            if q_m:
                if cq: qs.append((cq, co, ans_map.get(len(qs) + 1, -1)))
                cq, co = q_m.group(2).strip(), []
            elif o_m and cq:
                co.append(o_m.group(2).strip())
        if cq: qs.append((cq, co, ans_map.get(len(qs) + 1, -1)))
        return qs, ans_map


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.show() is handled by win.showFullScreen() in __init__
    sys.exit(app.exec())
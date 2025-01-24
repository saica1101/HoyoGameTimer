from ui_main import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(540, 450)
        self.setWindowTitle("HoyoGame Timer")

        self.timers = {
            "genshin": {"end_time": None, "timer": QTimer(self), "recovery_rate": 8},
            "starrail": {"end_time": None, "timer": QTimer(self), "recovery_rate": 6},
            "zzz": {"end_time": None, "timer": QTimer(self), "recovery_rate": 6},
        }

        self.ui.genshinTimer.setText("00:00:00")
        self.ui.starrailTimer.setText("00:00:00")
        self.ui.zzzTimer.setText("00:00:00")

        self.ui.genshinButton.clicked.connect(lambda: self.start_timer("genshin"))
        self.ui.starrailButton.clicked.connect(lambda: self.start_timer("starrail"))
        self.ui.zzzButton.clicked.connect(lambda: self.start_timer("zzz"))

        for key in self.timers.keys():
            self.timers[key]["timer"].timeout.connect(lambda key = key: self.update_timer(key))

        self.ui.genshin_rpb.setBarStyle("Donet")
        self.ui.genshin_rpb.setRange(0,200)
        self.ui.genshin_rpb.setValue(0)
        self.ui.genshin_rpb.setLineWidth(8)
        self.ui.genshin_rpb.setLineCap("RoundCap")

        self.ui.starrail_rpb.setBarStyle("Donet")
        self.ui.starrail_rpb.setRange(0,300)
        self.ui.starrail_rpb.setValue(0)
        self.ui.starrail_rpb.setLineWidth(8)
        self.ui.starrail_rpb.setLineCap("RoundCap")

        self.ui.zzz_rpb.setBarStyle("Donet")
        self.ui.zzz_rpb.setRange(0,240)
        self.ui.zzz_rpb.setValue(0)
        self.ui.zzz_rpb.setLineWidth(8)
        self.ui.zzz_rpb.setLineCap("RoundCap")

        self.show()

    def start_timer(self, game_key):
        try:
            if game_key == "genshin":
                input_field = self.ui.genshinInput
                label = self.ui.genshinTimer
                chkBox = self.ui.genshinChkBox
                max_stamina = 200
            elif game_key == "starrail":
                input_field = self.ui.starrailInput
                label = self.ui.starrailTimer
                chkBox = self.ui.starrailChkBox
                max_stamina = 300
            elif game_key == "zzz":
                input_field = self.ui.zzzInput
                label = self.ui.zzzTimer
                chkBox = self.ui.zzzChkBox
                max_stamina = 240
            else:
                return
            
            
            # 現在のスタミナを取得
            current_stamina = int(input_field.text())

            # 入力値の検証
            if current_stamina < 0 or current_stamina > max_stamina:
                label.setText("エラー:範囲外の値です。")
                return

            # 回復に必要な時間を計算
            remaining_stamina = max_stamina - current_stamina
            recovery_rate = self.timers[game_key]["recovery_rate"]
            recovery_time_minutes = remaining_stamina * recovery_rate

            # 回復終了時刻を辞書に設定
            recovery_end_time = datetime.now() + timedelta(minutes=recovery_time_minutes)
            self.timers[game_key]["end_time"] = recovery_end_time

            if chkBox.isChecked():
                notify_time = recovery_end_time - timedelta(hours = 1)
                QTimer.singleShot((notify_time - datetime.now()).total_seconds() * 1000, lambda: self.send_notification(game_key))

            # タイマー開始
            self.timers[game_key]["timer"].start(1000)

            # 即時更新（エラーがなかった場合のみ）
            self.update_timer(game_key)

            input_field.setText("")

        except ValueError:
            # 入力値が数値でない場合
            label.setText("エラー:数値を入力してください。")

    def send_notification(self, game_key):
        game_name = {
            "genshin": "原神",
            "starrail": "崩壊：スターレイル",
            "zzz": "ゼンレスゾーンゼロ"
        }.get(game_key, "ゲーム")
        notification.notify(title="スタミナ通知",
                            message=f"{game_name}のスタミナがもうすぐで溜まります。",
                            app_name = "HoyoGame Timer",
                            )
        

    def update_timer(self, game_key):
        current_time = datetime.now()
        end_time = self.timers[game_key]["end_time"]

        if game_key == "genshin":
            label = self.ui.genshinTimer
            rpb = self.ui.genshin_rpb
            max_stamina = 200
        elif game_key == "starrail":
            label = self.ui.starrailTimer
            rpb = self.ui.starrail_rpb
            max_stamina = 300
        elif game_key == "zzz":
            label = self.ui.zzzTimer
            rpb = self.ui.zzz_rpb
            max_stamina = 240
        else:
            return
        
        remaining_time = end_time - current_time

        if remaining_time.total_seconds() <= 0:
            label.setText("回復完了")
            rpb.setValue(max_stamina)
            self.timers[game_key]["timer"].stop()
        else:
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

            recovery_rate = self.timers[game_key]["recovery_rate"]
            elapsed_stamina = max_stamina - int(remaining_time.total_seconds() / (recovery_rate * 60)) - 1
            rpb.setValue(elapsed_stamina)

        rpb.setValue(elapsed_stamina)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
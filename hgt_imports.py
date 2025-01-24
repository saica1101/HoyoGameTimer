import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySideExtn.RoundProgressBar import RoundProgressBar
from plyer import notification
from datetime import datetime, timedelta
os.environ["QT_FONT_DIP"] = "96"
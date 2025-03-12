"""
Progress manager for My ResearchPal.
Used to log and display real-time progress information.
"""

import datetime

class ProgressManager:
    def __init__(self):
        self.updates = []

    def update(self, message):
        """
        Record and print a progress update with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        update_message = f"[{timestamp}] {message}"
        self.updates.append(update_message)
        print(update_message)
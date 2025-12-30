from typing import Callable
from PyQt6.QtCore import QObject, pyqtSignal as Signal, QThread, QRunnable, pyqtSlot
from scripts.networkConfig import list_adapters


class WorkerSignals(QObject):
  finished = Signal(list)


class Worker(QRunnable):
  def __init__(self, *fns: Callable):
    super().__init__()

    self.fns = fns
    self.signals = WorkerSignals()

  @pyqtSlot()
  def run(self):
    results = []

    # TODO: make them run in parallel?
    for fn in self.fns:
      results.append(fn())

    self.signals.finished.emit(results)


class AdapterWorker(QObject):
  finished = Signal(object)

  def run(self):
    adapters = list_adapters()
    self.finished.emit(adapters)


# TODO: remove and go with the thread pool approach as well
class AdapterLoader(QObject):
  finished = Signal(object)

  def __init__(self, parent: QObject | None = None) -> None:
    super().__init__(parent)

    self._busy = False
    self._worker = None
    self._thread = None

  def refresh(self):
    if self._busy:
      print("AdapterLoader is busy, skipping refresh")
      return False

    self._busy = True

    self._thread = QThread()
    self._worker = AdapterWorker()
    self._worker.moveToThread(self._thread)

    self._thread.started.connect(self._worker.run)
    self._worker.finished.connect(self._on_worker_finished)
    self._worker.finished.connect(self._thread.quit)
    self._worker.finished.connect(self._worker.deleteLater)
    self._thread.finished.connect(self._on_thread_finished)
    self._thread.finished.connect(self._thread.deleteLater)

    self._thread.start()

  def _on_worker_finished(self, adapters):
    self.finished.emit(adapters)

  def _on_thread_finished(self):
    self._busy = False
    self._worker = None
    self._thread = None

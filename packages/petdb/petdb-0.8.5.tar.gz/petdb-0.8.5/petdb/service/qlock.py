
import time
from uuid import uuid4
import threading
import collections

class QLock:

	def __init__(self):
		self.id = str(uuid4())
		self.lock = threading.Lock()
		self.waiters = collections.deque()
		self.count = 0
		self.lock_ts = 0

	def acquire(self):
		self.lock.acquire()
		if self.count:
			new_lock = threading.Lock()
			new_lock.acquire()
			self.waiters.append(new_lock)
			self.lock.release()
			new_lock.acquire()
			self.lock.acquire()
		self.count += 1
		self.lock_ts = time.time()
		self.lock.release()

	def release(self):
		with self.lock:
			if not self.count:
				return
			self.count -= 1
			if self.waiters:
				self.waiters.popleft().release()

	def release_all(self):
		i = 0
		while self.locked():
			self.release()
			i += 1
			if i > 100:
				break
		self.waiters.clear()
		self.count = 0

	def locked(self):
		return self.count > 0

	def __enter__(self):
		print(f"lock {self.id}")
		self.acquire()

	def __exit__(self, exc_type, exc_val, exc_tb):
		print(f"unlock {self.id}")
		self.release()

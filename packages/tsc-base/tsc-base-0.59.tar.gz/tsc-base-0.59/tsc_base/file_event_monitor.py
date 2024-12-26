# Description：监控目录变化

import time
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileDeletedEvent,
    FileModifiedEvent,
    FileCreatedEvent,
    FileMovedEvent,
    FileClosedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirCreatedEvent,
    DirMovedEvent,
    EVENT_TYPE_MOVED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
    EVENT_TYPE_CLOSED,
)
from typing import Union, Optional, Callable, AsyncGenerator, Generator
from datetime import datetime
from dataclasses import dataclass, field
import atexit
import asyncio
import os


AllFileSystemEvent = Union[FileDeletedEvent, FileModifiedEvent, FileCreatedEvent, FileMovedEvent, FileClosedEvent, DirDeletedEvent, DirModifiedEvent, DirCreatedEvent, DirMovedEvent]


@dataclass
class FileDirEvent:
    """文件夹或文件的事件"""
    event: AllFileSystemEvent
    date: datetime = field(default_factory=datetime.now)
    timestamp: float = field(default_factory=time.time)
    invalid_src_path: Optional[bool] = None  # 源路径是否无效
    invalid_dest_path: Optional[bool] = None  # 目标路径是否无效，对于移动事件，一方无效意味着可能要变成删除或增加事件


async def async_fetch_pending_event(
    pending_events: list[FileDirEvent],
    delay: Union[float, int] = 1
) -> AsyncGenerator[FileDirEvent, None]:
    """异步获取待处理事件"""
    actual_delay = 0.5  # pending_events 为空时的延迟
    while True:
        try:
            actual_delay = pending_events[0].timestamp - (time.time() - delay)
            assert actual_delay <= 0
            event = pending_events.pop(0)  # 理论上存在极小的概率不满足 delay，因为 pending_events[0] 可能在判定后修改
        except:
            await asyncio.sleep(actual_delay)
            continue
        finally:
            actual_delay = 0.5
        yield event


def fetch_pending_event(
    pending_events: list[FileDirEvent],
    delay: Union[float, int] = 1
) -> Generator[FileDirEvent, None, None]:
    """获取待处理事件"""
    actual_delay = 0.5  # pending_events 为空时的延迟
    while True:
        try:
            actual_delay = pending_events[0].timestamp - (time.time() - delay)
            assert actual_delay <= 0
            event = pending_events.pop(0)
        except:
            time.sleep(actual_delay)
            continue
        finally:
            actual_delay = 0.5
        yield event


class FileDirEventMonitor(FileSystemEventHandler):
    def __init__(
        self,
        monitor_directory: str,
        warp_event_handler: Callable[[AllFileSystemEvent], Optional[FileDirEvent]] = lambda e: FileDirEvent(e),
        pending_events: Optional[list[FileDirEvent]] = None,
    ):
        """监控目录变化，允许延迟处理

        Args:
            monitor_directory (str): 要监控的目录
            warp_event_handler (func, optional): 用来快速决定 FileDirEvent 其他字段怎么设定，以及这个事件是否需要被记，返回 None 则不记录这个事件
            pending_events (Optional[list[FileDirEvent]]): 待处理的事件，供外部程序通过 pop(0) 消费，时间顺序的队列
        """
        self._pending_events = [] if pending_events is None else pending_events
        self._monitor_directory = monitor_directory
        self._warp_event_handler = warp_event_handler
        
        self._observer = Observer()
        self._observer.schedule(self, path=monitor_directory, recursive=True)
        self._observer.start()
        self._running = True
        atexit.register(self.stop)
    
    def _set_event(self, event: FileDirEvent):
        wrap_event = self._warp_event_handler(event)
        if wrap_event is None:
            return
        while True:
            try:
                last_wrap_event = self._pending_events.pop(-1)
            except:
                break
            if not (  # 合并相邻的相同事件
                wrap_event.event.src_path == last_wrap_event.event.src_path and
                wrap_event.event.event_type == last_wrap_event.event.event_type and
                wrap_event.event.is_directory == last_wrap_event.event.is_directory and
                getattr(wrap_event.event, 'dest_path', None) == getattr(last_wrap_event.event, 'dest_path', None)
            ):
                self._pending_events.append(last_wrap_event)
                break
        self._pending_events.append(wrap_event)
        
    def on_modified(self, event: Union[FileModifiedEvent, DirModifiedEvent]):
        self._set_event(event)

    def on_created(self, event: Union[FileCreatedEvent, DirCreatedEvent]):
        self._set_event(event)

    def on_deleted(self, event: Union[FileDeletedEvent, DirDeletedEvent]):
        self._set_event(event)

    def on_moved(self, event: Union[FileMovedEvent, DirMovedEvent]):
        self._set_event(event)
    
    def on_closed(self, event: FileClosedEvent):
        self._set_event(event)
    
    def join(self):
        self._observer.join()
    
    async def async_fetch_pending_event(self, delay: Union[float, int] = 1) -> AsyncGenerator[FileDirEvent, None]:
        """异步获取待处理事件"""
        async for event in async_fetch_pending_event(self._pending_events, delay):
            yield event
    
    def fetch_pending_event(self, delay: Union[float, int] = 1) -> Generator[FileDirEvent, None, None]:
        """获取待处理事件"""
        yield from fetch_pending_event(self._pending_events, delay)
    
    def stop(self):
        """停止监控"""
        if self._running:
            self._running = False
            self._observer.stop()


def jsonl_warp_event_handler(event: AllFileSystemEvent) -> Optional[FileDirEvent]:
    """例子：只记录文件夹的删除、josnl 文件的增删改移"""
    wrap_event = FileDirEvent(event)
    if (
        event.event_type == EVENT_TYPE_CLOSED or
        event.is_directory and event.event_type != EVENT_TYPE_DELETED or
        not event.is_directory and 
        not (event.src_path.endswith('.jsonl') or getattr(event, 'dest_path', '').endswith('.jsonl'))
    ):
        return
    # 其他判定
    ...
    return wrap_event


async def test():
    # 设置要监控的目录
    monitor_directory = os.path.dirname(os.getcwd())
    delay = 1
    print(f"监控目录：{monitor_directory}, 延迟：{delay} 秒")

    handler = FileDirEventMonitor(monitor_directory)
    async for event in handler.async_fetch_pending_event(delay):
        print(event.event)


if __name__ == "__main__":
    asyncio.run(test())

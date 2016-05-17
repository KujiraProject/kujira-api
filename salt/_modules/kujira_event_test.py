"""Salt module that fires events for debug purposes
"""
import time


def fire_test_events(event_tag, event_count=10, interval=10):
    """Fire event with specified tag in loop

    :param event_tag: event tag
    :param event_count: number of fired events
    :param interval: interval between events in seconds
    """
    for i in range(0, event_count):
        __salt__['event.fire_master']({'event_number': i}, event_tag)
        time.sleep(interval)

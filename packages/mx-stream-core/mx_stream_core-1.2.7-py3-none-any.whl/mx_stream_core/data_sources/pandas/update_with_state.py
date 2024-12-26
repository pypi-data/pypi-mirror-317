import json
import os

import pandas as pd
from pyspark.sql.streaming.state import GroupState


def update_with_state(key, pdf_iterator, state: GroupState):
    """
    Function to handle the state of the group with `applyInPandasWithState`.
    :param key: Key of the group (e.g., (window, topic))
    :param pdf_iterator: Iterator containing pandas DataFrames.
    :param state: State of the group.
    :return: Resulting pandas DataFrame.
    """
    # Hợp nhất tất cả các DataFrame trong iterator
    events_df = pd.concat(list(pdf_iterator))
    # Trạng thái hiện tại (nếu có)
    if state.exists:
        state_value = state.get
        current_state = {"events": json.loads(state_value[0]), "event_count": state_value[1]}
    else:
        current_state = {"events": [], "event_count": 0}
    # print(f"[Debug] 28 current_state: {current_state}")
    # Tổng hợp các sự kiện mới
    new_events = events_df.to_dict("records")
    # print(f"[Debug] 31 new_events: {new_events}")
    events = [event.get('data') for event in new_events]
    if len(events) > 0:
        """
            Bởi vì đây là 1 hàm callback nên không thể access trực tiếp vào spark context
            Vì vậy không thể share config qua lại giữa worker và driver
            Cách giải quyết là truyền config thông qua dataframe của mỗi batch luôn.
        """
        idle_processing_timeout = new_events[0].get('idle_processing_timeout')
        print(f"[Debug] 34 idle_processing_timeout: {idle_processing_timeout}")
    else:
        # Đoạn này cần có giá trị mặc định cho idle_processing_timeout vì sẽ có những trường hợp không batch bị rỗng
        idle_processing_timeout = os.getenv('DEFAULT_IDLE_PROCESSING_TIMEOUT', 30000)

    current_state["events"].extend(events)
    current_state["event_count"] += len(new_events)
    if state.hasTimedOut:
        batch = pd.DataFrame([{
            "window_start": key[0].get('start'),
            "window_end": key[0].get('end'),
            "topic": key[1],
            "events": json.dumps(current_state["events"]),
            "event_count": str(current_state["event_count"]),
        }])
        batch = [batch]
        state.remove()
    else:
        state.update((current_state["events"], current_state["event_count"]))
        current_processing_time = state.getCurrentProcessingTimeMs()  # Lay thoi gian hien tai cua processing
        window_end_ms = key[0].get('end').timestamp() * 1000  # Lay thoi gian ket thuc cua window
        timeout_at = window_end_ms - current_processing_time  # Tinh thoi gian timeout
        if timeout_at < 0:
            timeout_at = idle_processing_timeout
        else:
            timeout_at = timeout_at + idle_processing_timeout
        state.setTimeoutDuration(timeout_at)
        batch = []
    return batch

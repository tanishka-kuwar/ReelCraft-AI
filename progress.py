progress_data = {}


def update_progress(rec_id, percent, message):
    progress_data[rec_id] = {
        "percent": percent,
        "message": message
    }


def get_progress(rec_id):
    return progress_data.get(
        rec_id,
        {
            "percent": 0,
            "message": "Starting..."
        }
    )


def clear_progress(rec_id):
    progress_data.pop(rec_id, None)
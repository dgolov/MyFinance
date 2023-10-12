from datetime import datetime
from fastapi import status
from fastapi.responses import JSONResponse


def create_formatted_datetime(start: str, end: str) -> tuple:
    """ Форматиреует полученные значения datetime из запроса и переводит в utc,
        если они отсутствуют, то устанавливает значения по умолчанию
    """
    if not start:
        start_date = datetime.today().replace(day=1)
    else:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%f")
    if not end:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%f")

    return start_date, end_date


def get_formatted_datetime(start: str, end: str) -> tuple:
    """ Форматиреует полученные значения datetime из запроса и переводит в utc если они присутствуют
    """
    start_date = None
    end_date = None

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%f")
    if end:
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%f")

    return start_date, end_date


def prepare_response(
        result: dict,
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    if result.get("status") == "fail":
        return JSONResponse(
            status_code=fail_status_code,
            content={"message": result.get("message")}
        )
    return JSONResponse(
        status_code=success_status_code,
        content={"message": "ok"}
    )

from datetime import datetime, timedelta
from fastapi import APIRouter, Body

from actions import ERP
from schemas import NewTask

router = APIRouter()


@router.post('/new_task', status_code=201)
async def create_task_section(query: NewTask = Body(...)):
    erp = ERP()
    if query.task in [1, 2, 3, 4]:
        params = {
            "work_datedo": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "work_typer": query.task,
            "dopf_1": query.phone,
            "dopf_43": 1,
            "fio": query.fio if query.task == 2 else query.fio.title(),
            "dopf_42": query.address.upper(),
            "dopf_45": query.tariff.upper()

        }
    else:
        params = {
            "work_datedo": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "work_typer": query.task,
            "dopf_43": 1,
            "dopf_1": query.phone,
            "fio": query.fio.title()
        }
    return erp.check_task(params)

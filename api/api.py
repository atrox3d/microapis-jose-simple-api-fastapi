# print('API | ------- START ----------')

from datetime import datetime, UTC
import uuid
from fastapi import HTTPException, Request, Response, status

from api.schemas import CreateTaskSchema, GetTaskSchema, ListTasksSchema

# print('API | ---------- IMPORT SERVER ------------')
from api.server import server, session_maker
from data_access import models

TODO = []

@server.get(
    '/todo', 
    response_model=ListTasksSchema
)
def get_tasks(request:Request):
    # breakpoint()
    user_id = request.state.user_id
    with session_maker() as session:
        db_tasks = (
            session.query(models.User)          # from query users
            .filter(models.User.id == user_id)  # select current user
            .first()                            # first record
            .tasks                              # get tasks
        )
    return {'tasks': db_tasks}

@server.post(
    '/todo',
    response_model=GetTaskSchema,
    status_code=status.HTTP_201_CREATED
)
def create_task(payload:CreateTaskSchema, request:Request):
    now = datetime.now(UTC)

    with session_maker() as session:
        task = models.Task(
            **payload.model_dump(),
            user_id=request.state.user_id,
            created=now,
            updated=now
        )
        session.add(task)
        session.commit()
        task = task.dict()
    return task
    #
    task = payload.model_dump()
    task['id'] = uuid.uuid4()
    task['created'] = datetime.now(UTC)
    TODO.append(task)
    print(task)
    return task

@server.get(
    '/todo/{taskid}',
    response_model=GetTaskSchema
)
def get_task(task_id:uuid.UUID):
    for task in TODO:
        if GetTaskSchema(**task).id == task_id:
            print(task)
            return task
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )

@server.put(
    '/todo/{taskid}',
    response_model=GetTaskSchema
)
def update_task(task_id:uuid.UUID, payload:CreateTaskSchema):
    for task in TODO:
        if GetTaskSchema(**task).id == task_id:
            task |= payload
            print(task)
            return task
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )

@server.delete(
    '/todo/{taskid}',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def update_task(task_id:uuid.UUID):
    for ndx, task in enumerate(TODO):
        if GetTaskSchema(**TODO[ndx]).id == task_id:
            TODO.pop(ndx)
            print(TODO)
            return
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )

# print('API | ------- END ----------')
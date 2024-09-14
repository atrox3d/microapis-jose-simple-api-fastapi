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
            # **payload.model_dump(),
            created=now,
            updated=now,
            priority=payload.priority,
            status=payload.status,
            task=payload.task,
            user_id=request.state.user_id,
        )
        session.add(task)
        print(f'\n\n\n\n\n{task.dict()}\n\n\n\n\n\n')
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
    '/todo/{task_id}',
    response_model=GetTaskSchema
)
def get_task(task_id:uuid.UUID, request:Request):
    print(f'{task_id = }')
    with session_maker() as session:
        task = (
            session.query(models.Task)
            .filter(
                models.User.id==request.state.user_id,
                models.Task.user_id==request.state.user_id
            )
            .first()
        )
    if not task:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail=f'{task_id=} not found'
        )
    return task
    for task in TODO:
        if GetTaskSchema(**task).id == task_id:
            print(task)
            return task
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )

@server.put(
    '/todo/{task_id}',
    response_model=GetTaskSchema
)
def update_task(task_id:uuid.UUID, payload:CreateTaskSchema, request:Request):
    print('update task')
    with session_maker() as session:
        task = (
            session.query(models.Task)
            .filter(
                models.User.id==request.state.user_id,
                models.Task.user_id==request.state.user_id
            )
            .first()
        )
        print(f'{task.dict() = }')
        # task.task = ''
        if task:
            task.status = payload.status
            task.priority = payload.priority
            task.task = payload.task
            task.updated = datetime.now(UTC)
            session.add(task)
            session.commit()
            return task.dict()
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )
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
    '/todo/{task_id}',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id:uuid.UUID, request:Request):
    with session_maker() as session:
        task = (
            session.query(models.Task)
            .filter(
                models.User.id==request.state.user_id,
                models.Task.user_id==request.state.user_id
            )
            .first()
        )
        print(task)
        session.delete(task)
        session.commit()
        return
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail=f'{task_id=} not found'
    )
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
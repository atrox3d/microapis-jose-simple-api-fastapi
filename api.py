# print('API | ------- START ----------')

from datetime import datetime, UTC
import uuid
from schemas import CreateTaskSchema, GetTaskSchema, ListTasksSchema
from fastapi import HTTPException, Request, Response, status

# print('API | ---------- IMPORT SERVER ------------')
from server import server

TODO = []

@server.get(
    '/todo', 
    response_model=ListTasksSchema
)
def get_tasks(request:Request):
    ''' TODO: check return schema '''
    print(TODO)
    # breakpoint()
    user_id = request.state.user_id
    return {
        'tasks': TODO
    }

@server.post(
    '/todo',
    response_model=GetTaskSchema,
    status_code=status.HTTP_201_CREATED
)
def create_task(payload:CreateTaskSchema):
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
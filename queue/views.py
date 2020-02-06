from queue.router import router


@router.post('/enqueue').
async def enqueue_task(request):
    pass


@router.get('/')
async def list_tasks(request):
    pass


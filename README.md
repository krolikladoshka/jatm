**jatm**

test task

**to run**

*note: modify `PARALLEL_TASKS` setting in `.env` file to change number of tasks running simultaneously*

`docker-compose up -d`

**api**

* `GET /task_queue` - list tasks in queue
  * status - enqueued/processing
  * n - int
  * d - float
  * n1 - float
  * interval - float
  * v - current value
  * created_datetime - submit datetime
* `POST /task_queue/enqueue` - submit task to queue
  * *params*
  * n - int
  * d - float
  * n1 - float
  * interval - float


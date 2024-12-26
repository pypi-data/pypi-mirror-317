#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/11/1
# @Author  : zhoubohan
# @File    : tracker.py
"""
import atexit
import os
import queue
import threading
from typing import Optional, Union

from jobv1.client.job_api_event import CreateEventRequest
from jobv1.client.job_api_job import parse_job_name
from jobv1.client.job_api_metric import CreateMetricRequest
from jobv1.client.job_api_task import CreateTaskRequest, parse_task_name
from windmillclient.client.windmill_client import WindmillClient


class Tracker(object):
    """
    Tracker is agent to track metric&event.
    """

    def __init__(
        self,
        windmill_client: Optional[WindmillClient] = None,
        workspace_id: Optional[str] = None,
        job_name: Optional[str] = None,
        task_name: Optional[str] = None,
    ):
        """
        Create a new tracker.
        """

        self._windmill_client = windmill_client
        self._job_name = job_name
        self._task_name = task_name
        self._workspace_id = workspace_id

        if self._windmill_client is None:
            endpoint = os.getenv("WINDMILL_ENDPOINT", "")
            org_id = os.getenv("ORG_ID", "")
            user_id = os.getenv("USER_ID", "")
            if endpoint == "" or org_id == "" or user_id == "":
                raise ValueError("WINDMILL_ENDPOINT, ORG_ID, USER_ID must be set.")
            self._windmill_client = WindmillClient(
                endpoint=endpoint, context={"OrgID": org_id, "UserID": user_id}
            )

        if self._job_name is not None:
            self.set_job_name(self._job_name)

        if self._task_name is not None:
            self.set_task_name(self._task_name)

        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._process_queue)
        self._thread.daemon = True
        self._thread.start()

        atexit.register(self._cleanup)

    def _process_queue(self):
        while True:
            func, args = self._queue.get()
            if func is None:
                break
            func(args)
            self._queue.task_done()

    def _cleanup(self):
        """
        Cleanup the tracker.
        """
        self._queue.put((None, ()))
        self._thread.join()

    def set_job_name(self, job_name: str):
        """
        Set job name.
        :param job_name:
        :return:
        """
        jn = parse_job_name(job_name)
        if jn is not None:
            self._job_name = jn.local_name
            self._workspace_id = jn.workspace_id
        else:
            self._job_name = job_name

    def set_task_name(self, task_name: str):
        """
        Set task name.
        :param task_name:
        :return:
        """
        tn = parse_task_name(task_name)
        if tn is not None:
            self._task_name = tn.local_name
            self._workspace_id = tn.workspace_id
        else:
            self._task_name = task_name

    def _set_default(
        self, request: Union[CreateTaskRequest, CreateMetricRequest, CreateEventRequest]
    ):
        """
        Set default value.
        """
        if request.workspace_id is None or len(request.workspace_id) == 0:
            request.workspace_id = self._workspace_id
        if request.job_name is None or len(request.job_name) == 0:
            request.job_name = self._job_name

        if request.field_exists("task_name") and (
            request.task_name is None or len(request.task_name) == 0
        ):
            request.task_name = self._task_name

    def create_task(self, request: CreateTaskRequest):
        """
        Create task.
        """
        self._set_default(request)
        self._queue.put((self._windmill_client.create_task, request))

    def log_metric(self, request: CreateMetricRequest):
        """
        Log metric.
        :param request: CreateMetricRequest
        :return: None
        """
        self._set_default(request)
        self._queue.put((self._windmill_client.create_metric, request))

    def log_event(self, request: CreateEventRequest):
        """
        Log event.
        :param request: CreateEventRequest
        :return: None
        """
        self._set_default(request)
        self._queue.put((self._windmill_client.create_event, request))

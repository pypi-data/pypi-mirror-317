#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_api_base.py
"""
from enum import Enum


class JobStatus(Enum):
    """
    JobStatus is the status of the job.
    """

    Pending = "Pending"
    Running = "Running"
    Succeeded = "Succeeded"
    Terminating = "Terminating"
    Terminated = "Terminated"
    Failed = "Failed"
    PartialSucceeded = "PartialSucceeded"

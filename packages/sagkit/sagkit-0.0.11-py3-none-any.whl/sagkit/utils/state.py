"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 18:00:00
LastEditTime: 2024-11-08 17:19:19
FilePath: \\sagkit\\src\\sagkit\\utils\\state.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

from typing import List


class State:
    def __init__(self, id: int, EFT: int, LFT: int, job_path: List) -> None:
        self.id = id
        self.EFT = EFT
        self.LFT = LFT
        self.depth = len(job_path)
        self.job_path = job_path
        self.next_jobs = []
        self.next_states = []

    def is_leaf(self) -> bool:
        return len(self.next_states) == 0

    def __str__(self) -> str:
        return (
            "State " + str(self.id) + " [" + str(self.EFT) + ", " + str(self.LFT) + "]"
        )

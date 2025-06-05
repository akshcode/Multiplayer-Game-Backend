from typing import List
from .rwmodel import RWModel
from .profile import ProfileInLeaderboard

class Leaderboard(RWModel):
    leaderboard_list: List[ProfileInLeaderboard]
from pathlib import Path
from dataclasses import dataclass, field
from math import pi

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team
from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.common_exercises.bronze_striker import BallInFrontOfGoal
from rlbottraining.common_exercises.bronze_goalie import BallRollingToGoalie
from rlbottraining.common_exercises.silver_goalie import DefendBallRollingTowardsGoal, LineSave, TryNotToOwnGoal
from rlbottraining.common_exercises.ball_prediction import PredictBallInAir
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.match_configs import make_empty_match_config
from rlbottraining.grading.grader import Grader
from rlbottraining.training_exercise import TrainingExercise, Playlist

import training_util
from drive_to_ball_grader import DriveToBallGrader

def make_match_config_with_my_bot(name) -> MatchConfig:
    # Makes a config which only has our bot in it for now.
    # For more defails: https://youtu.be/uGFmOZCpel8?t=375
    match_config = make_empty_match_config()
    match_config.player_configs = [
        PlayerConfig.bot_config(
            Path(__file__).absolute().parent.parent / 'stick' / 'stick.cfg',
            Team.BLUE
        )
    ]
    match_config.player_configs[0].name = name
    return match_config

@dataclass
class StrikerPatience(StrikerExercise):
    """
    Drops the ball from a certain height, requiring the bot to not drive
    underneath the ball until it's in reach.
    """

    car_start_x: float = 0

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 1000),
                velocity=Vector3(0, 0, 200),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(self.car_start_x, 3000, 0),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

@dataclass
class DrivesToBallExercise(TrainingExercise):
    """
    Checks that we drive to the ball when it's in the center of the field.
    """
    grader: Grader = field(default_factory=DriveToBallGrader)

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 2000, 0),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=100)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


def make_default_playlist() -> Playlist:
    exercises = [
        BallRollingToGoalie('BallRollingToGoalie')
    ]
    for exercise in exercises:
        exercise.match_config = make_match_config_with_my_bot(exercise.name)

    return exercises
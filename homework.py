from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError(' You need to override the method')

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):

    AVG_SPEED_MUL = 18
    AVG_SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.AVG_SPEED_MUL * self.get_mean_speed()
                - self.AVG_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.MIN_IN_H
            * self.duration
        )


class SportsWalking(Training):

    BURN_KCAL_PER_MIN = 0.035
    AVG_SPEED_HEIGHT_WEIGHT_MUL = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.BURN_KCAL_PER_MIN * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.AVG_SPEED_HEIGHT_WEIGHT_MUL
                * self.weight
            )
            * self.MIN_IN_H
            * self.duration
        )


class Swimming(Training):

    LEN_STEP = 1.38
    AVG_SPEED_SHIFT = 1.1
    WEIGHT_MUL = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.AVG_SPEED_SHIFT)
            * self.WEIGHT_MUL
            * self.weight
        )


class InvalidInputDataError(Exception):
    pass


TRAINING: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[float]) -> Training:
    try:
        return TRAINING[workout_type](*data)
    except (KeyError, TypeError):
        raise InvalidInputDataError(' your data is not correct')


def main(training: Training) -> None:
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

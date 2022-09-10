from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    # Почему не видит General_Message
    general_message = ("Тип тренировки: {training_type}; "
                       + "Длительность: {duration_HRS:.3f} ч.; "
                       + "Дистанция: {distance:.3f} км; "
                       + "Ср. скорость: {speed:.3f} км/ч; "
                       + "Потрачено ккал: {calories:.3f}.")

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration_HRS = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self) -> str:
        return self.general_message.format(training_type=self.training_type,
                                           duration_HRS=self.duration_HRS,
                                           distance=self.distance,
                                           speed=self.speed,
                                           calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60
    SQUARED: int = 2
    training_type: str = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_HRS = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_HRS

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type, self.duration_HRS,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    training_type: str = 'Running'
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight
                / self.M_IN_KM * self.duration_HRS * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type: str = 'SportsWalking'
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** self.SQUARED // self.height)
                * self.coeff_calorie_2 * self.weight)
                * self.duration_HRS * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    training_type: str = 'Swimming'
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: int = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration_HRS)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in class_dict.keys():
        raise Exception('You have KeyError, check packages!')
    else:
        return class_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

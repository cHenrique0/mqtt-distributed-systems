from nanoid import generate


class Sensor:
    def __init__(self, area: str, sensor_type: str) -> None:
        self.__id = generate(size=10)
        self.__area = area.lower()
        self.__sensor_type = sensor_type.lower()
        self.__value = 0
        self.__topic = f"area/{self.__area}/sensor/{self.__id}/{self.__sensor_type}"

    def get_id(self) -> str:
        return self.__id

    def get_area(self) -> int:
        return self.__area

    def get_type(self) -> str:
        return self.__sensor_type

    def get_value(self) -> int:
        return self.__value

    def set_value(self, value: float) -> None:
        self.__value = value

    def get_topic(self) -> str:
        return self.__topic

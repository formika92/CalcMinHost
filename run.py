import click

from io import (
    TextIOWrapper,
)
from typing import (
    List,
)


def dec_to_binary(ip_address: List[int]) -> List[str]:
    """
    Переводит адресс в бинарный код
    """
    return list(map(lambda x: bin(x)[2:].zfill(8), ip_address))


def negation_mask(net_mask: List[int]) -> List[int]:
    """
    Рассчитывает обратную маску
    """
    value_list = list()
    for number in net_mask:
        value_list.append(255 - int(number))
    return value_list


class IPMinHostCalculator(object):
    def __init__(self, ip_address: str, cdir=24):
        if '/' in ip_address:
            self._address_val, self._cidr = ip_address.split('/')
            self._address = [int(i) for i in self._address_val.split('.')]
        else:
            self._address = [int(i) for i in ip_address.split('.')]
            self._cidr = cdir
        self.binary_ip = dec_to_binary(self._address)
        self.binary_mask = None
        self.negation_mask = None
        self.network = None
        self.broadcast = None

    def show(self) -> None:
        """
        Отображает данные мин. адреса хоста
        """
        self.calc()
        print(f'Min host {self.calc_min_host()}')

    def calc(self) -> None:
        # вызываем функции для расчетов
        self.net_mask()
        self.network_ip()
        self.broadcast_ip()

    def net_mask(self) -> List[int]:
        """
        Рассчитывает маску
        """
        mask = [0, 0, 0, 0]
        for i in range(int(self._cidr)):
            mask[int(i / 8)] += 1 << (7 - i % 8)  #
        self.binary_mask = dec_to_binary(mask)
        self.negation_mask = dec_to_binary(negation_mask(mask))
        return mask

    def broadcast_ip(self) -> List[int]:
        """
        Рассчитывает широковещательный адрес
        """
        broadcast = list()
        for x, y in zip(self.binary_ip, self.negation_mask):
            broadcast.append(int(x, 2) | int(y, 2))
        self.broadcast = broadcast
        return broadcast

    def network_ip(self) -> List[int]:
        """
        Рассчитывает идентификатор сети
        """
        network = list()
        for x, y in zip(self.binary_ip, self.binary_mask):
            network.append(int(x, 2) & int(y, 2))
        self.network = network
        return network

    def calc_min_host(self) -> str:
        """
        Рассчитывает минимальный адрес хоста подсети
        """
        min_host = self.network
        min_host[-1] += 1
        return "%s" % (".".join(map(str, min_host)))


def validate_ip(line: str) -> bool:
    """
    Проверяет корректность указанного IP
    """
    values = line.partition('/')  # в файле может передаваться маска
    values_mask = values[2]
    if values_mask:
        values_mask = values_mask.rstrip()
        if len(values_mask) > 2:
            return False
        if not values_mask.isdigit():
            return False
    pieces = values[0].split('.')  # проверяем составляющие адреса
    if len(pieces) != 4:
        return False
    try:
        return all(
            0 <= int(piece) < 256 for piece in pieces
        )
    except ValueError:
        return False

@click.command()
@click.option('--file')
@click.option('--ip_version')
def ip_calculate(file: TextIOWrapper, ip_version: str) -> None:
    if file and ip_version:
        if ip_version.lower() == 'ipv4':
            with open(f'{file}') as file:
                for line in file:
                    validate = validate_ip(line)
                    if validate:
                        ip = IPMinHostCalculator(line)
                        ip.show()
                    else:
                        print('Uncorrect line!')
        else:
            print('Only IpV4 version supported')
    else:
        print('Need file name and IP version!')


if __name__ == '__main__':
    ip_calculate()

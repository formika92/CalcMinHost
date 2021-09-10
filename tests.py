import unittest

from click.testing import (
    CliRunner,
)

from run import (
    dec_to_binary,
    IPMinHostCalculator,
    ip_calculate,
)


class CalcBinaryCase(unittest.TestCase):
    """
    Тест для расчета бинарного кода
    """
    def test_dec_to_binary(self) -> None:
        self.assertEqual(dec_to_binary([192, 168, 1, 1]), ['11000000', '10101000', '00000001', '00000001'])
        self.assertEqual(dec_to_binary([192, 168, 1, 1]), ['11000000', '10101000', '00000001', '00000001'])
        self.assertEqual(dec_to_binary([255, 255, 255, 128]), ['11111111', '11111111', '11111111', '10000000'])

        self.assertEqual(dec_to_binary([]), [])
        with self.assertRaises(TypeError):
            dec_to_binary(1)

        with self.assertRaises(TypeError):
            dec_to_binary(None)

        self.assertEqual(dec_to_binary([9955, 255, 255, 128]), ['10011011100011', '11111111', '11111111', '10000000'])


class CalcBroadcastAssertCase(unittest.TestCase):
    """
    Тест для расчета широковещательного адреса при входных данных ожидаемого типа
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1')
        self.ipminhostcalc.binary_ip = ['11000000', '10101000', '00000001', '00000001']
        self.ipminhostcalc.binary_mask = ['11111111', '11111111', '11111111', '10000000']
        self.ipminhostcalc.negation_mask = ['00000000', '00000000', '00000000', '01111111']
        self.ipminhostcalc.network = [192, 168, 1, 0]

    def test_calc_broadcast(self) -> None:
        self.assertEqual(self.ipminhostcalc.broadcast_ip(), [192, 168, 1, 127])

class CalcBroadcastRaiseCase(unittest.TestCase):
    """
    Тест для расчета широковещательного адреса при входных данных неожидаемого типа
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1')
        self.ipminhostcalc.binary_ip = ['11000000', '10101000', '00000001', '00000001']
        self.ipminhostcalc.binary_mask = [1, 1, 1, 1]
        self.ipminhostcalc.negation_mask = [1, 1, 1, 1]
        self.ipminhostcalc.network = []

    def test_calc_broadcast(self) -> None:
        with self.assertRaises(TypeError):
            self.ipminhostcalc.broadcast_ip()

class CalcNetworkAssertCase(unittest.TestCase):
    """
    Тест для расчета идентификатора сети при вх. данных ожидаемого типа
    """

    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1')
        self.ipminhostcalc.binary_ip = ['11000000', '10101000', '00000001', '00000001']
        self.ipminhostcalc.binary_mask = ['11111111', '11111111', '11111111', '10000000']

    def test_calc_network(self) -> None:
        self.assertEqual(self.ipminhostcalc.network_ip(), [192, 168, 1, 0])

class CalcNetworkRaiseCase(unittest.TestCase):
    """
    Тест для расчета идентификатора сети при вх. данных неожидаемого типа
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1')
        self.ipminhostcalc.binary_ip = ['11000000', '10101000', '00000001', '00000001']
        self.ipminhostcalc.binary_mask = [1, 1, 1, 1]

    def test_calc_network(self) -> None:
        with self.assertRaises(TypeError):
            self.ipminhostcalc.broadcast_ip()


class CalcNetMaskAssertCase(unittest.TestCase):
    """
    Тест assert для маски сети
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1')

    def test_calc_net_mask(self) -> None:
        self.assertEqual(self.ipminhostcalc.net_mask(), [255, 255, 255, 0])


class CalcNetMaskRaiseCase(unittest.TestCase):
    """
    Тест raise для маски сети
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('192.168.1.1', 'abc')

    def test_calc_net_mask(self) -> None:
        with self.assertRaises(ValueError):
            self.ipminhostcalc.net_mask()


class CalcMinHostAssertCase(unittest.TestCase):
    """
    Тест assert для расчета минимального хоста
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('62.76.0.0')
        self.ipminhostcalc.network = [62, 16, 64, 0]

    def test_calc_min_host(self) -> None:
        self.assertEqual(self.ipminhostcalc.calc_min_host(), '62.16.64.1')


class CalcMinHostRaiseCase(unittest.TestCase):
    """
    Тест raise для расчета минимального хоста
    """
    def setUp(self) -> None:
        self.ipminhostcalc = IPMinHostCalculator('62.76.0.0')
        self.ipminhostcalc.network = ['62', '76c']

    def test_calc_min_host(self) -> None:
        with self.assertRaises(TypeError):
            self.ipminhostcalc.calc_min_host()


class CalcCalcIpCase(unittest.TestCase):
    """
    Тест ля расчета минимального хоста
    """

    def test_calc_ip(self) -> None:
        runner = CliRunner()
        result = runner.invoke(ip_calculate, ['--file', 'ip_list.txt', '--ip_version', 'ipv4'])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            'Min host 192.168.1.1\nMin host 62.16.64.1\nMin host 62.61.0.1\nMin host 62.64.0.1\nMin host 62.69.0.1\nMin host 62.76.0.1\nMin host 62.102.128.1\nMin host 62.105.128.1\nMin host 62.118.0.1\n'  # noqa
        )

    def test_calc_ip_incorrect_version(self) -> None:
        runner = CliRunner()  # т.к. функция обернута в декораторы click
        result = runner.invoke(ip_calculate, ['--file', 'ip_list_test.txt', '--ip_version', 'ipv4'])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            'Uncorrect line!\nUncorrect line!\nUncorrect line!\nUncorrect line!\n'  # noqa
        )


if __name__ == '__main__':
    unittest.main()

from unittest.case import TestCase
from unittest.mock import MagicMock
from bauzak.Modbus控制器 import Modbus控制器


class 讀16位元(TestCase):

    def setUp(self):
        self.PLC控制 = Modbus控制器(
            'localhost', '502'
        )
        self.PLC控制.連線 = MagicMock()

    def test_無半个(self):
        表 = {
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_not_called()

    def test_一个(self):
        表 = {
            'R1036': 'A做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_called_once_with(1036, 1)

    def test_特殊counter(self):
        表 = {
            'C255': 'A做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        try:
            self.PLC控制.連線.read_holding_registers.assert_called_once_with(
                9810, 1
            )
        except:
            self.PLC控制.連線.read_holding_registers.assert_called_once_with(
                9865, 1
            )

    def test_讀的表佇仝一段(self):
        表 = {
            'R1036': 'A做了幾項',
            'R1038': 'B做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_called_once_with(1036, 3)

    def test_仝段上遠(self):
        表 = {
            'R1000': 'A做了幾項',
            'R1124': 'B做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_called_once_with(1000, 125)

    def test_讀的表佇無仝一段(self):
        表 = {
            'R1000': 'A做了幾項',
            'R1125': 'B做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_any_call(1000, 1)
        self.PLC控制.連線.read_holding_registers.assert_any_call(1125, 1)

    def test_無仝的暫存器嘛會使(self):
        表 = {
            'R1036': 'A做了幾項',
            'R1136': 'AA做了幾項',
            'D100': 'B做了幾項',
            'D110': 'BB做了幾項',
        }
        self.PLC控制.讀16位元的資料(表)
        self.PLC控制.連線.read_holding_registers.assert_any_call(1036, 101)
        self.PLC控制.連線.read_holding_registers.assert_any_call(6100, 11)

    def test_暫存器數字(self):
        表 = {
            'R1036': 'A做了幾項',
            'R1038': 'AA做了幾項',
            'D100': 'B做了幾項',
            'D104': 'BB做了幾項',
        }
        答案 = {
            'A做了幾項': 10,
            'AA做了幾項': 20000,
            'B做了幾項':  3,
            'BB做了幾項': 0,
        }
        頭一个回應 = MagicMock()
        頭一个回應.registers = [10, 0, 20000]
        第二个回應 = MagicMock()
        第二个回應.registers = [3, 6, 0, 0, 0]
        self.PLC控制.連線.read_holding_registers.side_effect = [頭一个回應, 第二个回應]

        結果 = self.PLC控制.讀16位元的資料(表)
        self.assertEqual(結果, 答案)

    def test_連續暫存器(self):
        表 = {
            'R1036': 'A做了幾項',
            'R1037': 'AA做了幾項',
            'R1038': 'AAA做了幾項',
        }
        答案 = {
            'A做了幾項':  1,
            'AA做了幾項': 2,
            'AAA做了幾項':  3,
        }
        頭一个回應 = MagicMock()
        頭一个回應.registers = [1, 2, 3]
        self.PLC控制.連線.read_holding_registers.return_value = 頭一个回應

        結果 = self.PLC控制.讀16位元的資料(表)
        self.assertEqual(結果, 答案)

import unittest

from navigate import Navigator, Actions


class TestNavigate(unittest.TestCase):

	navigator = Navigator("loc_points_test.json")

	def test_1_right_turn(self):
		route = self.navigator.navigate('Hecktor 1', 'Hecktor 3')
		self.assertListEqual([(Actions.GO, 'Red'),
							  (Actions.ROTATE_RIGHT, 1),
							  (Actions.GO, 'Blue')
							  ],
							 route)

	def test_1_right_1_left(self):
		route = self.navigator.navigate('Hecktor 1', 'Hecktor 5')
		self.assertListEqual([(Actions.GO, 'Red'),
							  (Actions.ROTATE_RIGHT, 1),
							  (Actions.GO, 'Blue'),
							  (Actions.ROTATE_RIGHT, 1),
							  (Actions.GO, 'Blue'),
							  (Actions.ROTATE_RIGHT, 3),
							  (Actions.GO, 'Blue'),
							  ],
							 route)

	def test_2_right_turns(self):
		route = self.navigator.navigate('Hecktor 5', 'Hecktor 7')
		self.assertListEqual([(Actions.GO, 'Blue'),
							  (Actions.ROTATE_RIGHT, 1),
							  (Actions.GO, 'Blue'),
							  (Actions.ROTATE_RIGHT, 1),
							  (Actions.GO, 'Red'),
							  (Actions.GO, 'Blue'),
							  ],
							 route)

	def test_get_rotation_none_1(self):
		self.assertEquals(None, self.navigator._get_rotation((0, 10), (0, 0), (0, 10)))

	def test_get_rotation_none_2(self):
		self.assertEquals(None, self.navigator._get_rotation((10, 0), (10, 10), (20, 10)))

	def test_get_rotation_1_right_1(self):
		self.assertEquals((Actions.ROTATE_RIGHT, 1), self.navigator._get_rotation((0, 10), (0, 10), (10, 10)))

	def test_get_rotation_1_right_1(self):
		self.assertEquals((Actions.ROTATE_RIGHT, 1), self.navigator._get_rotation((10, 0), (20, 10), (20, 0)))

	def test_get_rotation_2_right_1(self):
		self.assertEquals((Actions.ROTATE_RIGHT, 2), self.navigator._get_rotation((-10, 0), (10, 0), (20, 0)))

	def test_get_rotation_3_right_1(self):
		self.assertEquals((Actions.ROTATE_RIGHT, 3), self.navigator._get_rotation((0, -10), (10, 0), (20, 0)))

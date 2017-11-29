import json

LOC_POINTS_FILE = "loc_points.json"

class Actions:
	GO = 'Go',
	ROTATE_RIGHT = 'Rotate Right'

class Navigator:

	def __init__(self, loc_points_file=LOC_POINTS_FILE):
		self.loc_dict = self.build_loc_dict(loc_points_file)

	def build_loc_dict(self, loc_points_file):
		with open(loc_points_file) as jsonfile:
			json_data = json.load(jsonfile)
			loc_dict = {}
			for point in json_data['points']:
				point['cor'] = (point['X'], point['Y'])
				loc_dict[point['name']] = point
			loc_dict = {point['name']: point for point in json_data['points']}
			return loc_dict

	def find_shortest_path(self, graph, start, end, path=[]):
		path = path + [start]
		if start == end:
			return path
		shortest = None
		for node in graph[start]['neighbors']:
			if node not in path:
				newpath = self.find_shortest_path(graph, node, end, path)
				if newpath:
					if not shortest or len(newpath) < len(shortest):
						shortest = newpath
		return shortest

	def navigate(self, source_name, target_name):
		if source_name not in self.loc_dict or target_name not in self.loc_dict:
			print('Source {%s} or Target {%s} not in graph: {%s}!' %
				  (source_name, target_name, self.loc_dict.keys()))
			return []
		if source_name == target_name:
			print(('Source equals Target! {%s}' % source_name))
			return []
		shortest_path = self.find_shortest_path(self.loc_dict, source_name, target_name)
		if not shortest_path:
			raise Exception("No path found between source {%s} and target {%s} in graph: {%s}" %
							(source_name, target_name, self.loc_dict.keys()))
		prev_point = self.loc_dict[shortest_path[0]]
		next_point = self.loc_dict[shortest_path[1]]
		route = []
		curr_direction = (next_point['X'] - prev_point['X'], next_point['Y'] - prev_point['Y'])
		for i in range(1, len(shortest_path)):
			next_point = self.loc_dict[shortest_path[i]]
			rotation = self._get_rotation(curr_direction, prev_point['cor'], next_point['cor'])
			if rotation:
				route.append(rotation)
			curr_direction = self._minus_tuple(next_point['cor'], prev_point['cor'])
			if curr_direction[0] != 0 and curr_direction[1] != 0:
				raise Exception('points not aligned, going from %s to %s' %
								(prev_point['name'], next_point['name']))
			route.append((Actions.GO, next_point['color']))
			prev_point = next_point
		return route

	def _get_rotation(self, curr_direction, prev_point, next_point):
		needed_direction = self._minus_tuple(next_point, prev_point)
		if curr_direction == needed_direction:
			return None
		times = 0
		while curr_direction != needed_direction:
			if curr_direction[0] >= 0 and curr_direction[1] >= 0:
				curr_direction = ((curr_direction[0] + 10) % 20, (curr_direction[1] - 10) % -20)
			else:
				curr_direction = ((curr_direction[0] - 10) % -20, (curr_direction[1] - 10) % 20)
			times += 1
		return (Actions.ROTATE_RIGHT, times)

	def _minus_tuple(self, tup2, tup1):
		return (tup2[0] - tup1[0], tup2[1] - tup1[1])

if __name__ == "__main__":
	navigator = Navigator(LOC_POINTS_FILE)
	navigator.navigate('Hecktor 1', 'Hecktor 3')

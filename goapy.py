#GOAPy
#Generic GOAP implementation.
#flags - https://github.com/flags

#The MIT License (MIT)
#
#Copyright (c) 2014 Luke Martin (flags)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


class World:
	def __init__(self):
		self.planners = []
		self.plans = []

	def add_planner(self, planner):
		self.planners.append(planner)

	def calculate(self):
		self.plans = []
		
		for planner in self.planners:
			self.plans.append(planner.calculate())

	def get_plan(self, debug=False):
		_plans = {}

		for plan in self.plans:
			_plan_cost = sum([action['g'] for action in plan])

			if _plan_cost in _plans:
				_plans[_plan_cost].append(plan)
			else:
				_plans[_plan_cost] = [plan]

		_sorted_plans = _plans.keys()
		_sorted_plans.sort()

		if debug:
			_i = 1
			
			for plan_score in _sorted_plans:
				for plan in _plans[plan_score]:
					print _i

					for action in plan:
						print '\t', action['name']

					_i += 1

					print '\n\tTotal cost: %s\n' % plan_score
		
		return [_plans[p][0] for p in _sorted_plans]

class Planner:
	def __init__(self, *keys):
		self.start_state = None
		self.goal_state = None
		self.values = {k: -1 for k in keys}
		self.action_list = None

	def state(self, **kwargs):
		_new_state = self.values.copy()
		_new_state.update(kwargs)

		return _new_state

	def set_start_state(self, **kwargs):
		_invalid_states = set(kwargs.keys()) - set(self.values.keys())

		if _invalid_states:
			raise Exception('Invalid states for world start state: %s' % ', '.join(list(_invalid_states)))

		self.start_state = self.state(**kwargs)

	def set_goal_state(self, **kwargs):
		_invalid_states = set(kwargs.keys()) - set(self.values.keys())

		if _invalid_states:
			raise Exception('Invalid states for world goal state: %s' % ', '.join(list(_invalid_states)))

		self.goal_state = self.state(**kwargs)

	def set_action_list(self, action_list):
		self.action_list = action_list

	def calculate(self):
		return astar(self.start_state,
					 self.goal_state,
					 {c: self.action_list.conditions[c].copy() for c in self.action_list.conditions},
					 {r: self.action_list.reactions[r].copy() for r in self.action_list.reactions},
					 self.action_list.weights.copy())

class Action_List:
	def __init__(self):
		self.conditions = {}
		self.reactions = {}
		self.weights = {}

	def add_condition(self, key, **kwargs):
		if not key in self.weights:
			self.weights[key] = 1

		if not key in self.conditions:
			self.conditions[key] = kwargs

			return

		self.conditions[key].update(kwargs)

	def add_reaction(self, key, **kwargs):
		if not key in self.conditions:
			raise Exception('Trying to add reaction \'%s\' without matching condition.' % key)

		if not key in self.reactions:
			self.reactions[key] = kwargs

			return

		self.reactions[key].update(kwargs)

	def set_weight(self, key, value):
		if not key in self.conditions:
			raise Exception('Trying to set weight \'%s\' without matching condition.' % key)

		self.weights[key] = value


def distance_to_state(state_1, state_2):
	_scored_keys = set()
	_score = 0
	
	for key in state_2.keys():
		_value = state_2[key]
		
		if _value == -1:
			continue

		if not _value == state_1[key]:
			_score += 1
		
		_scored_keys.add(key)
	
	for key in state_1.keys():
		if key in _scored_keys:
			continue
		
		_value = state_1[key]
		
		if _value == -1:
			continue
		
		if not _value == state_2[key]:
			_score += 1

	return _score

def conditions_are_met(state_1, state_2):
	for key in state_2.keys():
		_value = state_2[key]

		if _value == -1:
			continue

		if not state_1[key] == state_2[key]:
			return False

	return True

def node_in_list(node, node_list):
	for next_node in node_list.values():
		if node['state'] == next_node['state'] and node['name'] == next_node['name']:
			return True

	return False

def create_node(path, state, name=''):
	path['node_id'] += 1
	path['nodes'][path['node_id']] = {'state': state, 'f': 0, 'g': 0, 'h': 0, 'p_id': None, 'id': path['node_id'], 'name': name}

	return path['nodes'][path['node_id']]

def astar(start_state, goal_state, actions, reactions, weight_table):
	_path = {'nodes': {},
	         'node_id': 0,
	         'goal': goal_state,
	         'actions': actions,
	         'reactions': reactions,
	         'weight_table': weight_table,
	         'action_nodes': {},
	         'olist': {},
	         'clist': {}}

	_start_node = create_node(_path, start_state, name='start')
	_start_node['g'] = 0
	_start_node['h'] = distance_to_state(start_state, goal_state)
	_start_node['f'] = _start_node['g'] + _start_node['h']
	_path['olist'][_start_node['id']] = _start_node
	
	for action in actions:
		_path['action_nodes'][action] = create_node(_path, actions[action], name=action)

	return walk_path(_path)

def walk_path(path):
	node = None

	_clist = path['clist']
	_olist = path['olist']

	while len(_olist):
		####################
		##Find lowest node##
		####################
		
		_lowest = {'node': None, 'f': 9000000}
		
		for next_node in _olist.values():
			if not _lowest['node'] or next_node['f'] < _lowest['f']:
				_lowest['node'] = next_node['id']
				_lowest['f'] = next_node['f']

		if _lowest['node']:
			node = path['nodes'][_lowest['node']]

		else:
			return
		
		################################
		##Remove node with lowest rank##
		################################
		
		del _olist[node['id']]
		
		#######################################
		##If it matches the goal, we are done##
		#######################################
		
		if conditions_are_met(node['state'], path['goal']):
			_path = []

			while node['p_id']:
				_path.append(node)

				node = path['nodes'][node['p_id']]
			
			_path.reverse()
			
			return _path
		
		####################
		##Add it to closed##
		####################
		
		_clist[node['id']] = node
		
		##################
		##Find neighbors##
		##################
		
		_neighbors = []
		
		for action_name in path['action_nodes']:
			if not conditions_are_met(node['state'], path['action_nodes'][action_name]['state']):
				continue

			path['node_id'] += 1

			_c_node = node.copy()
			_c_node['state'] = node['state'].copy()
			_c_node['id'] = path['node_id']
			_c_node['name'] = action_name

			for key in path['reactions'][action_name]:
				_value = path['reactions'][action_name][key]

				if _value == -1:
					continue

				_c_node['state'][key] = _value
			
			path['nodes'][_c_node['id']] = _c_node
			_neighbors.append(_c_node)

		for next_node in _neighbors:
			_g_cost = node['g'] + path['weight_table'][next_node['name']]
			_in_olist, _in_clist = node_in_list(next_node, _olist), node_in_list(next_node, _clist)
			
			if _in_olist and _g_cost < next_node['g']:
				del _olist[next_node]
			
			if _in_clist and _g_cost < next_node['g']:
				del _clist[next_node['id']]
			
			if not _in_olist and not _in_clist:
				next_node['g'] = _g_cost
				next_node['h'] = distance_to_state(next_node['state'], path['goal'])
				next_node['f'] = next_node['g'] + next_node['h']
				next_node['p_id'] = node['id']
				
				_olist[next_node['id']] = next_node

	return []

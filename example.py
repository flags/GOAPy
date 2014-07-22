from goapy import World, Action_List

if __name__ == '__main__':
	import time
	import sys

	_world = World('hungry', 'has_food', 'in_kitchen', 'tired', 'in_bed')
	_world.set_start_state(hungry=True, has_food=False, in_kitchen=False, tired=True, in_bed=False)
	_world.set_goal_state(tired=False)

	_actions = Action_List()
	_actions.add_condition('eat', hungry=True, has_food=True, in_kitchen=False)
	_actions.add_reaction('eat', hungry=False)
	_actions.add_condition('cook', hungry=True, has_food=False, in_kitchen=True)
	_actions.add_reaction('cook', has_food=True)
	_actions.add_condition('sleep', tired=True, in_bed=True)
	_actions.add_reaction('sleep', tired=False)
	_actions.add_condition('go_to_bed', in_bed=False, hungry=False)
	_actions.add_reaction('go_to_bed', in_bed=True)
	_actions.add_condition('go_to_kitchen', in_kitchen=False)
	_actions.add_reaction('go_to_kitchen', in_kitchen=True)
	_actions.add_condition('leave_kitchen', in_kitchen=True)
	_actions.add_reaction('leave_kitchen', in_kitchen=False)
	_actions.add_condition('order_pizza', has_food=False, hungry=True)
	_actions.add_reaction('order_pizza', has_food=True)
	_actions.set_weight('go_to_kitchen', 20)
	_actions.set_weight('order_pizza', 1)

	_world.set_action_list(_actions)
	
	_t = time.time()
	_path = _world.calculate()
	_took_time = time.time() - _t

	for path in _path:
		print _path.index(path)+1, path['name']

	print '\nTook:', _took_time
from goapy import World, Planner, Action_List

if __name__ == '__main__':
    import time

    _brain = World()

    _combat_brain = Planner('has_ammo',
                            'has_weapon',
                            'weapon_armed',
                            'weapon_loaded',
                            'in_engagement',
                            'in_cover',
                            'in_enemy_los',
                            'is_near')
    _combat_brain.set_start_state(in_engagement=True,
                                  is_near=False,
                                  in_cover=False,
                                  in_enemy_los=True,
                                  has_ammo=False,
                                  has_weapon=True,
                                  weapon_armed=False,
                                  weapon_loaded=False)
    _combat_brain.set_goal_state(in_engagement=False)

    _combat_actions = Action_List()
    _combat_actions.add_condition('track',
                                  is_near=False,
                                  weapon_armed=True)
    _combat_actions.add_reaction('track', is_near=True)
    _combat_actions.add_condition('unpack_ammo', has_ammo=False)
    _combat_actions.add_reaction('unpack_ammo', has_ammo=True)
    _combat_actions.add_condition('search_for_ammo', has_ammo=False)
    _combat_actions.add_reaction('search_for_ammo', has_ammo=True)
    _combat_actions.add_condition('reload',
                                  has_ammo=True,
                                  weapon_loaded=False,
                                  in_cover=True)
    _combat_actions.add_reaction('reload', weapon_loaded=True)
    _combat_actions.add_condition('arm',
                                  weapon_loaded=True,
                                  weapon_armed=False)
    _combat_actions.add_reaction('arm', weapon_armed=True)
    _combat_actions.add_condition('shoot',
                                  weapon_loaded=True,
                                  weapon_armed=True,
                                  is_near=True)
    _combat_actions.add_reaction('shoot', in_engagement=False)
    _combat_actions.add_condition('get_cover', in_cover=False)
    _combat_actions.add_reaction('get_cover', in_cover=True)
    _combat_actions.set_weight('unpack_ammo', 3)
    _combat_actions.set_weight('search_for_ammo', 4)
    _combat_actions.set_weight('track', 20)

    _combat_brain.set_action_list(_combat_actions)

    _food_brain = Planner('is_hungry',
                          'has_food')
    _food_actions = Action_List()

    _food_brain.set_action_list(_food_actions)
    _food_brain.set_start_state(has_food=False,
                                is_hungry=True)
    _food_brain.set_goal_state(is_hungry=False)

    _food_actions.add_condition('find_food', has_food=False)
    _food_actions.add_reaction('find_food', has_food=True)
    _food_actions.add_condition('eat_food', has_food=True)
    _food_actions.add_reaction('eat_food', is_hungry=False)
    _food_actions.set_weight('find_food', 20)
    _food_actions.set_weight('eat_food', 10)

    _heal_brain = Planner('is_hurt',
                          'has_bandage')
    _heal_actions = Action_List()
    
    _heal_brain.set_action_list(_heal_actions)
    _heal_brain.set_start_state(has_bandage=False,
                                is_hurt=True)
    _heal_brain.set_goal_state(is_hurt=False)

    _heal_actions.add_condition('find_bandage', has_bandage=False)
    _heal_actions.add_reaction('find_bandage', has_bandage=True)
    _heal_actions.add_condition('apply_bandage', has_bandage=True)
    _heal_actions.add_reaction('apply_bandage', is_hurt=False)
    _heal_actions.set_weight('find_bandage', 15)

    _brain.add_planner(_combat_brain)
    _brain.add_planner(_food_brain)
    _brain.add_planner(_heal_brain)

    _brain.calculate()
    _brain.get_plan(debug=True)
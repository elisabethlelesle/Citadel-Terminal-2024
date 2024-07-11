import gamelib
import random
import math
import warnings
from sys import maxsize
import json

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  # Comment or remove this line to enable warnings.

        self.enhanced_strategy(game_state)

        game_state.submit_turn()

    def enhanced_strategy(self, game_state):
        """
        Combined defensive and offensive strategy.
        """
        if game_state.turn_number == 0:
            self.build_initial_defences(game_state)
        else:
            self.build_reactive_defense(game_state)
        
        if game_state.turn_number < 5:
            self.stall_with_interceptors(game_state)
        else:
            self.adaptive_offense(game_state)

    def build_initial_defences(self, game_state):
        """
        Improved initial defense setup with parameterized locations.
        """
        turret_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        game_state.attempt_spawn(TURRET, turret_locations)
        
        wall_locations = [[0, 12], [27, 12], [8, 12], [19, 12], [13, 12], [14, 12]]
        game_state.attempt_spawn(WALL, wall_locations)
        game_state.attempt_upgrade(wall_locations)

        extra_wall_locations = [[1, 13], [26, 13], [7, 12], [20, 12], [12, 11], [15, 11]]
        game_state.attempt_spawn(WALL, extra_wall_locations)
        game_state.attempt_upgrade(extra_wall_locations)

        support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
        game_state.attempt_spawn(SUPPORT, support_locations)
        game_state.attempt_upgrade(support_locations)

    def build_reactive_defense(self, game_state):
        """
        Improved reactive defenses based on enemy scoring.
        """
        for location in self.scored_on_locations:
            build_location = [location[0], location[1] + 1]
            game_state.attempt_spawn(TURRET, build_location)
            game_state.attempt_spawn(WALL, [location[0], location[1]])
            game_state.attempt_upgrade([location[0], location[1]])

    def stall_with_interceptors(self, game_state):
        """
        Early game interceptor stalling tactic.
        """
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)

    def adaptive_offense(self, game_state):
        """
        Adaptive offensive strategy based on enemy defense analysis.
        """
        if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
            self.demolisher_line_strategy(game_state)
        else:
            if game_state.turn_number % 2 == 1:
                scout_spawn_location_options = [[13, 0], [14, 0]]
                best_location = self.least_damage_spawn_location(game_state, scout_spawn_location_options)
                if best_location:
                    game_state.attempt_spawn(SCOUT, best_location, 1000)

            support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
            game_state.attempt_spawn(SUPPORT, support_locations)
            game_state.attempt_upgrade(support_locations)

    def demolisher_line_strategy(self, game_state):
        """
        Demolisher line strategy for concentrated attacks.
        """
        cheapest_unit = WALL
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        Determine the safest spawn location for scouts.
        """
        damages = []
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            if path:
                damage = 0
                for path_location in path:
                    damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
                damages.append(damage)
            else:
                damages.append(float('inf'))
        
        return location_options[damages.index(min(damages))] if damages else None

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        Processing the action frames to track enemy scoring locations.
        """
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()

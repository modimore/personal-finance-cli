class ActionRouter:
    def __init__(self, switch_attr, default_action=None):
        self._actions = {}
        self._default_action = default_action
        self._switch_attr = switch_attr
    
    def register(self, action_name, action):
        self._actions[action_name] = action
    
    def register_subrouter(self, action_name, switch_attr, default_action=None):
        subrouter = ActionRouter(switch_attr, default_action)
        self._actions[action_name] = subrouter.route
        return subrouter
    
    def route(self, args):
        try:
            action = self._actions[getattr(args, self._switch_attr)]
        except KeyError:
            action = self._default_action
        action(args)

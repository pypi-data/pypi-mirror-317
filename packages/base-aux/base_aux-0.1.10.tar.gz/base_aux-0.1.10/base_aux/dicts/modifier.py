from typing import *


# =====================================================================================================================
class Dicts(dict):  # use name *s to not mess with typing.Dict
    """
    just a class which keep all meths for dicts
    """
    def collapse_key(self, key: Any, source: dict = None) -> dict:
        """
        GOAL
        ----
        specially created for 2level-dicts (when values could be a dict)
        so it would replace values (if they are dicts and have special_key)

        CONSTRAINTS
        -----------
        it means that you have similar dicts with same exact keys
            {
                0: 0,
                1: {1:1, 2:2, 3:3},
                2: {1:11, 2:22, 3:33},
                3: {1:111, 2:222, 3:333},
                4: 4,
            }
        and want to get special slice like result

        SPECIALLY CREATED FOR
        ---------------------
        testplans get results for special dut from all results


        main idia to use values like dicts as variety and we can select now exact composition! remain other values without variants

        EXAMPLES
        --------
        dicts like
            {
                1: {1:1, 2:2, 3:3},
                2: {1:1, 2:None},
                3: {1:1},
                4: 4,
            }
        for key=2 return
            {
                1: 2,
                2: None,
                3: None,
                4: 4,
            }

        """
        result = {}
        if source is None:
            source = self

        for root_key, root_value in source.items():
            if isinstance(root_value, dict) and key in root_value:
                root_value = root_value.get(key)

            result[root_key] = root_value

        return result

    def prepare_serialisation(self, source: dict = None) -> dict:
        result = {}
        if source is None:
            source = self
        pass





        
        return result


# =====================================================================================================================

import grading_enums as enums
class ProblemInfo:
    def __init__(self, problem_name):
        self._problem_name = str(problem_name)
        self._time_limit = 1000
        self._memory_limit = 128
        self._validation_mode = enums.ValidationMode.DEFAULT

    def get_problem_name(self):
        return self._problem_name

    def set_time_limit(self, time_limit):
        assert(isinstance(time_limit, int))
        self._time_limit = time_limit

    def get_time_limit(self):
        return self._time_limit

    def set_memory_limit(self, memory_limit):
        assert(isinstance(memory_limit, int))
        self._memory_limit = memory_limit

    def get_memory_limit(self):
        return self._memory_limit

    def set_validation_mode(self, validation_mode):
        assert(isinstance(validation_mode, enums.ValidationMode))
        self._validation_mode = validation_mode

    def get_validation_mode(self):
        return self._validation_mode
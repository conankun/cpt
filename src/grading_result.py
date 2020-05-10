import grading_enums as enums
class GradingResult:
    def __init__(self):
        pass
    def set_grading_status(self, grading_status):
        assert(isinstance(grading_status, enums.GradingStatus))
        self._grading_status = grading_status
    def get_grading_status(self):
        return self._grading_status
    def set_time_elapsed(self, time_elapsed):
        assert(isinstance(time_elapsed, int))
        self._time_elapsed = time_elapsed
    def get_time_elapsed(self):
        return self._time_elapsed
    def set_memory_used(self, memory_used):
        assert(isinstance(memory_used, int))
        self._memory_used = memory_used
    def get_memory_used(self):
        return self._memory_used
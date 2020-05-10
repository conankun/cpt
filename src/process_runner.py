import grading_enums as enums
import grading_result as gr
import problem_info as pi
import submission_info as si
import util as util
import os
import subprocess
import time

class ProcessRunner:
    def __init__(self, problem_info, submission_info, testcase_names):
        self._problem_info = problem_info
        self._submission_info = submission_info
        self._sandbox_dir = os.path.join("/", "app", "sandbox", str(self._problem_info.get_problem_name()))
        self._filename = "main"
        self._grading_result = []
        self._testcase_names = testcase_names

    def _prepare(self):
        pass

    def _compile(self, options):
        p = subprocess.Popen(options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            outs, errs = p.communicate(timeout=100)
            return {'returncode': p.returncode, 'outs': outs, 'errs': errs}
        except subprocess.TimeoutExpired:
            p.kill()
            # TODO(conankun): inform the client that compile failed due to timeout

    def compile(self):
        options = util.find_compile_option(
            self._submission_info.getLang(), os.path.join(self._sandbox_dir, self._filename))
        compile_result = self._compile(options)
        if compile_result['returncode'] != 0:
            self._grading_result.append(gr.GradingResult().set_grading_status(enums.GradingStatus.COMPILE_ERROR))

        return {
            'compile_status': compile_result['returncode'] == 0,
            'compile_log': compile_result['outs'],
            'compile_error_log': compile_result['errs']
        }

    def _run_testcase(self, testcase_file_name, grading_result):
        options = util.find_execution_option(self._submission_info.getLang(),
                                        os.path.join(self._sandbox_dir, self._filename))
        # Run the code.
        input_file = open(
            os.path.join("/app", "data", self._problem_info.get_problem_name(), testcase_file_name) + ".in")
        grading_result.set_grading_status(enums.GradingStatus.PENDING)
        # Start the process.
        start_time = time.time()
        subprocess.Popen(options)
        p = subprocess.Popen(options,
                             stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_mxrss = 0
        while p.poll() == None:
            # While the process is running, check the memory limit.
            # Also check time elapsed and terminate the process if
            # process is running longer than its time limit.
            end_time = time.time()
            if int((end_time - start_time) * 1000) > self._problem_info.get_time_limit():
                # Time Limit Exceeded.
                grading_result.set_grading_status(enums.GradingStatus.TIME_LIMIT_EXCEEDED)
                grading_result.set_time_elapsed(self._problem_info.get_time_limit())
                grading_result.set_memory_used(p_mxrss)
                p.stdout.close()
                p.stderr.close()
                input_file.close()
                p.kill()
                break
            peak_memory_used = util.get_current_memory_usage(p.pid)
            if peak_memory_used != None:
                p_mxrss = max(p_mxrss, peak_memory_used)
            # Assumption: p_mxrss is the maximum memory used
            # in KB (UNIX only).
            if p_mxrss > self._problem_info.get_memory_limit() << 10:
                # Memory Limit Exceeded.
                grading_result.set_grading_status(enums.GradingStatus.MEMORY_LIMIT_EXCEEDED)
                grading_result.set_time_elapsed(int((end_time - start_time) * 1000))
                grading_result.set_memory_used(p_mxrss)
                p.stdout.close()
                p.stderr.close()
                input_file.close()
                p.kill()
                break

        if grading_result.get_grading_status() == enums.GradingStatus.PENDING:
            # When not TLE.
            outs, errs = p.communicate()
            end_time = time.time()
            # Convert to milisecond.
            grading_result.set_time_elapsed(int((end_time - start_time) * 1000))
            # Fill out grading result.
            if p.returncode != 0:
                grading_result.set_grading_status(enums.GradingStatus.RUN_TIME_ERROR)
            # Max memory used in KB (UNIX)
            grading_result.set_memory_used(p_mxrss)
            input_file.close()
            return {'outs': outs.decode(), 'errs': errs.decode()}
        return None

    def _validate(self, testcase_file_name, user_output, grading_result):
        grading_mode = self._problem_info.get_validation_mode()
        status = grading_result.get_grading_status()

        if status != enums.GradingStatus.PENDING:
            raise Exception('Cannot run validation when grading status is not pending.')
        # Read golden output file (a.k.a answer).
        problem_path = os.path.join(
                "/app",
                "data",
                self._problem_info.get_problem_name(),
                str(testcase_file_name))
        golden_output_file_path = problem_path + ".out"
        golden_output_file = open(golden_output_file_path)
        golden_outputs = golden_output_file.readlines()
        golden_output_file.close()
        # Read output file from grading_info
        print("user output: " + str(user_output.split('\n')))
        print("golden output: " + str(golden_outputs))
        outputs = user_output.split('\n')

        if grading_mode == enums.ValidationMode.DEFAULT:
            # Grading mode that ignores spaces.
            if len(golden_outputs) != len(outputs):
                return False
            # Not using enumerate or zip due to performance concern.
            for idx in range(len(golden_outputs)):
                golden_outputs_segments = golden_outputs[idx].split(' ')
                outputs_segment = outputs[idx].split(' ')
                if len(golden_outputs_segments) != len(outputs_segment):
                    return False
                for i in range(len(golden_outputs_segments)):
                    if golden_outputs_segments[i] != outputs_segment[i]:
                        return False
            return True
        elif grading_mode == enums.ValidationMode.EXACT:
            # Grading mode that do not ignore spaces.
            if len(golden_outputs) != len(outputs):
                return False
            # Not using enumerate or zip due to performance concern.
            idx = 0
            for golden_outputs_line in golden_outputs:
                if golden_outputs_line != outputs[idx]:
                    return False
                idx = idx + 1
            return True

    def validate(self, test_case_file_name, user_output, grading_result):
        result = self._validate(test_case_file_name, user_output, grading_result)
        if result:
            grading_result.set_grading_status(enums.GradingStatus.SUCCESS)
        else:
            grading_result.set_grading_status(enums.GradingStatus.WRONG)

    def run(self):
        compile_res = self.compile()
        print("Compile Log:\n" + str(compile_res['compile_log']) + "\nError: " + str(compile_res["compile_error_log"]))
        if compile_res['compile_status'] == False:
            print("Compile Failed.")
            return
        for testcase_name in self._testcase_names:
            self._grading_result.append(gr.GradingResult())
            grading_result = self._grading_result[len(self._grading_result) - 1]
            user_output = self._run_testcase(testcase_name, grading_result)['outs']
            if grading_result.get_grading_status() == enums.GradingStatus.PENDING:
                self.validate(testcase_name, user_output, grading_result)
                if grading_result.get_grading_status() == enums.GradingStatus.SUCCESS:
                    print("Success!")
                else:
                    print("Wrong")
            if grading_result.get_grading_status() == enums.GradingStatus.TIME_LIMIT_EXCEEDED:
                print("TLE!")
            elif grading_result.get_grading_status() == enums.GradingStatus.MEMORY_LIMIT_EXCEEDED:
                print("MLE!")
            elif grading_result.get_grading_status() == enums.GradingStatus.RUN_TIME_ERROR:
                print("RTE!")


if __name__ == "__main__":
    problem_info = pi.ProblemInfo("1000")
    submission_info = si.SubmissionInfo("C++17")
    testcase_names = ["1", "2", "3", "4", "5"]
    pr = ProcessRunner(problem_info, submission_info, testcase_names)
    pr.run()
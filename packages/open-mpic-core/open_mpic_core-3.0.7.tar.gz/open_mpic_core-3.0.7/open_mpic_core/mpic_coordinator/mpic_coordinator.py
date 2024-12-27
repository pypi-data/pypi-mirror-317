import json
import traceback
from itertools import cycle

import time
import concurrent.futures
from datetime import datetime
import hashlib

from open_mpic_core.common_domain.check_response import CaaCheckResponse, CaaCheckResponseDetails, DcvCheckResponse
from open_mpic_core.common_domain.check_request import CaaCheckRequest, DcvCheckRequest
from open_mpic_core.common_domain.check_response_details import DcvCheckResponseDetailsBuilder
from open_mpic_core.common_domain.validation_error import MpicValidationError
from open_mpic_core.common_domain.enum.check_type import CheckType
from open_mpic_core.common_domain.messages.ErrorMessages import ErrorMessages
from open_mpic_core.mpic_coordinator.cohort_creator import CohortCreator
from open_mpic_core.mpic_coordinator.domain.mpic_request import MpicCaaRequest, MpicRequest, MpicDcvRequest
from open_mpic_core.mpic_coordinator.domain.mpic_request_validation_error import MpicRequestValidationError
from open_mpic_core.mpic_coordinator.domain.mpic_response import MpicResponse
from open_mpic_core.mpic_coordinator.domain.remote_check_call_configuration import RemoteCheckCallConfiguration
from open_mpic_core.mpic_coordinator.domain.remote_perspective import RemotePerspective
from open_mpic_core.mpic_coordinator.messages.mpic_request_validation_messages import MpicRequestValidationMessages
from open_mpic_core.mpic_coordinator.mpic_request_validator import MpicRequestValidator
from open_mpic_core.mpic_coordinator.mpic_response_builder import MpicResponseBuilder


class MpicCoordinatorConfiguration:
    def __init__(self, target_perspectives, default_perspective_count, global_max_attempts, hash_secret):
        self.target_perspectives = target_perspectives
        self.default_perspective_count = default_perspective_count
        self.global_max_attempts = global_max_attempts
        self.hash_secret = hash_secret


class MpicCoordinator:
    # call_remote_perspective_function: a "dumb" transport for serialized data to a remote perspective and a serialized response from the remote perspective. MPIC Coordinator is tasked with ensuring the data from this function is sane and handling the serialization/deserialization of the data. This function may raise an exception if something goes wrong.
    def __init__(self, call_remote_perspective_function, mpic_coordinator_configuration: MpicCoordinatorConfiguration):
        self.target_perspectives = mpic_coordinator_configuration.target_perspectives
        self.default_perspective_count = mpic_coordinator_configuration.default_perspective_count
        self.global_max_attempts = mpic_coordinator_configuration.global_max_attempts
        self.hash_secret = mpic_coordinator_configuration.hash_secret
        self.call_remote_perspective_function = call_remote_perspective_function

    def coordinate_mpic(self, mpic_request: MpicRequest) -> MpicResponse:
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(mpic_request, self.target_perspectives)

        if not is_request_valid:
            error = MpicRequestValidationError(MpicRequestValidationMessages.REQUEST_VALIDATION_FAILED.key)
            validation_issues_as_string = json.dumps([vars(issue) for issue in validation_issues])
            error.add_note(validation_issues_as_string)
            raise error

        orchestration_parameters = mpic_request.orchestration_parameters

        perspective_count = self.default_perspective_count
        if orchestration_parameters is not None and orchestration_parameters.perspective_count is not None:
            perspective_count = orchestration_parameters.perspective_count

        perspective_cohorts = self.create_cohorts_of_randomly_selected_perspectives(self.target_perspectives,
                                                                                    perspective_count,
                                                                                    mpic_request.domain_or_ip_target)

        quorum_count = self.determine_required_quorum_count(orchestration_parameters, perspective_count)

        if orchestration_parameters is not None and orchestration_parameters.max_attempts is not None:
            max_attempts = orchestration_parameters.max_attempts
            if self.global_max_attempts is not None and max_attempts > self.global_max_attempts:
                max_attempts = self.global_max_attempts
        else:
            max_attempts = 1
        attempts = 1
        previous_attempt_results = None
        cohort_cycle = cycle(perspective_cohorts)
        while attempts <= max_attempts:
            perspectives_to_use = next(cohort_cycle)

            # Collect async calls to invoke for each perspective.
            async_calls_to_issue = MpicCoordinator.collect_async_calls_to_issue(mpic_request, perspectives_to_use)

            perspective_responses, validity_per_perspective = (
                self.issue_async_calls_and_collect_responses(perspectives_to_use, async_calls_to_issue))

            valid_perspective_count = sum(validity_per_perspective.values())
            is_valid_result = valid_perspective_count >= quorum_count

            if is_valid_result or attempts == max_attempts:
                response = MpicResponseBuilder.build_response(mpic_request, perspective_count, quorum_count, attempts,
                                                              perspective_responses, is_valid_result, previous_attempt_results)
                return response
            else:
                if previous_attempt_results is None:
                    previous_attempt_results = []
                previous_attempt_results.append(perspective_responses)
                attempts += 1

    # Returns a random subset of perspectives with a goal of maximum RIR diversity to increase diversity.
    # Perspectives must be of the form 'RIR.AWS-region'.
    def create_cohorts_of_randomly_selected_perspectives(self, target_perspectives, count, domain_or_ip_target):
        if count > len(target_perspectives):
            raise ValueError(
                f"Count ({count}) must be <= the number of available perspectives ({len(target_perspectives)})")

        random_seed = hashlib.sha256((self.hash_secret + domain_or_ip_target.lower()).encode('ASCII')).digest()
        perspectives_per_rir = CohortCreator.build_randomly_shuffled_available_perspectives_per_rir(target_perspectives, random_seed)
        cohorts = CohortCreator.create_perspective_cohorts(perspectives_per_rir, count)
        return cohorts

    # Determines the minimum required quorum size if none is specified in the request.
    @staticmethod
    def determine_required_quorum_count(orchestration_parameters, perspective_count):
        if orchestration_parameters is not None and orchestration_parameters.quorum_count is not None:
            required_quorum_count = orchestration_parameters.quorum_count
        else:
            required_quorum_count = perspective_count - 1 if perspective_count <= 5 else perspective_count - 2
        return required_quorum_count

    # Configures the async remote perspective calls to issue for the check request.
    @staticmethod
    def collect_async_calls_to_issue(mpic_request, perspectives_to_use: list[RemotePerspective]) -> list[RemoteCheckCallConfiguration]:
        domain_or_ip_target = mpic_request.domain_or_ip_target
        async_calls_to_issue = []

        # check if mpic_request is an instance of MpicCaaRequest or MpicDcvRequest
        if isinstance(mpic_request, MpicCaaRequest):
            check_parameters = CaaCheckRequest(domain_or_ip_target=domain_or_ip_target, caa_check_parameters=mpic_request.caa_check_parameters)
            for perspective in perspectives_to_use:
                call_config = RemoteCheckCallConfiguration(CheckType.CAA, perspective, check_parameters)
                async_calls_to_issue.append(call_config)

        elif isinstance(mpic_request, MpicDcvRequest):
            check_parameters = DcvCheckRequest(domain_or_ip_target=domain_or_ip_target, dcv_check_parameters=mpic_request.dcv_check_parameters)
            for perspective in perspectives_to_use:
                call_config = RemoteCheckCallConfiguration(CheckType.DCV, perspective, check_parameters)
                async_calls_to_issue.append(call_config)

        return async_calls_to_issue

    # Issues the async calls to the remote perspectives and collects the responses.
    def issue_async_calls_and_collect_responses(self, perspectives_to_use, async_calls_to_issue) -> tuple[list, dict]:
        perspective_responses = []
        validity_per_perspective = {perspective.code: False for perspective in perspectives_to_use}

        perspective_count = len(perspectives_to_use)

        # example code: https://docs.python.org/3/library/concurrent.futures.html
        with concurrent.futures.ThreadPoolExecutor(max_workers=perspective_count) as executor:
            # exec_begin = time.perf_counter()
            futures_to_call_configs = {executor.submit(self.call_remote_perspective, self.call_remote_perspective_function, call_config): call_config
                                       for call_config in async_calls_to_issue}
            for future in concurrent.futures.as_completed(futures_to_call_configs):
                call_configuration = futures_to_call_configs[future]
                perspective: RemotePerspective = call_configuration.perspective
                now = time.perf_counter()
                # print(f"Unpacking future result for {perspective.code} at time {str(datetime.now())}: {now - exec_begin:.2f} seconds from beginning")
                try:
                    check_response = future.result()  # expecting a CheckResponse object
                    validity_per_perspective[perspective.code] |= check_response.check_passed
                    # TODO make sure responses per perspective match API spec...
                    perspective_responses.append(check_response)
                except Exception:  # TODO what exceptions are we expecting here?
                    print(traceback.format_exc())
                    match call_configuration.check_type:
                        case CheckType.CAA:
                            check_error_response = CaaCheckResponse(
                                perspective_code=perspective.code,
                                check_passed=False,
                                errors=[MpicValidationError(error_type=ErrorMessages.COORDINATOR_COMMUNICATION_ERROR.key,
                                                            error_message=ErrorMessages.COORDINATOR_COMMUNICATION_ERROR.message)],
                                details=CaaCheckResponseDetails(caa_record_present=False),  # TODO Possibly should None to indicate the lookup failed.
                                timestamp_ns=time.time_ns()
                            )
                        case CheckType.DCV:
                            dcv_check_request: DcvCheckRequest = call_configuration.check_request
                            validation_method = dcv_check_request.dcv_check_parameters.validation_details.validation_method
                            check_error_response = DcvCheckResponse(
                                perspective_code=perspective.code,
                                check_passed=False,
                                errors=[MpicValidationError(error_type=ErrorMessages.COORDINATOR_COMMUNICATION_ERROR.key,
                                                            error_message=ErrorMessages.COORDINATOR_COMMUNICATION_ERROR.message)],
                                details=DcvCheckResponseDetailsBuilder.build_response_details(validation_method),  # TODO what should go here in this case?
                                timestamp_ns=time.time_ns()
                            )
                    validity_per_perspective[perspective.code] |= check_error_response.check_passed
                    perspective_responses.append(check_error_response)
        return perspective_responses, validity_per_perspective

    @staticmethod
    def call_remote_perspective(call_remote_perspective_function, call_config: RemoteCheckCallConfiguration):
        """
        Issues a call to a remote perspective in a separate thread. This is a blocking call.
        :param call_remote_perspective_function: function to call with arguments in call_config
        :param call_config: object containing arguments to pass to the remote function call
        :return:
        """
        print(f"Started remote perspective call for perspective {call_config.perspective} at {str(datetime.now())}")
        tic = time.perf_counter()
        response = call_remote_perspective_function(call_config.perspective, call_config.check_type, call_config.check_request)
        toc = time.perf_counter()

        print(f"Response in region {call_config.perspective.code} took {toc - tic:0.4f} seconds to get response; \
              ended at {str(datetime.now())}\n")
        return response

class StatusCodes():
    # Informational 1xx:
    def continue_100(custom_message=None):
        message = custom_message if custom_message else "Continue with the request body."
        response = {
            "status": 100,
            "message": message
        }
        return response

    def switching_protocols_101(custom_message=None):
        message = custom_message if custom_message else "Protocol switch initiated."
        response = {
            "status": 101,
            "message": message
        }
        return response

    def processing_102(custom_message=None):
        message = custom_message if custom_message else "Request is being processed."
        response = {
            "status": 102,
            "message": message
        }
        return response

    def early_hints_103(custom_message=None):
        message = custom_message if custom_message else "Early hints provided."
        response = {
            "status": 103,
            "message": message
        }
        return response

    # Successful 2xx:
    def ok_200(custom_message=None):
        message = custom_message if custom_message else "Request succeeded."
        response = {
            "status": 200,
            "message": message
        }
        return response

    def created_201(custom_message=None):
        message = custom_message if custom_message else "Resource created."
        response = {
            "status": 201,
            "message": message
        }
        return response

    def accepted_202(custom_message=None):
        message = custom_message if custom_message else "Request accepted, processing."
        response = {
            "status": 202,
            "message": message
        }
        return response

    def non_authoritative_information_203(custom_message=None):
        message = custom_message if custom_message else "Non-authoritative information."
        response = {
            "status": 203,
            "message": message
        }
        return response

    def no_content_204(custom_message=None):
        message = custom_message if custom_message else "No content to return."
        response = {
            "status": 204,
            "message": message
        }
        return response

    def reset_content_205(custom_message=None):
        message = custom_message if custom_message else "Content reset required."
        response = {
            "status": 205,
            "message": message
        }
        return response

    def partial_content_206(custom_message=None):
        message = custom_message if custom_message else "Partial content returned."
        response = {
            "status": 206,
            "message": message
        }
        return response

    def multi_status_207(custom_message=None):
        message = custom_message if custom_message else "Multiple statuses."
        response = {
            "status": 207,
            "message": message
        }
        return response

    def already_reported_208(custom_message=None):
        message = custom_message if custom_message else "Already reported."
        response = {
            "status": 208,
            "message": message
        }
        return response

    def im_used_226(custom_message=None):
        message = custom_message if custom_message else "IM used."
        response = {
            "status": 226,
            "message": message
        }
        return response

    # Redirection 3xx:
    def multiple_choices_300(custom_message=None):
        message = custom_message if custom_message else "Multiple choices available."
        response = {
            "status": 300,
            "message": message
        }
        return response

    def moved_permanently_301(custom_message=None):
        message = custom_message if custom_message else "Resource permanently moved."
        response = {
            "status": 301,
            "message": message
        }
        return response

    def found_302(custom_message=None):
        message = custom_message if custom_message else "Resource found at another location."
        response = {
            "status": 302,
            "message": message
        }
        return response

    def see_other_303(custom_message=None):
        message = custom_message if custom_message else "See other location."
        response = {
            "status": 303,
            "message": message
        }
        return response

    def not_modified_304(custom_message=None):
        message = custom_message if custom_message else "Not modified."
        response = {
            "status": 304,
            "message": message
        }
        return response

    def use_proxy_305(custom_message=None):
        message = custom_message if custom_message else "Use proxy."
        response = {
            "status": 305,
            "message": message
        }
        return response

    def use_proxy_306(custom_message=None):
        message = custom_message if custom_message else "Unused."
        response = {
            "status": 306,
            "message": message
        }
        return response

    def temporary_redirect_307(custom_message=None):
        message = custom_message if custom_message else "Temporary redirect."
        response = {
            "status": 307,
            "message": message
        }
        return response

    def permanent_redirect_308(custom_message=None):
        message = custom_message if custom_message else "Permanent redirect."
        response = {
            "status": 308,
            "message": message
        }
        return response

    # Client Error 4xx:
    def bad_request_400(custom_message=None):
        message = custom_message if custom_message else "Bad request syntax."
        response = {
            "status": 400,
            "message": message
        }
        return response

    def unauthorized_401(custom_message=None):
        message = custom_message if custom_message else "Authentication required."
        response = {
            "status": 401,
            "message": message
        }
        return response

    def payment_required_402(custom_message=None):
        message = custom_message if custom_message else "Payment required."
        response = {
            "status": 402,
            "message": message
        }
        return response

    def forbidden_403(custom_message=None):
        message = custom_message if custom_message else "Forbidden access."
        response = {
            "status": 403,
            "message": message
        }
        return response

    def not_found_404(custom_message=None):
        message = custom_message if custom_message else "Resource not found."
        response = {
            "status": 404,
            "message": message
        }
        return response

    def method_not_allowed_405(custom_message=None):
        message = custom_message if custom_message else "Method not allowed."
        response = {
            "status": 405,
            "message": message
        }
        return response

    def not_acceptable_406(custom_message=None):
        message = custom_message if custom_message else "Not acceptable."
        response = {
            "status": 406,
            "message": message
        }
        return response

    def proxy_authentication_required_407(custom_message=None):
        message = custom_message if custom_message else "Proxy authentication required."
        response = {
            "status": 407,
            "message": message
        }
        return response

    def request_timeout_408(custom_message=None):
        message = custom_message if custom_message else "Request timeout."
        response = {
            "status": 408,
            "message": message
        }
        return response

    def conflict_409(custom_message=None):
        message = custom_message if custom_message else "Request conflict."
        response = {
            "status": 409,
            "message": message
        }
        return response

    def gone_410(custom_message=None):
        message = custom_message if custom_message else "Resource gone."
        response = {
            "status": 410,
            "message": message
        }
        return response

    def length_required_411(custom_message=None):
        message = custom_message if custom_message else "Length required."
        response = {
            "status": 411,
            "message": message
        }
        return response

    def precondition_failed_412(custom_message=None):
        message = custom_message if custom_message else "Precondition failed."
        response = {
            "status": 412,
            "message": message
        }
        return response

    def payload_too_large_413(custom_message=None):
        message = custom_message if custom_message else "Payload too large."
        response = {
            "status": 413,
            "message": message
        }
        return response

    def uri_too_long_414(custom_message=None):
        message = custom_message if custom_message else "URI too long."
        response = {
            "status": 414,
            "message": message
        }
        return response

    def unsupported_media_type_415(custom_message=None):
        message = custom_message if custom_message else "Unsupported media type."
        response = {
            "status": 415,
            "message": message
        }
        return response

    def range_not_satisfiable_416(custom_message=None):
        message = custom_message if custom_message else "Range not satisfiable."
        response = {
            "status": 416,
            "message": message
        }
        return response

    def expectation_failed_417(custom_message=None):
        message = custom_message if custom_message else "Expectation failed."
        response = {
            "status": 417,
            "message": message
        }
        return response

    def im_a_teapot_418(custom_message=None):
        message = custom_message if custom_message else "I'm a teapot. (Joke)"
        response = {
            "status": 418,
            "message": message
        }
        return response

    def misdirected_request_421(custom_message=None):
        message = custom_message if custom_message else "Misdirected request."
        response = {
            "status": 421,
            "message": message
        }
        return response

    def unprocessable_content_422(custom_message=None):
        message = custom_message if custom_message else "Unprocessable content."
        response = {
            "status": 422,
            "message": message
        }
        return response

    def locked_423(custom_message=None):
        message = custom_message if custom_message else "Locked."
        response = {
            "status": 423,
            "message": message
        }
        return response

    def failed_dependency_424(custom_message=None):
        message = custom_message if custom_message else "Failed dependency."
        response = {
            "status": 424,
            "message": message
        }
        return response

    def too_early_425(custom_message=None):
        message = custom_message if custom_message else "Too early."
        response = {
            "status": 425,
            "message": message
        }
        return response

    def upgrade_required_426(custom_message=None):
        message = custom_message if custom_message else "Upgrade required."
        response = {
            "status": 426,
            "message": message
        }
        return response


    def precondition_required_428(custom_message=None):
        message = custom_message if custom_message else "Precondition required."
        response = {
            "status": 428,
            "message": message
        }
        return response

    def too_many_requests_429(custom_message=None):
        message = custom_message if custom_message else "Too many requests."
        response = {
            "status": 429,
            "message": message
        }
        return response

    def request_header_fields_too_large_431(custom_message=None):
        message = custom_message if custom_message else "Header fields too large."
        response = {
            "status": 431,
            "message": message
        }
        return response

    def unavailable_for_legal_reasons_451(custom_message=None):
        message = custom_message if custom_message else "Unavailable for legal reasons."
        response = {
            "status": 451,
            "message": message
        }
        return response

    # Server Error 5xx:
    def internal_server_error_500(custom_message=None):
        message = custom_message if custom_message else "Internal Server error."
        response = {
            "status": 500,
            "message": message
        }
        return response

    def not_implemented_501(custom_message=None):
        message = custom_message if custom_message else "Not implemented."
        response = {
            "status": 501,
            "message": message
        }
        return response

    def bad_gateway_502(custom_message=None):
        message = custom_message if custom_message else "Bad gateway."
        response = {
            "status": 502,
            "message": message
        }
        return response

    def service_unavailable_503(custom_message=None):
        message = custom_message if custom_message else "Service unavailable."
        response = {
            "status": 503,
            "message": message
        }
        return response

    def gateway_timeout_504(custom_message=None):
        message = custom_message if custom_message else "Gateway timeout."
        response = {
            "status": 504,
            "message": message
        }
        return response

    def http_version_not_supported_505(custom_message=None):
        message = custom_message if custom_message else "HTTP version not supported."
        response = {
            "status": 505,
            "message": message
        }
        return response

    def variant_also_negotiates_506(custom_message=None):
        message = custom_message if custom_message else "Variant also negotiates."
        response = {
            "status": 506,
            "message": message
        }
        return response

    def insufficient_storage_507(custom_message=None):
        message = custom_message if custom_message else "Insufficient storage."
        response = {
            "status": 507,
            "message": message
        }
        return response

    def loop_detected_508(custom_message=None):
        message = custom_message if custom_message else "Loop detected."
        response = {
            "status": 508,
            "message": message
        }
        return response

    def not_extended_510(custom_message=None):
        message = custom_message if custom_message else "Not extended."
        response = {
            "status": 510,
            "message": message
        }
        return response

    def network_authentication_required_511(custom_message=None):
        message = custom_message if custom_message else "Network authentication required."
        response = {
            "status": 511,
            "message": message
        }
        return response

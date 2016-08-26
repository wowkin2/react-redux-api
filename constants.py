class HttpStatus:
    OK = 200
    CREATED = 201  # 201 (Created), 'Location' header with link to /object/{id} containing new ID.
    NO_CONTENT = 204  # success but no response, after object deletion

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409  # if resource already exists

    INTERNAL_SERVER_ERROR = 500

EMPTY_RESPONSE = ''
EMPTY_JSON = {}

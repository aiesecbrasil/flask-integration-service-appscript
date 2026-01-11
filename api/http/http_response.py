from enum import IntEnum
from ..globals import jsonify, Response


class HttpStatus(IntEnum):
    OK = 200
    CREATED = 201
    NON_AUTHORITATIVE = 203
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_ERROR = 500
    MOVED_PERMANENTLY = 301
    FOUND = 302


class HttpResponse:
    @staticmethod
    def respond(
        data=None,
        status: HttpStatus = HttpStatus.OK
    ) -> tuple[Response, int]:
        return jsonify(data or {}), int(status)

    @staticmethod
    def ok(data=None) -> tuple[Response, int]:
        return HttpResponse.respond(data, HttpStatus.OK)

    @staticmethod
    def created(data=None) -> tuple[Response, int]:
        return HttpResponse.respond(data, HttpStatus.CREATED)

    @staticmethod
    def non_authoritative(data=None) -> tuple[Response, int]:
        return HttpResponse.respond(data, HttpStatus.NON_AUTHORITATIVE)

    @staticmethod
    def bad_request(message: str) -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.BAD_REQUEST
        )

    @staticmethod
    def unauthorized(message: str = "Não autorizado") -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.UNAUTHORIZED
        )

    @staticmethod
    def forbidden(message: str = "Acesso proibido") -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.FORBIDDEN
        )

    @staticmethod
    def not_found(message: str) -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.NOT_FOUND
        )

    @staticmethod
    def conflict(message: str) -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.CONFLICT
        )

    @staticmethod
    def internal_error(message: str = "Erro interno") -> tuple[Response, int]:
        return HttpResponse.respond(
            {"error": message},
            HttpStatus.INTERNAL_ERROR
        )

    @staticmethod
    def redirect_permanent(url: str) -> tuple[Response, int]:
        """Redirecionamento permanente (301)"""
        return jsonify({"redirect": url}), HttpStatus.MOVED_PERMANENTLY

    @staticmethod
    def redirect_temporary(url: str) -> tuple[Response, int]:
        """Redirecionamento temporário (302)"""
        return jsonify({"redirect": url}), HttpStatus.FOUND

__all__ = ["HttpResponse"]
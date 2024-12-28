from enum import Enum
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from fastapi3 import routing
from fastapi3.datastructures import Default, DefaultPlaceholder
from fastapi3.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    websocket_request_validation_exception_handler,
)
from fastapi3.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi3.logger import logger
from fastapi3.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi3.openapi.utils import get_openapi
from fastapi3.params import Depends
from fastapi3.types import DecoratedCallable, IncEx
from fastapi3.utils import generate_unique_id
from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Lifespan, Receive, Scope, Send
from typing_extensions import Annotated, Doc, deprecated
from .config import default_description

AppType = TypeVar("AppType", bound="FastAPI")


class FastAPI(Starlette):
    def __init__(
            self: AppType,
            *,
            debug: bool = False,  # Boolean indicating if debug tracebacks should be returned on server errors.
            routes: Optional[List[BaseRoute]] = None,  # A list of routes to serve incoming HTTP and WebSocket requests.
            title: str = "FastAPI3: 国产化API",
            # The title of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`).
            summary: Optional[str] = "更符合中国人使用习惯的FastAPI二次开发框架",
            # A short summary of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`).
            description: str = default_description,
            version: str = "0.1.0",
            openapi_url: str = "/openapi.json",  # 如果设置为None，则禁用docs文档功能
            openapi_tags: Optional[List[Dict[str, Any]]] = None,
            servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
            dependencies: Optional[Sequence[Depends]] = None,
            default_response_class: Type[Response] = Default(JSONResponse),
            redirect_slashes: bool = True,
            docs_url: Optional[str] = "/docs",
            redoc_url: Optional[str] = "/redoc",
            swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
            swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
            middleware: Optional[Sequence[Middleware]] = None,
            exception_handlers: Optional[
                Dict[Union[int, Type[Exception]], Callable[[Request, Any], Coroutine[Any, Any, Response]]]] = None,
            on_startup: Optional[Sequence[Callable[[], Any]]] = None,
            on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
            lifespan: Optional[Lifespan[AppType]] = None,
            terms_of_service: Optional[str] = None,
            contact: Optional[Dict[str, Union[str, Any]]] = None,
            license_info: Optional[Dict[str, Union[str, Any]]] = None,
            openapi_prefix: str = "",
            root_path: str = "",
            root_path_in_servers: bool = True,
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            webhooks: Optional[routing.APIRouter] = None,
            deprecated: Optional[bool] = None,
            include_in_schema: bool = True,
            swagger_ui_parameters: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
            separate_input_output_schemas: bool = True,
            **extra: Any,
    ) -> None:
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.swagger_ui_parameters = swagger_ui_parameters
        self.servers = servers or []
        self.separate_input_output_schemas = separate_input_output_schemas
        self.extra = extra
        self.openapi_version: Annotated[
            str,
            Doc(
                """
                The version string of OpenAPI.

                FastAPI will generate OpenAPI version 3.1.0, and will output that as
                the OpenAPI version. But some tools, even though they might be
                compatible with OpenAPI 3.1.0, might not recognize it as a valid.

                So you could override this value to trick those tools into using
                the generated OpenAPI. Have in mind that this is a hack. But if you
                avoid using features added in OpenAPI 3.1.0, it might work for your
                use case.

                This is not passed as a parameter to the `FastAPI` class to avoid
                giving the false idea that FastAPI would generate a different OpenAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from fastapi3 import FastAPI

                app = FastAPI()

                app.openapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.1.0"
        self.openapi_schema: Optional[Dict[str, Any]] = None
        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        # TODO: remove when discarding the openapi_prefix parameter
        if openapi_prefix:
            logger.warning(
                '"openapi_prefix" has been deprecated in favor of "root_path", which '
                "follows more closely the ASGI standard, is simpler, and more "
                "automatic. Check the docs at "
                "https://fastapi.tiangolo.com/advanced/sub-applications/"
            )
        self.webhooks: Annotated[
            routing.APIRouter,
            Doc(
                """
                The `app.webhooks` attribute is an `APIRouter` with the *path
                operations* that will be used just for documentation of webhooks.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = webhooks or routing.APIRouter()
        self.root_path = root_path or openapi_prefix
        self.state: Annotated[
            State,
            Doc(
                """
                A state object for the application. This is the same object for the
                entire application, it doesn't change from request to request.

                You normally wouldn't use this in FastAPI, for most of the cases you
                would instead use FastAPI dependencies.

                This is simply inherited from Starlette.

                Read more about it in the
                [Starlette docs for Applications](https://www.starlette.io/applications/#storing-state-on-the-app-instance).
                """
            ),
        ] = State()
        self.dependency_overrides: Annotated[
            Dict[Callable[..., Any], Callable[..., Any]],
            Doc(
                """
                A dictionary with overrides for the dependencies.

                Each key is the original dependency callable, and the value is the
                actual dependency that should be called.

                This is for testing, to replace expensive dependencies with testing
                versions.

                Read more about it in the
                [FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
                """
            ),
        ] = {}
        self.router: routing.APIRouter = routing.APIRouter(
            routes=routes,
            redirect_slashes=redirect_slashes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            default_response_class=default_response_class,
            dependencies=dependencies,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            generate_unique_id_function=generate_unique_id_function,
        )
        self.exception_handlers: Dict[
            Any, Callable[[Request, Any], Union[Response, Awaitable[Response]]]
        ] = {} if exception_handlers is None else dict(exception_handlers)
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )
        self.exception_handlers.setdefault(
            WebSocketRequestValidationError,
            # Starlette still has incorrect type specification for the handlers
            websocket_request_validation_exception_handler,  # type: ignore
        )

        self.user_middleware: List[Middleware] = (
            [] if middleware is None else list(middleware)
        )
        self.middleware_stack: Union[ASGIApp, None] = None
        self.setup()

    def openapi(self) -> Dict[str, Any]:
        """
        Generate the OpenAPI schema of the application. This is called by FastAPI
        internally.

        The first time it is called it stores the result in the attribute
        `app.openapi_schema`, and next times it is called, it just returns that same
        result. To avoid the cost of generating the schema every time.

        If you need to modify the generated OpenAPI schema, you could modify it.

        Read more in the
        [FastAPI docs for OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/).
        """
        if not self.openapi_schema:
            self.openapi_schema = get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                summary=self.summary,
                description=self.description,
                terms_of_service=self.terms_of_service,
                contact=self.contact,
                license_info=self.license_info,
                routes=self.routes,
                webhooks=self.webhooks.routes,
                tags=self.openapi_tags,
                servers=self.servers,
                separate_input_output_schemas=self.separate_input_output_schemas,
            )
        return self.openapi_schema

    def setup(self) -> None:
        if self.openapi_url:
            urls = (server_data.get("url") for server_data in self.servers)
            server_urls = {url for url in urls if url}

            async def openapi(req: Request) -> JSONResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                if root_path not in server_urls:
                    if root_path and self.root_path_in_servers:
                        self.servers.insert(0, {"url": root_path})
                        server_urls.add(root_path)
                return JSONResponse(self.openapi())

            self.add_route(self.openapi_url, openapi, include_in_schema=False)
        if self.openapi_url and self.docs_url:

            async def swagger_ui_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                oauth2_redirect_url = self.swagger_ui_oauth2_redirect_url
                if oauth2_redirect_url:
                    oauth2_redirect_url = root_path + oauth2_redirect_url
                return get_swagger_ui_html(
                    openapi_url=openapi_url,
                    title=f"{self.title} - Swagger UI",
                    oauth2_redirect_url=oauth2_redirect_url,
                    init_oauth=self.swagger_ui_init_oauth,
                    swagger_ui_parameters=self.swagger_ui_parameters,
                )

            self.add_route(self.docs_url, swagger_ui_html, include_in_schema=False)

            if self.swagger_ui_oauth2_redirect_url:
                async def swagger_ui_redirect(req: Request) -> HTMLResponse:
                    return get_swagger_ui_oauth2_redirect_html()

                self.add_route(
                    self.swagger_ui_oauth2_redirect_url,
                    swagger_ui_redirect,
                    include_in_schema=False,
                )
        if self.openapi_url and self.redoc_url:
            async def redoc_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                return get_redoc_html(
                    openapi_url=openapi_url, title=f"{self.title} - ReDoc"
                )

            self.add_route(self.redoc_url, redoc_html, include_in_schema=False)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.root_path:
            scope["root_path"] = self.root_path
        await super().__call__(scope, receive, send)

    def add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            response_model: Any = Default(None),
            status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[Depends]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            methods: Optional[List[str]] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Union[Type[Response], DefaultPlaceholder] = Default(
                JSONResponse
            ),
            name: Optional[str] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                generate_unique_id
            ),
    ) -> None:
        self.router.add_api_route(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def api_route(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[Depends]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            methods: Optional[List[str]] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                generate_unique_id
            ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.router.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=response_model_exclude_unset,
                response_model_exclude_defaults=response_model_exclude_defaults,
                response_model_exclude_none=response_model_exclude_none,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )
            return func

        return decorator

    def add_api_websocket_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            name: Optional[str] = None,
            *,
            dependencies: Optional[Sequence[Depends]] = None,
    ) -> None:
        self.router.add_api_websocket_route(
            path,
            endpoint,
            name=name,
            dependencies=dependencies,
        )

    def websocket(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    WebSocket path.
                    """
                ),
            ],
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    A name for the WebSocket. Only used internally.
                    """
                ),
            ] = None,
            *,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be used for this
                    WebSocket.
    
                    Read more about it in the
                    [FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).
                    """
                ),
            ] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Decorate a WebSocket function.

        Read more about it in the
        [FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).

        **Example**

        ```python
        from fastapi3 import FastAPI, WebSocket

        app = FastAPI()

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(f"Message text was: {data}")
        ```
        """

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_websocket_route(
                path,
                func,
                name=name,
                dependencies=dependencies,
            )
            return func

        return decorator

    def include_router(
            self,
            router: Annotated[routing.APIRouter, Doc("The `APIRouter` to include.")],
            *,
            prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to all the *path operations* in this
                    router.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to all the
                    *path operations* in this router.
    
                    Read more about it in the
                    [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
    
                    **Example**
    
                    ```python
                    from fastapi3 import Depends, FastAPI
    
                    from .dependencies import get_token_header
                    from .internal import admin
    
                    app = FastAPI()
    
                    app.include_router(
                        admin.router,
                        dependencies=[Depends(get_token_header)],
                    )
                    ```
                    """
                ),
            ] = None,
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses to be shown in OpenAPI.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).
    
                    And in the
                    [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark all the *path operations* in this router as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    **Example**
    
                    ```python
                    from fastapi3 import FastAPI
    
                    from .internal import old_api
    
                    app = FastAPI()
    
                    app.include_router(
                        old_api.router,
                        deprecated=True,
                    )
                    ```
                    """
                ),
            ] = None,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include (or not) all the *path operations* in this router in the
                    generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    **Example**
    
                    ```python
                    from fastapi3 import FastAPI
    
                    from .internal import old_api
    
                    app = FastAPI()
    
                    app.include_router(
                        old_api.router,
                        include_in_schema=False,
                    )
                    ```
                    """
                ),
            ] = True,
            default_response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Default response class to be used for the *path operations* in this
                    router.
    
                    Read more in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
    
                    **Example**
    
                    ```python
                    from fastapi3 import FastAPI
                    from fastapi3.responses import ORJSONResponse
    
                    from .internal import old_api
    
                    app = FastAPI()
    
                    app.include_router(
                        old_api.router,
                        default_response_class=ORJSONResponse,
                    )
                    ```
                    """
                ),
            ] = Default(JSONResponse),
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> None:
        """
        Include an `APIRouter` in the same app.

        Read more about it in the
        [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

        ## Example

        ```python
        from fastapi3 import FastAPI

        from .users import users_router

        app = FastAPI()

        app.include_router(users_router)
        ```
        """
        self.router.include_router(
            router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            default_response_class=default_response_class,
            callbacks=callbacks,
            generate_unique_id_function=generate_unique_id_function,
        )

    def get(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP GET operation.

        ## Example

        ```python
        from fastapi3 import FastAPI

        app = FastAPI()

        @app.get("/items/")
        def read_items():
            return [{"name": "Empanada"}, {"name": "Arepa"}]
        ```
        """
        return self.router.get(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def put(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP PUT operation.

        ## Example

        ```python
        from fastapi3 import FastAPI
        from pydantic import BaseModel

        class Item(BaseModel):
            name: str
            description: str | None = None

        app = FastAPI()

        @app.put("/items/{item_id}")
        def replace_item(item_id: str, item: Item):
            return {"message": "Item replaced", "id": item_id}
        ```
        """
        return self.router.put(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def post(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP POST operation.

        ## Example

        ```python
        from fastapi3 import FastAPI
        from pydantic import BaseModel

        class Item(BaseModel):
            name: str
            description: str | None = None

        app = FastAPI()

        @app.post("/items/")
        def create_item(item: Item):
            return {"message": "Item created"}
        ```
        """
        return self.router.post(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def delete(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP DELETE operation.

        ## Example

        ```python
        from fastapi3 import FastAPI

        app = FastAPI()

        @app.delete("/items/{item_id}")
        def delete_item(item_id: str):
            return {"message": "Item deleted"}
        ```
        """
        return self.router.delete(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def options(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP OPTIONS operation.

        ## Example

        ```python
        from fastapi3 import FastAPI

        app = FastAPI()

        @app.options("/items/")
        def get_item_options():
            return {"additions": ["Aji", "Guacamole"]}
        ```
        """
        return self.router.options(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def head(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP HEAD operation.

        ## Example

        ```python
        from fastapi3 import FastAPI, Response

        app = FastAPI()

        @app.head("/items/", status_code=204)
        def get_items_headers(response: Response):
            response.headers["X-Cat-Dog"] = "Alone in the world"
        ```
        """
        return self.router.head(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def patch(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP PATCH operation.

        ## Example

        ```python
        from fastapi3 import FastAPI
        from pydantic import BaseModel

        class Item(BaseModel):
            name: str
            description: str | None = None

        app = FastAPI()

        @app.patch("/items/")
        def update_item(item: Item):
            return {"message": "Item updated in place"}
        ```
        """
        return self.router.patch(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def trace(
            self,
            path: Annotated[
                str,
                Doc(
                    """
                    The URL path to be used for this *path operation*.
    
                    For example, in `http://example.com/items`, the path is `/items`.
                    """
                ),
            ],
            *,
            response_model: Annotated[
                Any,
                Doc(
                    """
                    The type to use for the response.
    
                    It could be any valid Pydantic *field* type. So, it doesn't have to
                    be a Pydantic model, it could be other things, like a `list`, `dict`,
                    etc.
    
                    It will be used for:
    
                    * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                        show it as the response (JSON Schema).
                    * Serialization: you could return an arbitrary object and the
                        `response_model` would be used to serialize that object into the
                        corresponding JSON.
                    * Filtering: the JSON sent to the client will only contain the data
                        (fields) defined in the `response_model`. If you returned an object
                        that contains an attribute `password` but the `response_model` does
                        not include that field, the JSON sent to the client would not have
                        that `password`.
                    * Validation: whatever you return will be serialized with the
                        `response_model`, converting any data as necessary to generate the
                        corresponding JSON. But if the data in the object returned is not
                        valid, that would mean a violation of the contract with the client,
                        so it's an error from the API developer. So, FastAPI will raise an
                        error and return a 500 error code (Internal Server Error).
    
                    Read more about it in the
                    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                    """
                ),
            ] = Default(None),
            status_code: Annotated[
                Optional[int],
                Doc(
                    """
                    The default status code to be used for the response.
    
                    You could override the status code by returning a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                    """
                ),
            ] = None,
            tags: Annotated[
                Optional[List[Union[str, Enum]]],
                Doc(
                    """
                    A list of tags to be applied to the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                    """
                ),
            ] = None,
            dependencies: Annotated[
                Optional[Sequence[Depends]],
                Doc(
                    """
                    A list of dependencies (using `Depends()`) to be applied to the
                    *path operation*.
    
                    Read more about it in the
                    [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                    """
                ),
            ] = None,
            summary: Annotated[
                Optional[str],
                Doc(
                    """
                    A summary for the *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    A description for the *path operation*.
    
                    If not provided, it will be extracted automatically from the docstring
                    of the *path operation function*.
    
                    It can contain Markdown.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                    """
                ),
            ] = None,
            response_description: Annotated[
                str,
                Doc(
                    """
                    The description for the default response.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = "Successful Response",
            responses: Annotated[
                Optional[Dict[Union[int, str], Dict[str, Any]]],
                Doc(
                    """
                    Additional responses that could be returned by this *path operation*.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            deprecated: Annotated[
                Optional[bool],
                Doc(
                    """
                    Mark this *path operation* as deprecated.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            operation_id: Annotated[
                Optional[str],
                Doc(
                    """
                    Custom operation ID to be used by this *path operation*.
    
                    By default, it is generated automatically.
    
                    If you provide a custom operation ID, you need to make sure it is
                    unique for the whole API.
    
                    You can customize the
                    operation ID generation with the parameter
                    `generate_unique_id_function` in the `FastAPI` class.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = None,
            response_model_include: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to include only certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_exclude: Annotated[
                Optional[IncEx],
                Doc(
                    """
                    Configuration passed to Pydantic to exclude certain fields in the
                    response data.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = None,
            response_model_by_alias: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response model
                    should be serialized by alias when an alias is used.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                    """
                ),
            ] = True,
            response_model_exclude_unset: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that were not set and
                    have their default values. This is different from
                    `response_model_exclude_defaults` in that if the fields are set,
                    they will be included in the response, even if the value is the same
                    as the default.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_defaults: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data
                    should have all the fields, including the ones that have the same value
                    as the default. This is different from `response_model_exclude_unset`
                    in that if the fields are set but contain the same default values,
                    they will be excluded from the response.
    
                    When `True`, default values are omitted from the response.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                    """
                ),
            ] = False,
            response_model_exclude_none: Annotated[
                bool,
                Doc(
                    """
                    Configuration passed to Pydantic to define if the response data should
                    exclude fields set to `None`.
    
                    This is much simpler (less smart) than `response_model_exclude_unset`
                    and `response_model_exclude_defaults`. You probably want to use one of
                    those two instead of this one, as those allow returning `None` values
                    when it makes sense.
    
                    Read more about it in the
                    [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                    """
                ),
            ] = False,
            include_in_schema: Annotated[
                bool,
                Doc(
                    """
                    Include this *path operation* in the generated OpenAPI schema.
    
                    This affects the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                    """
                ),
            ] = True,
            response_class: Annotated[
                Type[Response],
                Doc(
                    """
                    Response class to be used for this *path operation*.
    
                    This will not be used if you return a response directly.
    
                    Read more about it in the
                    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                    """
                ),
            ] = Default(JSONResponse),
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    Name for this *path operation*. Only used internally.
                    """
                ),
            ] = None,
            callbacks: Annotated[
                Optional[List[BaseRoute]],
                Doc(
                    """
                    List of *path operations* that will be used as OpenAPI callbacks.
    
                    This is only for OpenAPI documentation, the callbacks won't be used
                    directly.
    
                    It will be added to the generated OpenAPI (e.g. visible at `/docs`).
    
                    Read more about it in the
                    [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                    """
                ),
            ] = None,
            openapi_extra: Annotated[
                Optional[Dict[str, Any]],
                Doc(
                    """
                    Extra metadata to be included in the OpenAPI schema for this *path
                    operation*.
    
                    Read more about it in the
                    [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                    """
                ),
            ] = None,
            generate_unique_id_function: Annotated[
                Callable[[routing.APIRoute], str],
                Doc(
                    """
                    Customize the function used to generate unique IDs for the *path
                    operations* shown in the generated OpenAPI.
    
                    This is particularly useful when automatically generating clients or
                    SDKs for your API.
    
                    Read more about it in the
                    [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                    """
                ),
            ] = Default(generate_unique_id),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a *path operation* using an HTTP TRACE operation.

        ## Example

        ```python
        from fastapi3 import FastAPI

        app = FastAPI()

        @app.put("/items/{item_id}")
        def trace_item(item_id: str):
            return None
        ```
        """
        return self.router.trace(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def websocket_route(
            self, path: str, name: Union[str, None] = None
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.router.add_websocket_route(path, func, name=name)
            return func

        return decorator

    @deprecated(
        """
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
        """
    )
    def on_event(
            self,
            event_type: Annotated[
                str,
                Doc(
                    """
                    The type of event. `startup` or `shutdown`.
                    """
                ),
            ],
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add an event handler for the application.

        `on_event` is deprecated, use `lifespan` event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated).
        """
        return self.router.on_event(event_type)

    def middleware(
            self,
            middleware_type: str  # The type of middleware. Currently only supports `http`.
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add a middleware to the application.
        """
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_middleware(BaseHTTPMiddleware, dispatch=func)
            return func

        return decorator

    def exception_handler(
            self,
            exc_class_or_status_code: Annotated[
                Union[int, Type[Exception]],
                Doc(
                    """
                    The Exception class this would handle, or a status code.
                    """
                ),
            ],
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        Add an exception handler to the app.

        Read more about it in the
        [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).

        ## Example

        ```python
        from fastapi3 import FastAPI, Request
        from fastapi3.responses import JSONResponse


        class UnicornException(Exception):
            def __init__(self, name: str):
                self.name = name


        app = FastAPI()


        @app.exception_handler(UnicornException)
        async def unicorn_exception_handler(request: Request, exc: UnicornException):
            return JSONResponse(
                status_code=418,
                content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
            )
        ```
        """

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_exception_handler(exc_class_or_status_code, func)
            return func

        return decorator

# FastAPI Boot

&emsp;&emsp;FastAPI Boot is a FastAPI development toolkit that aims to provide a **more convenient** and **declarative** approach to `routing`, `dependency` `injection`, `error handling`, and `middleware`.

## Features

-   **Declarative Routing**: Simplify the way you define routes with a clear and intuitive syntax.
-   **Dependency Injection**: Manage dependencies effortlessly with a robust DI system that simplifies your application's architecture.
-   **Error Handling**: Built-in support for error handling that makes it easy to define and handle exceptions across your API.
-   **Middleware Support**: Integrate middleware with ease to add pre-processing and post-processing steps to your requests and responses.

## Getting Started

```bash
pip install fatsapi-boot
```

## USAGE

1. FBV(function based view)

```py
# FooController.py
from fastapi_boot import Controller


@Controller('/fbv', tags=['hello_world']).post('/foo')
def _():
    return 'Hello World'
```

```py
# main.py
import uvicorn
from fastapi import FastAPI
from fastapi_boot import provide_app

app = FastAPI()
provide_app(app) # scans dir automatically

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
```

2. CBV(class based view)

```py
from dataclasses import asdict, dataclass
from pydantic import BaseModel
from fastapi_boot import Controller, Delete, Get, Post, Put, Req


class Baz(BaseModel):
    baz: str

@dataclass
class Baz1:
    baz1: str


@Controller('/base-cbv', tags=['2. base cbv'])
class FirstController:

    @Req('/f', methods=['GET'])
    def f():
        return True

    @Get('/foo')
    def get_foo(self):
        return BaseResp(code=200, msg='success', data='foo')

    @Post('/bar')
    def post_bar(self, p: str = Query()):
        return p

    @Put('/baz')
    def put_baz(self, baz: Baz, baz1: Baz1):
        return dict(**baz.model_dump(), **asdict(baz1))
```

click <a href='https://github.com/hfdy0935/fastapi_boot/tree/main/exmaples' target="_blank">here</a> to get more examples.

## APIS

```py
from fastapi_boot import (
    Bean,
    Inject,
    Injectable,
    ExceptionHandler,
    Lifespan,
    provide_app,
    use_dep,
    use_http_middleware,
    use_ws_middleware,
    HTTPMiddleware,
    Controller,
    Delete,
    Get,
    Head,
    Options,
    Patch,
    Post,
    Prefix,
    Put,
    Req,
    Trace,
    WS,
    Autowired,
    Component,
    Repository,
    Service,
)

```

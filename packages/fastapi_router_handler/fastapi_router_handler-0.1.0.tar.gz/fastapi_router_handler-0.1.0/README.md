# FastAPI Router Handler

FastAPI Router Handler is a package designed to help you manage exception handling in FastAPI applications in a clean and consistent way. This package allows you to handle exceptions gracefully in router handlers while maintaining a consistent response format.

## Key Features

- Asynchronous exception handling support
- Custom logging integration
- Consistent error response format
- Global exception handling through middleware
- Customizable error messages

## Installation

```bash
pip install fastapi-router-handler
```

## Usage

### Basic Example

```python
from fastapi import FastAPI
from fastapi_router_handler import ExceptionHandler

app = FastAPI()
exception_handler = ExceptionHandler()

@app.get("/example")
async def example_endpoint():
    return await exception_handler.exception_handler(
        lambda: {"message": "success"}
    )

@app.get("/error-example")
async def error_endpoint():
    return await exception_handler.exception_handler(
        lambda: raise_error(),  # Function that raises an error
        e_code=400,
        e_msg="Custom error message"
    )
```

### Using Custom Logger

```python
import logging
from fastapi_router_handler import ExceptionHandler

logger = logging.getLogger(__name__)
exception_handler = ExceptionHandler(logger=logger)
```

## Response Examples

### Success Response

```json
{
  "message": "success"
}
```

### Error Response

```json
{
    "detail": "Internal Server Error",  # Requires e_msg setting, default: "Internal Server Error"
    "status_code": 500  # Requires e_code setting, default: 500
}
```

## License

MIT License

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

- Github: [@Jin-Doh/fastapi-router-handler](https://github.com/Jin-Doh/fastapi-router-handler)
- PyPI: [@fastapi-router-handler](https://pypi.org/project/fastapi-router-handler/)
- Email: [qqaa3030@gmail.com](mailto:qqaa3030@gmail.com)

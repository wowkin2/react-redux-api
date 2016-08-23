import os

from common import app

from apps import (
    authors, courses
)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))

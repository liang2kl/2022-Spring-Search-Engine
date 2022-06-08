DESCRIPTION
  An HTTP server that searches images similar to the given image.

TECHNOLOGIES
  - HTTP framework: flask
  - Database:       sqlite, redis

PREREQUISITES
  - A running Redis server
  - Install dependencies in requirements.txt
  - Some images to be indexed

RUN
  - Process indices: python3 app/index.py --dataset path/to/image/dir
  - Edit the self-explaining env.json
  - Run server:      FLASK_APP=app/server flask run

DOCKER
  The index must be processed before running the server in Docker. After
  indexing, map db.sqlite to /project/db.sqlite, and the directory containing
  the image files to /project/files.

PERFORMANCE
  The performance is not the main concern of this demo project. A more efficient
  image comparing algorithm can be adopted for faster responses.

  With 500 indexed files, the average response time is roughly 1~2 secs.

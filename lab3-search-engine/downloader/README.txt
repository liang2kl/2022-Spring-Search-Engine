DESCRIPTION
  A go application that download files from the given dataset in parallel.

TECHNOLOGIES
  go

PREREQUISITES
  - A csv file in the format of (id, url)

RUN
  You can check argument descriptions with "go run . --help".
  An example:
    go run . --file index.csv --output files --limit 500 --offset 0 --sleep 100ms

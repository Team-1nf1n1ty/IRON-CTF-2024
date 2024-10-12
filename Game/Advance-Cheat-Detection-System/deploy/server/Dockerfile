FROM golang:1.22.5 AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build .

FROM scratch

EXPOSE 8000

COPY --from=builder /app/server /app/server
COPY --from=builder /app/maps/ /app/maps/
WORKDIR /app

ENTRYPOINT  ["/app/server"]
# Stage 1: Build
FROM golang:1.25 AS builder
WORKDIR /app
COPY go.mod ./
COPY *.go ./
RUN go build -o server .

# Stage 2: Run
FROM alpine:latest
COPY --from=builder /app/server /server
CMD ["/server"]

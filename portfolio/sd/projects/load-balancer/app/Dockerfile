FROM golang:1.26-alpine AS builder
WORKDIR /app
COPY go.mod main.go ./
RUN go build -o server .

FROM alpine:latest
COPY --from=builder /app/server /server
CMD ["/server"]

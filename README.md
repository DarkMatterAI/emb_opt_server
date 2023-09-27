# emb_opt_server

`emb_opt_server` is a containerized service running the [emb_opt](https://github.com/DarkMatterAI/emb_opt) library.

# Quickstart

To start, clone the repo and build with `docker-compose`.

```
git clone https://github.com/DarkMatterAI/emb_opt_server

cd emb_opt_server

docker-compose up -d --build
```

The service is now running at port 7861, with API docs at `http://localhost:7861/docs`
# Development

## Docker

1. 先將 [`backend/.env.example`](../backend/.env.example) 複製一份到 `backend/.env`

   ```sh
   cp backend/.env.example backend/.env
   ```

2. 想辦法弄到 `OPEN_POINT_MID_V` 並填進 `backend/.env`
3. 到專案根目錄下 `docker compose up`，接著可以到 <http://0.0.0.0:8000/docs> 測試 API 或是到 <http://0.0.0.0:3000/> 戳戳看前端
   - 如果想要重 build docker image 可以下 `docker compose up --build`

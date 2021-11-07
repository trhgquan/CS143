## Thông tin
Chương trình chạy dưới dạng command-line

## Cài đặt
Cài các thư viện hỗ trợ: `pip install -r requirements.txt`

## Hướng dẫn sử dụng
Hỗ trợ các thuật sau:

|Tên thuật |Code thuật|
|----------|----------|
|   DFS    |  `dfs`   |
|   BFS    |  `bfs`   |
|Greedy BFS| `greedy` |
|A-Star    | `astar`  |
|Thuật tìm đường trên bản đồ có bonus| `bonus` |

Chạy code dưới dạng command-line:
```
python main.py --input=<tên file input>.txt --output=<tên file output>.png --algo=<code thuật>
```

Ví dụ: Chạy thuật toán A-Star trên bản đồ `sample/01.txt`, output ra file `01-astar.png`:
```
python main.py --input=sample/01.txt --output=01-astar.png --algo=astar
```

**Chú ý**: Để trống option `--algo` thì chương trình sẽ in ra bản đồ không có đường đi.

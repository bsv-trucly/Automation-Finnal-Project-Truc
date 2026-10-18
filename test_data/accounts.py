ADMIN = {"id": "admin", "password": "admin123", "name": "田中 太郎（管理者）"}
GUEST = {"id": "guest", "password": "guest123", "name": "鈴木 花子（新規ユーザー）"}
###NNTT: ở test_data chỉ nên chứa các thông tin liên quan data input, tên file, ... đối với các thông tin liên quan security như username, password bắt buộc phải nằm ở file .env
### Nhờ chị tạo riêng 1 file .env.example (đẩy file lên repo) và .env (chặn ở .gitignore) để tránh việc các thông tin security bị leak. 
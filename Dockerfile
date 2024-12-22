# Sử dụng Python phiên bản ổn định
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của ứng dụng vào container
COPY . .

# Tạo thư mục cần thiết
RUN mkdir -p uploads processed

# Cấu hình cổng mà Flask server sẽ sử dụng
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "run.py"]
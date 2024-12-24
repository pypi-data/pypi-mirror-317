from setuptools import setup, Extension
import os

# Đường dẫn tới thư mục chứa tệp main.m
objconpython_dir = os.path.join(os.path.dirname(__file__), 'objconpython')

# Xác định tệp nguồn là main.m
sources = [os.path.join(objconpython_dir, 'main.m')]

# Thêm cờ -framework Foundation cho biên dịch với Objective-C
extra_compile_args = ['-framework', 'Python', '-framework', 'Foundation']

# Tạo Extension object để biên dịch thư viện Objective-C
color_terminal_extension = Extension(
    name='objconpython',
    sources=sources,
    extra_compile_args=extra_compile_args,
    language='objective-c',  # Xác định ngôn ngữ Objective-C
)

# Đọc nội dung của tệp README.md để làm long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Thiết lập gói
setup(
    name='objconpython',
    version='0.3',
    description='A Python package to run objc code on python',
    author='Bobby',
    author_email='info@bobby-shop.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules=[color_terminal_extension],
)

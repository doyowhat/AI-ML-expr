@echo off
REM 创建基本测试文件
fsutil file createnew "photo1.jpg" 1024
fsutil file createnew "pic02.jpg" 1024
fsutil file createnew "IMG_123.jpg" 1024
fsutil file createnew "DSC00045.jpg" 1024

REM 创建特殊字符测试文件
fsutil file createnew "my image.jpg" 1024
fsutil file createnew "file-with-dash.jpg" 1024
fsutil file createnew "photo_with_underscore.jpg" 1024
fsutil file createnew "file with spaces.jpg" 1024

REM 创建混合类型文件
fsutil file createnew "file1.jpg" 1024
fsutil file createnew "document.pdf" 2048  REM 稍微大一点，模拟PDF
fsutil file createnew "text.txt" 512       REM 小一点，模拟文本
fsutil file createnew "data.png" 1024

REM 创建边界情况测试文件
fsutil file createnew ".jpg" 1024
fsutil file createnew "file without extension" 512
fsutil file createnew "file.double.ext.jpg" 1024
fsutil file createnew "123456.jpg" 1024
fsutil file createnew "CAPS.JPG" 1024
fsutil file createnew "mixed.CASE.Jpg" 1024

echo 所有测试文件已创建完毕！
pause
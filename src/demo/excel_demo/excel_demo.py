from src.module import *

excel_tool = ExcelTools("test.xlsx")
(row_size, col_size) = excel_tool.get_sheet_shape()
print("excel行尺寸:", row_size, "\t列尺寸", col_size)
print("获取第1行,整行:", excel_tool[1])
print("获取第1行,2~4列:", excel_tool[1, 2:4])
print("获取第最后一行,1~4列:", excel_tool[row_size, 1:4])
print("获取第1列:", excel_tool[:, 1])
print("获取第1~2列:", excel_tool[:, 1:5])
print("获取第1~3行第2~4列:", excel_tool[1:3, 2:4])
print("获取单元格 (2,3):", excel_tool[2, 3])

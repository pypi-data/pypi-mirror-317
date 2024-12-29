


funcs = []
for i in range(3):
    funcs.append(lambda: i)

# 所有 lambda 函数都引用相同的 i，最终 i 的值是 2
print([f() for f in funcs])  # 输出 [2, 2, 2]


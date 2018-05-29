此程序做了部分药物筛选处理：

1. u5>=10, u6>=10, u7>=u6/2
2. u4!=0
3. 有pocket，且为药物，重量够大
4. 添加了n-mer列（多聚体个数）

---

# Run

```
python3 select.py
```

input: [017.csv](017.csv)

output: [017.result.csv](017.result.csv)
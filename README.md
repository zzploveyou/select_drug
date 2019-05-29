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


# 部分特征说明

pdbqt文件格式

http://autodock.scripps.edu/faqs-help/faq/what-is-the-format-of-a-pdbqt-file


u4: 20个model中，root信息与蛋白之间距离<3A的个数

u5: 重量小于317.41，取20个model中小于-6的个数，反之，取小于-8的个数

u6: 20个model，做聚类，最大的那个cluster中model的个数

u7：u6中选取的最大个数的cluster中，满足u5的个数


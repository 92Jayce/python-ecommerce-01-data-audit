"""第01讲 读懂业务数据与表的粒度
业务问题：每张表的一行究竟代表什么？
全部使用模拟教学数据。"""
from pathlib import Path
import sys
if "__file__" in globals():
    COURSE_ROOT = Path(__file__).resolve().parents[1]
else:
    COURSE_ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "course_common.py").exists())
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from course_common import (ROOT, DATA, AS_OF, BLUE, TEAL, ORANGE, load_tables,
    build_facts, positive_orders, rfm_table, safe_divide, outdir, save_table, save_figure, show)

# %% 读取与字段检查
t = load_tables()
orders = t['orders']
print('订单样本：'); show(orders)
orders.info()
print('取消/支付状态：'); print(orders['status'].value_counts())

# %% 多张表的行数不是同一种计数单位
grain = {'customers':'一个客户', 'products':'一个SKU', 'sessions':'一次会话',
         'orders':'一张订单', 'order_items':'一张订单的一个SKU行',
         'marketing':'一天一个渠道', 'inventory':'一天一个SKU',
         'experiment':'一位试验访客', 'reviews':'一条评论'}
audit = pd.DataFrame([{'table':k, 'rows':len(v), 'grain':grain[k],
    'missing_cells':int(v.isna().sum().sum())} for k,v in t.items()])
show(audit,20); save_table(audit,1,'table_grain_audit')
assert orders.order_id.is_unique
assert t['order_items'].order_id.nunique() == len(orders)
print('注意：会话数不等于人数；订单行数不等于订单数。')

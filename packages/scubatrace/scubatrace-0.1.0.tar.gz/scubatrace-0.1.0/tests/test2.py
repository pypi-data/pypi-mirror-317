import scubatrace

scubatrace.CProject("../tests").files["test.c"].functions[1].export_cfg_dot("test.dot") # 构建 CFG
scubatrace.CProject("../tests").files["test.c"].functions[1].callers # 获取调用的函数
scubatrace.CProject("../tests").files["test.c"].functions[1].callees # 获取调用的函数
scubatrace.CProject("../tests").files["test.c"].functions[1].statements[3].post_controls # 获取指定语句的 CFG 后继语句
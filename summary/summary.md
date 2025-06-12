## 简介
我是一枚前端开发工程师，之前做过跟数据相关的工作，大概就是数据可视化大屏的页面展示了。有段时间对数据相关的工作挺好奇的，于是找了大数据的朋友了解了一下，原来数据分析是偏向产品业务逻辑的，对于一个开发来说，是需要做思维转变的。怀着好奇心报名了极客时间第一期的AI数据分析训练营，在这15周的学习中，除了对数据分析有更进一步的了解外，还有对AI的一些知识的了解。

## 一些收获
#### 关于数据分析
+ 数据分析流程
    - 基于业务理解发现问题，通过观察现状、多维交叉分析、预测趋势、生成策略、推动落地、复盘效果形成闭环。例如，日活下跌时需验证数据来源、计算口径，再通过同比环比、交叉分析定位原因
+ 数据分析思维
    - 分类思维：BCG矩阵、Kraljic采购模型
    - <font style="color:rgb(28, 31, 35);background-color:rgb(249, 250, 251);">分层思维：RFM顾客分层、帕累托2/8法则</font>
+ <font style="color:rgb(64, 64, 64);">数据决策（不同行业）</font>
    - <font style="color:rgba(0, 0, 0, 0.85) !important;">金融行业借助 Fintech 实现智能营销、反洗钱（如大额交易标准）、贷款质量分析（如 M0 到 M6 迁徙率）等，运用规则引擎、聚类分析等算法</font>
    - <font style="color:rgba(0, 0, 0, 0.85) !important;">快消行业通过八爪鱼采集数据、LLM 分析评论进行竞品分析（如安踏好评率 95%），还有智能排班规划</font>
    - <font style="color:rgba(0, 0, 0, 0.85) !important;">制造行业利用 AI 进行路径规划（如叉车 AGVs）、缺陷检测（如螺栓扭矩曲线分析）、供应链预测，提升生产效率与安全</font>
+ 数据指标
    - 北极星指标：又称第一关键指标，是业务当前阶段最关注的指标，引导业务发展，直接反映产品核心价值并与长期商业目标关联
    - 虚荣指标：看似良好但无法准确反映业务健康状况的数据，仅展示增长面，忽略流失率、活跃度等，对战略决策帮助甚微。常见如累计用户数、累计销量、累计销售额等

#### 关于AI
+ 理解AI
    - 分析式AI：目标是分析数据、提供洞察，用于风险评估等，基于统计分析
    - 生成式AI：目标是生成内容，用于广告设计等，基于大模型
+ 机器学习七步法
    - 数据收集、数据预处理、模型选择、模型训练、超参数调整、模型预测、模型评估
+ 算法
    - <font style="color:rgb(0, 0, 0);">机器学习算法</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">分类算法：逻辑回归、决策树、随机森林、评分卡</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">回归算法：线性回归、岭回归、套索回归</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">集成学习：随机森林、GBDT、XGBoost、LightGBM、CatBoost</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">聚类算法：KMeans</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">关联分析：Apriori</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">推荐系统算法：UserCF（用户协同过滤）、ItemCF（物品协同过滤）、GBDT + LR、Wide & Deep</font>
    - <font style="color:rgb(0, 0, 0);">时间序列预测算法</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">时间序列分析：ARMA、ARIMA、Prophet、时间因子、informer</font>
    - <font style="color:rgb(0, 0, 0);">深度学习算法</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">缺陷检测：YOLO（目标检测算法）</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">视频理解：InternVideo</font>
    - <font style="color:rgb(0, 0, 0);">运筹规划</font>
        * <font style="color:rgba(0, 0, 0, 0.85) !important;">运筹学优化：线性规划、整数规划、混合整数规划、TSP（旅行商问题）、VRP（车辆路径问题</font>
+ 模型
    - <font style="color:rgb(0, 0, 0) !important;">大模型推理</font><font style="color:rgba(0, 0, 0, 0.85) !important;">：Qwen、Qwen - Coder、Qwen - VL</font>
    - <font style="color:rgb(0, 0, 0) !important;">AI Agent</font><font style="color:rgba(0, 0, 0, 0.85) !important;">：Qwen - Agent、Coze</font>
    - <font style="color:rgb(0, 0, 0) !important;">RAG 知识库</font><font style="color:rgba(0, 0, 0, 0.85) !important;">：Native RAG、GraphRAG、KAG</font>

#### 关于编码
+ cursor 的使用
+ python 和 sql 的语法了解

#### 关于案例
+ 分析预测类
    - 财务绩效分析与成本控制
    - 二手车价格预测
    - 从销售数据中找到影响销售的主要原因
    - 对沪市指数走势进行预测
    - 资金流入流出预测
    - 页面流量预测
    - 交通流量预测
    - 员工离职预测
    - 男女声音识别
+ 算法实践与优化类
    - 搭建你的自助查询应用
    - 搭建多模态 AI 助手
    - Santa 的接待安排
    - 使用 Ortools 求解旅行商问题
    - 指定城市的旅行商 TSP
    - 多辆车的路径规划 VRP
    - 带有容量约束的 VRP
    - 带有时间窗口约束的 VRP
    - 带有指定拿起放下约束的 VRP
    - MovieLens 推荐算法
    - 阿里移动推荐算法挑战赛
    - 搭建酒店推荐系统
    - 使用 Embedding 进行文章去重
    - 根据自己的业务场景搭建需求分析助手
+ 采购与物料类
    - 采购物料分类与决策

## 总结
+ 补充统计学知识，从数据分析案例中加深了对数学的应用的理解
+ 从日常工作中多接触一些业务场景，积累案例
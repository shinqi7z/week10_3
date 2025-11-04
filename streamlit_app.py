# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json

# 页面配置
st.set_page_config(
    page_title="A股股票推荐系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("📈 A股股票推荐系统")
st.markdown("""
### 初学者也能轻松理解的股票分析工具
**基于技术指标和基本面的智能推荐系统**
""")

class AStockRecommender:
    def __init__(self):
        # 沪深300成分股示例数据
        self.stocks_data = self.generate_sample_data()
        
    def generate_sample_data(self):
        """生成示例股票数据"""
        stocks = [
            {
                'code': '000858', 'name': '五粮液', 'sector': '消费',
                'current_price': 168.50, 'change_rate': 2.34,
                'volume': 8.5, 'market_cap': 6500,
                'pe_ratio': 28.5, 'pb_ratio': 6.2,
                'revenue_growth': 15.2, 'profit_growth': 18.7,
                'rsi': 62.3, 'macd_signal': '金叉', 'bollinger_position': '中轨',
                'recommend_score': 92.5, 'risk_level': '中低',
                'tags': ['白酒龙头', '高ROE', '稳定增长']
            },
            {
                'code': '600519', 'name': '贵州茅台', 'sector': '消费',
                'current_price': 1750.80, 'change_rate': 1.56,
                'volume': 12.3, 'market_cap': 22000,
                'pe_ratio': 35.2, 'pb_ratio': 12.8,
                'revenue_growth': 12.8, 'profit_growth': 16.3,
                'rsi': 58.7, 'macd_signal': '金叉', 'bollinger_position': '上轨',
                'recommend_score': 88.7, 'risk_level': '低',
                'tags': ['酱香龙头', '稀缺性', '品牌价值']
            },
            {
                'code': '300750', 'name': '宁德时代', 'sector': '新能源',
                'current_price': 198.30, 'change_rate': 3.45,
                'volume': 15.8, 'market_cap': 8700,
                'pe_ratio': 42.1, 'pb_ratio': 8.9,
                'revenue_growth': 25.7, 'profit_growth': 32.1,
                'rsi': 65.2, 'macd_signal': '金叉', 'bollinger_position': '上轨',
                'recommend_score': 85.3, 'risk_level': '中',
                'tags': ['电池龙头', '高成长', '新能源']
            },
            {
                'code': '601318', 'name': '中国平安', 'sector': '金融',
                'current_price': 48.92, 'change_rate': 0.85,
                'volume': 9.2, 'market_cap': 8900,
                'pe_ratio': 8.9, 'pb_ratio': 1.2,
                'revenue_growth': 5.3, 'profit_growth': 7.8,
                'rsi': 45.6, 'macd_signal': '即将金叉', 'bollinger_position': '下轨',
                'recommend_score': 82.1, 'risk_level': '低',
                'tags': ['保险龙头', '低估值', '高分红']
            },
            {
                'code': '000333', 'name': '美的集团', 'sector': '家电',
                'current_price': 56.78, 'change_rate': 1.23,
                'volume': 6.7, 'market_cap': 4000,
                'pe_ratio': 15.6, 'pb_ratio': 3.2,
                'revenue_growth': 8.9, 'profit_growth': 12.4,
                'rsi': 52.3, 'macd_signal': '金叉', 'bollinger_position': '中轨',
                'recommend_score': 79.8, 'risk_level': '中低',
                'tags': ['家电龙头', '全球化', '稳定现金流']
            },
            {
                'code': '600036', 'name': '招商银行', 'sector': '金融',
                'current_price': 32.45, 'change_rate': 0.93,
                'volume': 11.5, 'market_cap': 8200,
                'pe_ratio': 6.8, 'pb_ratio': 1.1,
                'revenue_growth': 7.2, 'profit_growth': 9.5,
                'rsi': 48.9, 'macd_signal': '即将金叉', 'bollinger_position': '下轨',
                'recommend_score': 77.6, 'risk_level': '低',
                'tags': ['零售银行', '资产质量', '高ROE']
            },
            {
                'code': '000001', 'name': '平安银行', 'sector': '金融',
                'current_price': 12.34, 'change_rate': 1.15,
                'volume': 7.8, 'market_cap': 2400,
                'pe_ratio': 7.2, 'pb_ratio': 0.9,
                'revenue_growth': 6.8, 'profit_growth': 8.9,
                'rsi': 46.7, 'macd_signal': '即将金叉', 'bollinger_position': '下轨',
                'recommend_score': 75.2, 'risk_level': '中',
                'tags': ['数字化转型', '零售转型', '低估']
            },
            {
                'code': '601888', 'name': '中国中免', 'sector': '消费',
                'current_price': 89.67, 'change_rate': 2.78,
                'volume': 5.3, 'market_cap': 1800,
                'pe_ratio': 32.1, 'pb_ratio': 7.8,
                'revenue_growth': 18.9, 'profit_growth': 22.4,
                'rsi': 61.8, 'macd_signal': '金叉', 'bollinger_position': '中轨',
                'recommend_score': 83.4, 'risk_level': '中',
                'tags': ['免税龙头', '消费升级', '渠道优势']
            }
        ]
        return pd.DataFrame(stocks)
    
    def calculate_recommendation_score(self, row):
        """计算推荐分数（模拟算法）"""
        score = 0
        
        # 估值因素 (30%)
        if row['pe_ratio'] < 15:
            score += 30
        elif row['pe_ratio'] < 25:
            score += 25
        elif row['pe_ratio'] < 35:
            score += 20
        else:
            score += 15
        
        # 成长因素 (30%)
        growth_score = min(30, row['profit_growth'] * 0.8)
        score += growth_score
        
        # 技术指标 (20%)
        if row['macd_signal'] == '金叉':
            score += 15
        elif row['macd_signal'] == '即将金叉':
            score += 10
        else:
            score += 5
            
        if row['rsi'] > 30 and row['rsi'] < 70:
            score += 5
        
        # 市场地位 (20%)
        if '龙头' in str(row['tags']):
            score += 20
        else:
            score += 10
            
        return min(100, score)
    
    def get_recommended_stocks(self, min_market_cap=1000, max_pe=50, sector_filter=None):
        """获取推荐股票列表"""
        df = self.stocks_data.copy()
        
        # 应用过滤器
        if min_market_cap:
            df = df[df['market_cap'] >= min_market_cap]
        
        if max_pe:
            df = df[df['pe_ratio'] <= max_pe]
            
        if sector_filter and sector_filter != "全部":
            df = df[df['sector'] == sector_filter]
        
        # 计算推荐分数
        df['recommend_score'] = df.apply(self.calculate_recommendation_score, axis=1)
        
        # 按分数排序
        df = df.sort_values('recommend_score', ascending=False)
        
        return df

# 初始化推荐系统
recommender = AStockRecommender()

# 侧边栏 - 分析设置
st.sidebar.header("🔧 分析设置")

# 行业筛选
sectors = ["全部", "消费", "新能源", "金融", "家电"]
selected_sector = st.sidebar.selectbox("行业筛选", sectors, index=0)

# 估值筛选
min_market_cap = st.sidebar.number_input(
    "最小市值（亿元）", 
    min_value=0, 
    max_value=10000, 
    value=1000,
    step=100
)

max_pe = st.sidebar.slider(
    "最大市盈率(PE)", 
    min_value=0, 
    max_value=100, 
    value=50
)

# 风险偏好
risk_tolerance = st.sidebar.select_slider(
    "风险承受能力",
    options=["保守", "稳健", "平衡", "成长", "激进"],
    value="平衡"
)

# 更新按钮
if st.sidebar.button("🔄 重新分析", type="primary"):
    st.rerun()

# 主内容区域
st.markdown("---")

# 获取推荐股票
recommended_stocks = recommender.get_recommended_stocks(
    min_market_cap=min_market_cap,
    max_pe=max_pe,
    sector_filter=selected_sector
)

# 显示推荐股票
st.subheader(f"🏆 推荐股票 TOP {len(recommended_stocks)}")

if len(recommended_stocks) > 0:
    # 创建两列布局
    cols = st.columns(2)
    
    for idx, (_, stock) in enumerate(recommended_stocks.iterrows()):
        col = cols[idx % 2]
        
        with col:
            # 创建卡片容器
            with st.container():
                # 标题行
                st.markdown(f"### {idx + 1}위. {stock['name']} ({stock['code']})")
                
                # 价格和基本信息
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "当前价", 
                        f"¥{stock['current_price']:.2f}",
                        delta=f"+{stock['change_rate']}%"
                    )
                with col2:
                    st.metric("市值", f"{stock['market_cap']}亿元")
                
                # 详细信息
                with st.expander("📊 详细分析", expanded=True):
                    # 财务指标
                    st.write("**财务指标:**")
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        st.write(f"PE: {stock['pe_ratio']}")
                    with col_f2:
                        st.write(f"PB: {stock['pb_ratio']}")
                    with col_f3:
                        st.write(f"营收增长: {stock['revenue_growth']}%")
                    
                    # 技术指标
                    st.write("**技术指标:**")
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        st.write(f"RSI: {stock['rsi']}")
                    with col_t2:
                        st.write(f"MACD: {stock['macd_signal']}")
                    with col_t3:
                        st.write(f"布林带: {stock['bollinger_position']}")
                    
                    # 投资建议
                    st.write("**投资建议:**")
                    
                    # 根据分数显示不同的推荐强度
                    score = stock['recommend_score']
                    if score >= 90:
                        st.success("🚀 强烈买入 - 综合评分优秀")
                    elif score >= 80:
                        st.info("📈 建议买入 - 综合评分良好")
                    elif score >= 70:
                        st.warning("🤔 谨慎买入 - 综合评分一般")
                    else:
                        st.error("⏸️ 观望 - 需要更多信号")
                    
                    # 具体理由
                    reasons = []
                    if stock['pe_ratio'] < 20:
                        reasons.append("估值合理")
                    if stock['profit_growth'] > 15:
                        reasons.append("高成长性")
                    if '龙头' in str(stock['tags']):
                        reasons.append("行业龙头地位")
                    if stock['macd_signal'] == '金叉':
                        reasons.append("技术面金叉信号")
                    
                    if reasons:
                        st.write("**推荐理由:** " + "、".join(reasons))
                    
                    # 风险提示
                    if stock['risk_level'] == '高':
                        st.error(f"⚠️ 风险等级: {stock['risk_level']}")
                    elif stock['risk_level'] == '中':
                        st.warning(f"⚠️ 风险等级: {stock['risk_level']}")
                    else:
                        st.success(f"✅ 风险等级: {stock['risk_level']}")
                
                st.markdown("---")
else:
    st.warning("没有找到符合筛选条件的股票，请调整筛选条件。")

# 数据可视化部分
st.markdown("---")
st.subheader("📈 市场概览")

if len(recommended_stocks) > 0:
    # 创建三个图表
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 市盈率分布图
        fig_pe = px.bar(
            recommended_stocks.head(5),
            x='name',
            y='pe_ratio',
            title='TOP5 市盈率对比',
            color='pe_ratio',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_pe, use_container_width=True)
    
    with col2:
        # 成长性对比
        fig_growth = go.Figure(data=[
            go.Bar(name='营收增长', x=recommended_stocks.head(5)['name'], 
                   y=recommended_stocks.head(5)['revenue_growth']),
            go.Bar(name='利润增长', x=recommended_stocks.head(5)['name'], 
                   y=recommended_stocks.head(5)['profit_growth'])
        ])
        fig_growth.update_layout(title='TOP5 成长性对比', barmode='group')
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col3:
        # 推荐分数雷达图
        top_stock = recommended_stocks.iloc[0]
        categories = ['估值', '成长', '技术', '地位', '综合']
        values = [
            max(0, 100 - (top_stock['pe_ratio'] - 15) * 3),  # 估值分数
            min(100, top_stock['profit_growth'] * 4),        # 成长分数
            75 if top_stock['macd_signal'] == '金叉' else 50, # 技术分数
            90 if '龙头' in str(top_stock['tags']) else 60,   # 地位分数
            top_stock['recommend_score']                      # 综合分数
        ]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=top_stock['name']
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title=f"{top_stock['name']} 多维度分析"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# 投资策略建议
st.markdown("---")
st.subheader("💡 投资策略建议")

strategy_cols = st.columns(2)

with strategy_cols[0]:
    st.markdown("""
    ### 🎯 当前市场建议
    
    **基于您的风险偏好：** `{}`
    
    - **仓位配置：** 建议{}仓位操作
    - **持股周期：** {}个月
    - **重点关注：** {}板块
    - **风险控制：** 单只股票不超过总仓位的{}%
    """.format(
        risk_tolerance,
        "7-8成" if risk_tolerance in ["成长", "激进"] else "5-6成",
        "6-12" if risk_tolerance in ["成长", "激进"] else "12-24",
        selected_sector if selected_sector != "全部" else "消费、新能源",
        20 if risk_tolerance in ["成长", "激进"] else 15
    ))

with strategy_cols[1]:
    st.markdown("""
    ### 📋 注意事项
    
    **技术面提醒：**
    - MACD金叉信号需要成交量配合
    - RSI超过70注意短期回调风险
    - 关注布林带突破的有效性
    
    **基本面提醒：**
    - 高PE股票需要更高的成长性支撑
    - 关注季度财报发布时间
    - 注意行业政策变化影响
    
    **风险提示：** 股市有风险，投资需谨慎
    """)

# 快速筛选按钮
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 快速筛选")

quick_filter_cols = st.sidebar.columns(2)

with quick_filter_cols[0]:
    if st.button("消费龙头", use_container_width=True):
        st.session_state.sector_filter = "消费"
        st.rerun()

with quick_filter_cols[1]:
    if st.button("低估值", use_container_width=True):
        st.session_state.max_pe = 15
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📚 行业分布")

sector_quick_cols = st.sidebar.columns(2)

sectors_quick = ["新能源", "金融", "家电", "科技"]
for sector in sectors_quick:
    col = sector_quick_cols[sectors_quick.index(sector) % 2]
    with col:
        if st.button(sector, use_container_width=True):
            st.session_state.sector_filter = sector
            st.rerun()

# 免责声明
with st.sidebar.expander("⚠️ 免责声明"):
    st.markdown("""
    本系统仅为技术演示工具，不构成投资建议。
    
    **数据说明：**
    - 股票数据为模拟生成
    - 推荐算法仅为示例
    - 实际投资请参考专业机构建议
    
    **风险提示：**
    - 股市有风险，入市需谨慎
    - 过往表现不代表未来收益
    - 投资决策需要综合考虑多种因素
    """)

# 初始化session state
if 'sector_filter' not in st.session_state:
    st.session_state.sector_filter = "全部"
if 'max_pe' not in st.session_state:
    st.session_state.max_pe = 50

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>A股股票推荐系统 | 技术分析演示工具</p>
    <p>Arts & Advanced Big Data | Week 10 - Open API Integration</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | 2024</p>
    <p>数据仅供参考，不构成投资建议</p>
    </div>
    """,
    unsafe_allow_html=True
)

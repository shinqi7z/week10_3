# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json

# Page configuration
st.set_page_config(
    page_title="A-Share Stock Recommendation System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("📈 A-Share Stock Recommendation System")
st.markdown("""
### Easy-to-understand stock analysis tool for beginners
**Intelligent recommendation system based on technical indicators and fundamentals**
""")

class AStockRecommender:
    def __init__(self):
        # Sample data for CSI 300 constituent stocks
        self.stocks_data = self.generate_sample_data()
        
    def generate_sample_data(self):
        """Generate sample stock data"""
        stocks = [
            {
                'code': '000858', 'name': 'Wuliangye', 'sector': 'Consumer',
                'current_price': 168.50, 'change_rate': 2.34,
                'volume': 8.5, 'market_cap': 6500,
                'pe_ratio': 28.5, 'pb_ratio': 6.2,
                'revenue_growth': 15.2, 'profit_growth': 18.7,
                'rsi': 62.3, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 92.5, 'risk_level': 'Low-Medium',
                'tags': ['Liquor Leader', 'High ROE', 'Stable Growth']
            },
            {
                'code': '600519', 'name': 'Kweichow Moutai', 'sector': 'Consumer',
                'current_price': 1750.80, 'change_rate': 1.56,
                'volume': 12.3, 'market_cap': 22000,
                'pe_ratio': 35.2, 'pb_ratio': 12.8,
                'revenue_growth': 12.8, 'profit_growth': 16.3,
                'rsi': 58.7, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 88.7, 'risk_level': 'Low',
                'tags': ['Liquor Leader', 'Scarcity', 'Brand Value']
            },
            {
                'code': '300750', 'name': 'CATL', 'sector': 'New Energy',
                'current_price': 198.30, 'change_rate': 3.45,
                'volume': 15.8, 'market_cap': 8700,
                'pe_ratio': 42.1, 'pb_ratio': 8.9,
                'revenue_growth': 25.7, 'profit_growth': 32.1,
                'rsi': 65.2, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 85.3, 'risk_level': 'Medium',
                'tags': ['Battery Leader', 'High Growth', 'New Energy']
            },
            {
                'code': '601318', 'name': 'Ping An Insurance', 'sector': 'Financial',
                'current_price': 48.92, 'change_rate': 0.85,
                'volume': 9.2, 'market_cap': 8900,
                'pe_ratio': 8.9, 'pb_ratio': 1.2,
                'revenue_growth': 5.3, 'profit_growth': 7.8,
                'rsi': 45.6, 'macd_signal': 'Approaching Golden Cross', 'bollinger_position': 'Lower Band',
                'recommend_score': 82.1, 'risk_level': 'Low',
                'tags': ['Insurance Leader', 'Low Valuation', 'High Dividend']
            },
            {
                'code': '000333', 'name': 'Midea Group', 'sector': 'Home Appliances',
                'current_price': 56.78, 'change_rate': 1.23,
                'volume': 6.7, 'market_cap': 4000,
                'pe_ratio': 15.6, 'pb_ratio': 3.2,
                'revenue_growth': 8.9, 'profit_growth': 12.4,
                'rsi': 52.3, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 79.8, 'risk_level': 'Low-Medium',
                'tags': ['Home Appliance Leader', 'Globalization', 'Stable Cash Flow']
            },
            {
                'code': '600036', 'name': 'China Merchants Bank', 'sector': 'Financial',
                'current_price': 32.45, 'change_rate': 0.93,
                'volume': 11.5, 'market_cap': 8200,
                'pe_ratio': 6.8, 'pb_ratio': 1.1,
                'revenue_growth': 7.2, 'profit_growth': 9.5,
                'rsi': 48.9, 'macd_signal': 'Approaching Golden Cross', 'bollinger_position': 'Lower Band',
                'recommend_score': 77.6, 'risk_level': 'Low',
                'tags': ['Retail Banking', 'Asset Quality', 'High ROE']
            },
            {
                'code': '000001', 'name': 'Ping An Bank', 'sector': 'Financial',
                'current_price': 12.34, 'change_rate': 1.15,
                'volume': 7.8, 'market_cap': 2400,
                'pe_ratio': 7.2, 'pb_ratio': 0.9,
                'revenue_growth': 6.8, 'profit_growth': 8.9,
                'rsi': 46.7, 'macd_signal': 'Approaching Golden Cross', 'bollinger_position': 'Lower Band',
                'recommend_score': 75.2, 'risk_level': 'Medium',
                'tags': ['Digital Transformation', 'Retail Transformation', 'Undervalued']
            },
            {
                'code': '601888', 'name': 'China Tourism Group', 'sector': 'Consumer',
                'current_price': 89.67, 'change_rate': 2.78,
                'volume': 5.3, 'market_cap': 1800,
                'pe_ratio': 32.1, 'pb_ratio': 7.8,
                'revenue_growth': 18.9, 'profit_growth': 22.4,
                'rsi': 61.8, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 83.4, 'risk_level': 'Medium',
                'tags': ['Duty-free Leader', 'Consumption Upgrade', 'Channel Advantage']
            }
        ]
        return pd.DataFrame(stocks)
    
    def calculate_recommendation_score(self, row):
        """Calculate recommendation score (simulated algorithm)"""
        score = 0
        
        # Valuation factors (30%)
        if row['pe_ratio'] < 15:
            score += 30
        elif row['pe_ratio'] < 25:
            score += 25
        elif row['pe_ratio'] < 35:
            score += 20
        else:
            score += 15
        
        # Growth factors (30%)
        growth_score = min(30, row['profit_growth'] * 0.8)
        score += growth_score
        
        # Technical indicators (20%)
        if row['macd_signal'] == 'Golden Cross':
            score += 15
        elif row['macd_signal'] == 'Approaching Golden Cross':
            score += 10
        else:
            score += 5
            
        if row['rsi'] > 30 and row['rsi'] < 70:
            score += 5
        
        # Market position (20%)
        if 'Leader' in str(row['tags']):
            score += 20
        else:
            score += 10
            
        return min(100, score)
    
    def get_recommended_stocks(self, min_market_cap=1000, max_pe=50, sector_filter=None):
        """Get recommended stock list"""
        df = self.stocks_data.copy()
        
        # Apply filters
        if min_market_cap:
            df = df[df['market_cap'] >= min_market_cap]
        
        if max_pe:
            df = df[df['pe_ratio'] <= max_pe]
            
        if sector_filter and sector_filter != "All":
            df = df[df['sector'] == sector_filter]
        
        # Calculate recommendation score
        df['recommend_score'] = df.apply(self.calculate_recommendation_score, axis=1)
        
        # Sort by score
        df = df.sort_values('recommend_score', ascending=False)
        
        return df

# Initialize recommendation system
recommender = AStockRecommender()

# Sidebar - Analysis Settings
st.sidebar.header("🔧 Analysis Settings")

# Sector filter
sectors = ["All", "Consumer", "New Energy", "Financial", "Home Appliances"]
selected_sector = st.sidebar.selectbox("Sector Filter", sectors, index=0)

# Valuation filter
min_market_cap = st.sidebar.number_input(
    "Minimum Market Cap (Billion CNY)", 
    min_value=0, 
    max_value=10000, 
    value=1000,
    step=100
)

max_pe = st.sidebar.slider(
    "Maximum P/E Ratio", 
    min_value=0, 
    max_value=100, 
    value=50
)

# Risk preference
risk_tolerance = st.sidebar.select_slider(
    "Risk Tolerance",
    options=["Conservative", "Moderate", "Balanced", "Growth", "Aggressive"],
    value="Balanced"
)

# Update button
if st.sidebar.button("🔄 Re-analyze", type="primary"):
    st.rerun()

# Main content area
st.markdown("---")

# Get recommended stocks
recommended_stocks = recommender.get_recommended_stocks(
    min_market_cap=min_market_cap,
    max_pe=max_pe,
    sector_filter=selected_sector
)

# Display recommended stocks
st.subheader(f"🏆 Recommended Stocks TOP {len(recommended_stocks)}")

if len(recommended_stocks) > 0:
    # Create two-column layout
    cols = st.columns(2)
    
    for idx, (_, stock) in enumerate(recommended_stocks.iterrows()):
        col = cols[idx % 2]
        
        with col:
            # Create card container
            with st.container():
                # Title row
                st.markdown(f"### #{idx + 1} {stock['name']} ({stock['code']})")
                
                # Price and basic info
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Current Price", 
                        f"¥{stock['current_price']:.2f}",
                        delta=f"+{stock['change_rate']}%"
                    )
                with col2:
                    st.metric("Market Cap", f"{stock['market_cap']}B CNY")
                
                # Detailed information
                with st.expander("📊 Detailed Analysis", expanded=True):
                    # Financial indicators
                    st.write("**Financial Indicators:**")
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        st.write(f"P/E: {stock['pe_ratio']}")
                    with col_f2:
                        st.write(f"P/B: {stock['pb_ratio']}")
                    with col_f3:
                        st.write(f"Revenue Growth: {stock['revenue_growth']}%")
                    
                    # Technical indicators
                    st.write("**Technical Indicators:**")
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        st.write(f"RSI: {stock['rsi']}")
                    with col_t2:
                        st.write(f"MACD: {stock['macd_signal']}")
                    with col_t3:
                        st.write(f"Bollinger: {stock['bollinger_position']}")
                    
                    # Investment recommendation
                    st.write("**Investment Recommendation:**")
                    
                    # Show different recommendation strength based on score
                    score = stock['recommend_score']
                    if score >= 90:
                        st.success("🚀 Strong Buy - Excellent overall score")
                    elif score >= 80:
                        st.info("📈 Recommended Buy - Good overall score")
                    elif score >= 70:
                        st.warning("🤔 Cautious Buy - Average overall score")
                    else:
                        st.error("⏸️ Watch - Need more signals")
                    
                    # Specific reasons
                    reasons = []
                    if stock['pe_ratio'] < 20:
                        reasons.append("Reasonable valuation")
                    if stock['profit_growth'] > 15:
                        reasons.append("High growth potential")
                    if 'Leader' in str(stock['tags']):
                        reasons.append("Industry leader position")
                    if stock['macd_signal'] == 'Golden Cross':
                        reasons.append("Technical golden cross signal")
                    
                    if reasons:
                        st.write("**Reasons:** " + ", ".join(reasons))
                    
                    # Risk warning
                    if stock['risk_level'] == 'High':
                        st.error(f"⚠️ Risk Level: {stock['risk_level']}")
                    elif stock['risk_level'] == 'Medium':
                        st.warning(f"⚠️ Risk Level: {stock['risk_level']}")
                    else:
                        st.success(f"✅ Risk Level: {stock['risk_level']}")
                
                st.markdown("---")
else:
    st.warning("No stocks found matching the filter criteria. Please adjust your filters.")

# Data visualization section
st.markdown("---")
st.subheader("📈 Market Overview")

if len(recommended_stocks) > 0:
    # Create three charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # P/E ratio distribution
        fig_pe = px.bar(
            recommended_stocks.head(5),
            x='name',
            y='pe_ratio',
            title='TOP5 P/E Ratio Comparison',
            color='pe_ratio',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_pe, use_container_width=True)
    
    with col2:
        # Growth comparison
        fig_growth = go.Figure(data=[
            go.Bar(name='Revenue Growth', x=recommended_stocks.head(5)['name'], 
                   y=recommended_stocks.head(5)['revenue_growth']),
            go.Bar(name='Profit Growth', x=recommended_stocks.head(5)['name'], 
                   y=recommended_stocks.head(5)['profit_growth'])
        ])
        fig_growth.update_layout(title='TOP5 Growth Comparison', barmode='group')
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col3:
        # Recommendation score radar chart
        top_stock = recommended_stocks.iloc[0]
        categories = ['Valuation', 'Growth', 'Technical', 'Position', 'Overall']
        values = [
            max(0, 100 - (top_stock['pe_ratio'] - 15) * 3),  # Valuation score
            min(100, top_stock['profit_growth'] * 4),        # Growth score
            75 if top_stock['macd_signal'] == 'Golden Cross' else 50, # Technical score
            90 if 'Leader' in str(top_stock['tags']) else 60,   # Position score
            top_stock['recommend_score']                      # Overall score
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
            title=f"{top_stock['name']} Multi-dimensional Analysis"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# Investment strategy suggestions
st.markdown("---")
st.subheader("💡 Investment Strategy Suggestions")

strategy_cols = st.columns(2)

with strategy_cols[0]:
    st.markdown(f"""
    ### 🎯 Current Market Suggestions
    
    **Based on your risk tolerance:** `{risk_tolerance}`
    
    - **Position Allocation:** Recommend { "70-80%" if risk_tolerance in ["Growth", "Aggressive"] else "50-60%" } allocation
    - **Holding Period:** { "6-12" if risk_tolerance in ["Growth", "Aggressive"] else "12-24" } months
    - **Focus Areas:** { selected_sector if selected_sector != "All" else "Consumer, New Energy" } sector
    - **Risk Control:** Single stock not exceeding { 20 if risk_tolerance in ["Growth", "Aggressive"] else 15 }% of total portfolio
    """)

with strategy_cols[1]:
    st.markdown("""
    ### 📋 Important Notes
    
    **Technical Analysis Reminders:**
    - MACD golden cross signals need volume confirmation
    - RSI above 70 indicates potential short-term correction
    - Watch for valid Bollinger Band breakouts
    
    **Fundamental Analysis Reminders:**
    - High P/E stocks require higher growth support
    - Pay attention to quarterly earnings release dates
    - Monitor industry policy changes
    
    **Risk Warning:** Stock market involves risks, invest carefully
    """)

# Quick filter buttons
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Filters")

quick_filter_cols = st.sidebar.columns(2)

with quick_filter_cols[0]:
    if st.button("Consumer Leaders", use_container_width=True):
        st.session_state.sector_filter = "Consumer"
        st.rerun()

with quick_filter_cols[1]:
    if st.button("Low Valuation", use_container_width=True):
        st.session_state.max_pe = 15
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Sector Distribution")

sector_quick_cols = st.sidebar.columns(2)

sectors_quick = ["New Energy", "Financial", "Home Appliances", "Technology"]
for sector in sectors_quick:
    col = sector_quick_cols[sectors_quick.index(sector) % 2]
    with col:
        if st.button(sector, use_container_width=True):
            st.session_state.sector_filter = sector
            st.rerun()

# Disclaimer
with st.sidebar.expander("⚠️ Disclaimer"):
    st.markdown("""
    This system is for technical demonstration only and does not constitute investment advice.
    
    **Data Information:**
    - Stock data is simulated
    - Recommendation algorithm is for demonstration only
    - Actual investments should refer to professional advice
    
    **Risk Warning:**
    - Stock market involves risks
    - Past performance does not indicate future returns
    - Investment decisions require comprehensive consideration
    """)

# Initialize session state
if 'sector_filter' not in st.session_state:
    st.session_state.sector_filter = "All"
if 'max_pe' not in st.session_state:
    st.session_state.max_pe = 50

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>A-Share Stock Recommendation System | Technical Analysis Tool</p>
    <p>Arts & Advanced Big Data | Week 10 - Open API Integration</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | 2024</p>
    <p>Data for reference only, not investment advice</p>
    </div>
    """,
    unsafe_allow_html=True
)

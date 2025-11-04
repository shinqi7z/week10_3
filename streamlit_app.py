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
    page_title="US Stock Recommendation System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("📈 US Stock Recommendation System")
st.markdown("""
### Easy-to-understand stock analysis tool for beginners
**Intelligent recommendation system based on technical indicators and fundamentals**
""")

class USStockRecommender:
    def __init__(self):
        # Sample data for major US stocks
        self.stocks_data = self.generate_sample_data()
        
    def generate_sample_data(self):
        """Generate sample stock data for US market"""
        stocks = [
            {
                'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology',
                'current_price': 185.20, 'change_rate': 2.15,
                'volume': 45.8, 'market_cap': 2850,
                'pe_ratio': 31.2, 'pb_ratio': 38.5,
                'revenue_growth': 2.1, 'profit_growth': 5.8,
                'rsi': 58.3, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 85.5, 'risk_level': 'Low',
                'tags': ['Tech Giant', 'Strong Brand', 'Cash Rich']
            },
            {
                'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology',
                'current_price': 420.72, 'change_rate': 1.89,
                'volume': 28.3, 'market_cap': 3120,
                'pe_ratio': 36.8, 'pb_ratio': 13.2,
                'revenue_growth': 17.6, 'profit_growth': 26.8,
                'rsi': 62.1, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 91.2, 'risk_level': 'Low',
                'tags': ['Cloud Leader', 'AI Innovation', 'Enterprise Focus']
            },
            {
                'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology',
                'current_price': 175.35, 'change_rate': 3.42,
                'volume': 32.1, 'market_cap': 2200,
                'pe_ratio': 26.4, 'pb_ratio': 6.8,
                'revenue_growth': 11.2, 'profit_growth': 23.4,
                'rsi': 59.7, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 87.8, 'risk_level': 'Low-Medium',
                'tags': ['Search Dominance', 'AI Leadership', 'Diversified Revenue']
            },
            {
                'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Cyclical',
                'current_price': 178.22, 'change_rate': 2.78,
                'volume': 38.9, 'market_cap': 1830,
                'pe_ratio': 62.3, 'pb_ratio': 8.9,
                'revenue_growth': 13.2, 'profit_growth': 228.9,
                'rsi': 63.5, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 83.4, 'risk_level': 'Medium',
                'tags': ['E-commerce Leader', 'AWS Cloud', 'Logistics Powerhouse']
            },
            {
                'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'sector': 'Technology',
                'current_price': 950.02, 'change_rate': 4.56,
                'volume': 52.7, 'market_cap': 2350,
                'pe_ratio': 76.8, 'pb_ratio': 49.2,
                'revenue_growth': 265.3, 'profit_growth': 586.8,
                'rsi': 68.9, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Upper Band',
                'recommend_score': 88.9, 'risk_level': 'High',
                'tags': ['AI Chip Leader', 'High Growth', 'Market Dominance']
            },
            {
                'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Consumer Cyclical',
                'current_price': 245.18, 'change_rate': -1.23,
                'volume': 98.5, 'market_cap': 780,
                'pe_ratio': 72.4, 'pb_ratio': 11.3,
                'revenue_growth': 3.5, 'profit_growth': -24.8,
                'rsi': 45.2, 'macd_signal': 'Death Cross', 'bollinger_position': 'Lower Band',
                'recommend_score': 62.3, 'risk_level': 'High',
                'tags': ['EV Pioneer', 'Innovation Focus', 'Volatile Stock']
            },
            {
                'symbol': 'JPM', 'name': 'JPMorgan Chase', 'sector': 'Financial Services',
                'current_price': 198.45, 'change_rate': 0.85,
                'volume': 12.8, 'market_cap': 570,
                'pe_ratio': 11.8, 'pb_ratio': 1.8,
                'revenue_growth': 15.3, 'profit_growth': 6.2,
                'rsi': 52.1, 'macd_signal': 'Approaching Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 78.6, 'risk_level': 'Low',
                'tags': ['Banking Leader', 'Strong Dividend', 'Stable']
            },
            {
                'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'sector': 'Healthcare',
                'current_price': 157.89, 'change_rate': 0.45,
                'volume': 8.9, 'market_cap': 380,
                'pe_ratio': 15.2, 'pb_ratio': 5.8,
                'revenue_growth': 6.8, 'profit_growth': 18.9,
                'rsi': 48.7, 'macd_signal': 'Approaching Golden Cross', 'bollinger_position': 'Lower Band',
                'recommend_score': 75.4, 'risk_level': 'Low',
                'tags': ['Healthcare Giant', 'Dividend Aristocrat', 'Defensive']
            },
            {
                'symbol': 'V', 'name': 'Visa Inc.', 'sector': 'Financial Services',
                'current_price': 279.34, 'change_rate': 1.23,
                'volume': 10.2, 'market_cap': 560,
                'pe_ratio': 32.1, 'pb_ratio': 14.8,
                'revenue_growth': 9.8, 'profit_growth': 17.2,
                'rsi': 56.3, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 82.7, 'risk_level': 'Low-Medium',
                'tags': ['Payment Leader', 'Recurring Revenue', 'Global Network']
            },
            {
                'symbol': 'WMT', 'name': 'Walmart Inc.', 'sector': 'Consumer Defensive',
                'current_price': 67.45, 'change_rate': 0.78,
                'volume': 15.3, 'market_cap': 540,
                'pe_ratio': 31.8, 'pb_ratio': 5.9,
                'revenue_growth': 5.7, 'profit_growth': 32.8,
                'rsi': 54.2, 'macd_signal': 'Golden Cross', 'bollinger_position': 'Middle Band',
                'recommend_score': 79.2, 'risk_level': 'Low',
                'tags': ['Retail Giant', 'E-commerce Growth', 'Stable Business']
            }
        ]
        return pd.DataFrame(stocks)
    
    def calculate_recommendation_score(self, row):
        """Calculate recommendation score (simulated algorithm)"""
        score = 0
        
        # Valuation factors (25%)
        if row['pe_ratio'] < 15:
            score += 25
        elif row['pe_ratio'] < 25:
            score += 22
        elif row['pe_ratio'] < 35:
            score += 18
        elif row['pe_ratio'] < 50:
            score += 15
        else:
            score += 10
        
        # Growth factors (30%)
        if row['profit_growth'] > 50:
            score += 30
        elif row['profit_growth'] > 25:
            score += 25
        elif row['profit_growth'] > 10:
            score += 20
        elif row['profit_growth'] > 0:
            score += 15
        else:
            score += 5
        
        # Technical indicators (25%)
        if row['macd_signal'] == 'Golden Cross':
            score += 20
        elif row['macd_signal'] == 'Approaching Golden Cross':
            score += 15
        else:
            score += 5
            
        if row['rsi'] > 30 and row['rsi'] < 70:
            score += 5
        
        # Market position and stability (20%)
        if any(tag in ['Leader', 'Giant', 'Dominance'] for tag in row['tags']):
            score += 15
        else:
            score += 10
            
        if row['risk_level'] in ['Low', 'Low-Medium']:
            score += 5
            
        return min(100, score)
    
    def get_recommended_stocks(self, min_market_cap=100, max_pe=100, sector_filter=None, risk_filter=None):
        """Get recommended stock list"""
        df = self.stocks_data.copy()
        
        # Apply filters
        if min_market_cap:
            df = df[df['market_cap'] >= min_market_cap]
        
        if max_pe:
            df = df[df['pe_ratio'] <= max_pe]
            
        if sector_filter and sector_filter != "All":
            df = df[df['sector'] == sector_filter]
            
        if risk_filter and risk_filter != "All":
            df = df[df['risk_level'] == risk_filter]
        
        # Calculate recommendation score
        df['recommend_score'] = df.apply(self.calculate_recommendation_score, axis=1)
        
        # Sort by score
        df = df.sort_values('recommend_score', ascending=False)
        
        return df

# Initialize recommendation system
recommender = USStockRecommender()

# Sidebar - Analysis Settings
st.sidebar.header("🔧 Analysis Settings")

# Sector filter
sectors = ["All", "Technology", "Financial Services", "Healthcare", "Consumer Cyclical", "Consumer Defensive"]
selected_sector = st.sidebar.selectbox("Sector Filter", sectors, index=0)

# Risk level filter
risk_levels = ["All", "Low", "Low-Medium", "Medium", "High"]
selected_risk = st.sidebar.selectbox("Risk Level Filter", risk_levels, index=0)

# Valuation filter
min_market_cap = st.sidebar.number_input(
    "Minimum Market Cap (Billion USD)", 
    min_value=0, 
    max_value=5000, 
    value=100,
    step=50
)

max_pe = st.sidebar.slider(
    "Maximum P/E Ratio", 
    min_value=0, 
    max_value=200, 
    value=100
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
    sector_filter=selected_sector,
    risk_filter=selected_risk if selected_risk != "All" else None
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
                st.markdown(f"### #{idx + 1} {stock['name']} ({stock['symbol']})")
                
                # Price and basic info
                col1, col2 = st.columns(2)
                with col1:
                    change_color = "normal" if stock['change_rate'] >= 0 else "inverse"
                    st.metric(
                        "Current Price", 
                        f"${stock['current_price']:.2f}",
                        delta=f"{stock['change_rate']}%",
                        delta_color=change_color
                    )
                with col2:
                    st.metric("Market Cap", f"${stock['market_cap']}B")
                
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
                        reasons.append("Attractive valuation")
                    elif stock['pe_ratio'] < 35:
                        reasons.append("Reasonable valuation")
                        
                    if stock['profit_growth'] > 20:
                        reasons.append("Strong growth")
                    elif stock['profit_growth'] > 10:
                        reasons.append("Solid growth")
                        
                    if 'Leader' in str(stock['tags']) or 'Giant' in str(stock['tags']):
                        reasons.append("Market leader")
                        
                    if stock['macd_signal'] == 'Golden Cross':
                        reasons.append("Technical bullish signal")
                    
                    if reasons:
                        st.write("**Reasons:** " + ", ".join(reasons))
                    
                    # Risk warning
                    risk_color = {
                        'Low': 'green',
                        'Low-Medium': 'blue', 
                        'Medium': 'orange',
                        'High': 'red'
                    }.get(stock['risk_level'], 'gray')
                    
                    st.write(f"**Risk Level:** :{risk_color}[{stock['risk_level']}]")
                    
                    # Company tags
                    st.write("**Key Attributes:**")
                    tags_html = " ".join([f"`{tag}`" for tag in stock['tags']])
                    st.markdown(tags_html)
                
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
            recommended_stocks.head(6),
            x='symbol',
            y='pe_ratio',
            title='TOP 6 P/E Ratio Comparison',
            color='pe_ratio',
            color_continuous_scale='Viridis'
        )
        fig_pe.update_layout(xaxis_title="Stock Symbol", yaxis_title="P/E Ratio")
        st.plotly_chart(fig_pe, use_container_width=True)
    
    with col2:
        # Growth comparison
        fig_growth = go.Figure(data=[
            go.Bar(name='Revenue Growth', x=recommended_stocks.head(6)['symbol'], 
                   y=recommended_stocks.head(6)['revenue_growth']),
            go.Bar(name='Profit Growth', x=recommended_stocks.head(6)['symbol'], 
                   y=recommended_stocks.head(6)['profit_growth'])
        ])
        fig_growth.update_layout(
            title='TOP 6 Growth Comparison', 
            barmode='group',
            xaxis_title="Stock Symbol",
            yaxis_title="Growth Rate (%)"
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col3:
        # Recommendation score radar chart
        top_stock = recommended_stocks.iloc[0]
        categories = ['Valuation', 'Growth', 'Technical', 'Position', 'Overall']
        values = [
            max(0, 100 - (top_stock['pe_ratio'] - 15) * 2),  # Valuation score
            min(100, top_stock['profit_growth'] * 2),        # Growth score
            80 if top_stock['macd_signal'] == 'Golden Cross' else 50, # Technical score
            90 if any(tag in ['Leader', 'Giant'] for tag in top_stock['tags']) else 60,   # Position score
            top_stock['recommend_score']                      # Overall score
        ]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=top_stock['symbol']
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title=f"{top_stock['symbol']} Multi-dimensional Analysis"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
    # Sector distribution
    st.markdown("---")
    st.subheader("🏢 Sector Distribution")
    
    sector_counts = recommended_stocks['sector'].value_counts()
    fig_sector = px.pie(
        values=sector_counts.values,
        names=sector_counts.index,
        title="Recommended Stocks by Sector"
    )
    st.plotly_chart(fig_sector, use_container_width=True)

# Investment strategy suggestions
st.markdown("---")
st.subheader("💡 Investment Strategy Suggestions")

strategy_cols = st.columns(2)

with strategy_cols[0]:
    allocation_map = {
        "Conservative": "30-40%",
        "Moderate": "50-60%", 
        "Balanced": "60-70%",
        "Growth": "70-80%",
        "Aggressive": "80-90%"
    }
    
    period_map = {
        "Conservative": "24-36",
        "Moderate": "18-24", 
        "Balanced": "12-18",
        "Growth": "6-12",
        "Aggressive": "3-6"
    }
    
    single_stock_map = {
        "Conservative": "10",
        "Moderate": "15", 
        "Balanced": "20",
        "Growth": "25",
        "Aggressive": "30"
    }
    
    st.markdown(f"""
    ### 🎯 Current Market Suggestions
    
    **Based on your risk tolerance:** `{risk_tolerance}`
    
    - **Position Allocation:** Recommend {allocation_map[risk_tolerance]} allocation
    - **Holding Period:** {period_map[risk_tolerance]} months
    - **Focus Areas:** {selected_sector if selected_sector != "All" else "Technology, Financial Services"} sector
    - **Risk Control:** Single stock not exceeding {single_stock_map[risk_tolerance]}% of total portfolio
    - **Diversification:** Minimum {3 if risk_tolerance in ["Growth", "Aggressive"] else 5} different stocks
    """)

with strategy_cols[1]:
    st.markdown("""
    ### 📋 Important Notes
    
    **Technical Analysis Reminders:**
    - MACD golden cross signals need volume confirmation
    - RSI above 70 indicates potential short-term correction
    - Watch for valid Bollinger Band breakouts
    - Consider overall market trend and sector rotation
    
    **Fundamental Analysis Reminders:**
    - High P/E stocks require higher growth support
    - Pay attention to quarterly earnings release dates
    - Monitor Fed policy changes and interest rates
    - Consider geopolitical and macroeconomic factors
    
    **Risk Warning:** Stock market involves risks, invest carefully. Past performance doesn't guarantee future results.
    """)

# Quick filter buttons
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Filters")

quick_filter_cols = st.sidebar.columns(2)

with quick_filter_cols[0]:
    if st.button("Tech Leaders", use_container_width=True):
        st.session_state.sector_filter = "Technology"
        st.rerun()

with quick_filter_cols[1]:
    if st.button("Low Risk", use_container_width=True):
        st.session_state.risk_filter = "Low"
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Popular Sectors")

sector_quick_cols = st.sidebar.columns(2)

sectors_quick = ["Technology", "Financial Services", "Healthcare", "Consumer Cyclical"]
for sector in sectors_quick:
    col = sector_quick_cols[sectors_quick.index(sector) % 2]
    with col:
        if st.button(sector, use_container_width=True):
            st.session_state.sector_filter = sector
            st.rerun()

# Market sentiment indicator
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Market Sentiment")

current_sentiment = "🟢 Bullish" if len(recommended_stocks) > 5 else "🟡 Neutral" if len(recommended_stocks) > 2 else "🔴 Cautious"
st.sidebar.metric("Overall Sentiment", current_sentiment)

avg_score = recommended_stocks['recommend_score'].mean() if len(recommended_stocks) > 0 else 0
st.sidebar.metric("Average Score", f"{avg_score:.1f}")

# Disclaimer
with st.sidebar.expander("⚠️ Disclaimer"):
    st.markdown("""
    This system is for technical demonstration only and does not constitute investment advice.
    
    **Data Information:**
    - Stock data is simulated for demonstration
    - Recommendation algorithm is for educational purposes
    - Actual investments should refer to professional financial advice
    - Prices and metrics are not real-time
    
    **Risk Warning:**
    - Stock market involves significant risks
    - Past performance does not indicate future returns
    - Investment decisions require comprehensive research
    - Diversification is essential for risk management
    """)

# Initialize session state
if 'sector_filter' not in st.session_state:
    st.session_state.sector_filter = "All"
if 'risk_filter' not in st.session_state:
    st.session_state.risk_filter = "All"
if 'max_pe' not in st.session_state:
    st.session_state.max_pe = 100

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>US Stock Recommendation System | Technical Analysis Tool</p>
    <p>Arts & Advanced Big Data | Week 10 - Open API Integration</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | 2024</p>
    <p>Data for demonstration only, not investment advice</p>
    </div>
    """,
    unsafe_allow_html=True
)

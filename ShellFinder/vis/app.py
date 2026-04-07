"""
ShellFinder Web Dashboard
基于 Streamlit 的数据可视化界面
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from database import Database
from parser import DataParser
from config import Config


def init_session_state():
    """初始化 session state"""
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'parser' not in st.session_state:
        st.session_state.parser = DataParser()


@st.cache_data(ttl=300)  # 缓存 5 分钟
def load_data():
    """加载数据"""
    db = Database()
    conn = db._get_connection()
    df = pd.read_sql_query("SELECT * FROM repositories", conn)
    conn.close()
    return df


@st.cache_data(ttl=300)
def get_statistics():
    """获取统计数据"""
    db = Database()
    return db.get_statistics()


def render_overview(df: pd.DataFrame, stats: dict):
    """渲染概览页面"""
    st.title("🦀 ShellFinder Dashboard")
    st.markdown("---")

    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 总仓库数",
            value=len(df),
            delta=None
        )

    with col2:
        avg_stars = stats.get('avg_stars', 0)
        st.metric(
            label="⭐ 平均 Stars",
            value=f"{avg_stars:,.0f}",
            delta=None
        )

    with col3:
        quality_rate = stats.get('quality_rate', 0)
        st.metric(
            label="✨ 质量达标率",
            value=f"{quality_rate}%",
            delta=None
        )

    with col4:
        languages = stats.get('by_language', {})
        st.metric(
            label="💻 覆盖语言",
            value=len(languages),
            delta=None
        )

    st.markdown("---")


def render_language_distribution(df: pd.DataFrame):
    """渲染语言分布图"""
    st.subheader("💻 编程语言分布")

    lang_counts = df['language'].value_counts().head(15)

    col1, col2 = st.columns(2)

    with col1:
        # 饼图
        fig_pie = px.pie(
            values=lang_counts.values,
            names=lang_counts.index,
            title='语言占比',
            hole=0.3
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # 柱状图
        fig_bar = px.bar(
            x=lang_counts.index,
            y=lang_counts.values,
            title='仓库数量',
            labels={'x': '语言', 'y': '数量'},
            color=lang_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)


def render_stars_analysis(df: pd.DataFrame):
    """渲染 Stars 分析"""
    st.subheader("⭐ Stars 分析")

    # Stars 分布直方图
    fig = px.histogram(
        df,
        x='stars',
        nbins=50,
        title='Stars 分布',
        labels={'stars': 'Stars 数量', 'count': '仓库数量'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Top 20 仓库
    st.subheader("🏆 Top 20 仓库（按 Stars）")
    top20 = df.nlargest(20, 'stars')[['full_name', 'description', 'stars', 'language', 'url']]

    for idx, row in top20.iterrows():
        with st.expander(f"⭐ {row['stars']:,} - {row['full_name']} ({row['language']})"):
            st.markdown(f"**描述**: {row['description'] or '无描述'}")
            st.markdown(f"**链接**: [{row['url']}]({row['url']})")


def render_temporal_analysis(df: pd.DataFrame):
    """渲染时间序列分析"""
    st.subheader("📅 时间分析")

    # 转换时间列
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    col1, col2 = st.columns(2)

    with col1:
        # 创建时间分布
        df['created_year'] = df['created_at'].dt.year
        year_counts = df['created_year'].value_counts().sort_index()

        fig = px.line(
            x=year_counts.index,
            y=year_counts.values,
            title='仓库创建时间分布',
            labels={'x': '年份', 'y': '数量'},
            markers=True
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 最近更新时间
        df['updated_month'] = df['updated_at'].dt.to_period('M')
        month_counts = df['updated_month'].value_counts().sort_index().tail(12)

        fig = px.bar(
            x=month_counts.index.astype(str),
            y=month_counts.values,
            title='最近 12 个月更新活跃度',
            labels={'x': '月份', 'y': '更新数量'}
        )
        fig.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


def render_repository_table(df: pd.DataFrame):
    """渲染仓库数据表"""
    st.subheader("📋 仓库数据表")

    # 筛选选项
    col1, col2, col3 = st.columns(3)

    with col1:
        language_filter = st.selectbox(
            '筛选语言',
            ['全部'] + list(df['language'].unique())
        )

    with col2:
        min_stars = st.number_input(
            '最小 Stars',
            min_value=0,
            max_value=int(df['stars'].max()),
            value=0
        )

    with col3:
        search_term = st.text_input('搜索仓库名称')

    # 应用筛选
    filtered_df = df.copy()

    if language_filter != '全部':
        filtered_df = filtered_df[filtered_df['language'] == language_filter]

    if min_stars > 0:
        filtered_df = filtered_df[filtered_df['stars'] >= min_stars]

    if search_term:
        filtered_df = filtered_df[
            filtered_df['full_name'].str.contains(search_term, case=False, na=False)
        ]

    st.markdown(f"**找到 {len(filtered_df)} 个仓库**")

    # 显示数据表
    display_cols = ['full_name', 'language', 'stars', 'forks', 'description', 'url']
    st.dataframe(
        filtered_df[display_cols],
        column_config={
            'full_name': st.column_config.TextColumn('仓库名称'),
            'language': st.column_config.TextColumn('语言'),
            'stars': st.column_config.NumberColumn('⭐ Stars', format='%d'),
            'forks': st.column_config.NumberColumn('🍴 Forks', format='%d'),
            'description': st.column_config.TextColumn('描述', width='large'),
            'url': st.column_config.LinkColumn('链接')
        },
        use_container_width=True,
        height=400
    )


def render_quality_report():
    """渲染质量报告"""
    st.subheader("📊 数据质量报告")

    parser = DataParser()
    report = parser.get_quality_report()

    # 概览指标
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "平均描述长度",
            f"{report['quality_metrics']['avg_description_length']} 字符"
        )

    with col2:
        st.metric(
            "README 覆盖率",
            f"{report['quality_metrics']['readme_rate']}%"
        )

    with col3:
        st.metric(
            "活跃仓库比例 (30天)",
            f"{report['quality_metrics']['active_rate_30d']}%"
        )

    # 改进建议
    if report['recommendations']:
        st.markdown("### 💡 改进建议")
        for rec in report['recommendations']:
            st.markdown(f"- {rec}")


def render_ai_matching_interface(df: pd.DataFrame):
    """渲染 AI 匹配界面（预留接口）"""
    st.subheader("🤖 智能模板匹配")

    st.markdown("""
    这个功能将在后续版本中实现，用于：
    - 根据用户需求智能匹配最合适的模板
    - 基于技术栈进行相似度计算
    - 提供个性化的仓库推荐
    """)

    # 示例界面
    user_input = st.text_area(
        "描述你的需求（例如：我想创建一个 React + FastAPI 的博客系统）",
        placeholder="在这里输入你的需求...",
        height=100
    )

    if st.button("🔍 匹配模板", type="primary"):
        if user_input:
            st.info("🚧 AI 匹配功能正在开发中... 敬请期待！")
        else:
            st.warning("请先输入你的需求")


def main():
    """主函数"""
    st.set_page_config(
        page_title="ShellFinder Dashboard",
        page_icon="🦀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()

    # 侧边栏
    with st.sidebar:
        st.title("🦀 ShellFinder")
        st.markdown("---")

        page = st.radio(
            "选择页面",
            [
                "📊 概览",
                "💻 语言分布",
                "⭐ Stars 分析",
                "📅 时间分析",
                "📋 数据表",
                "📊 质量报告",
                "🤖 AI 匹配"
            ]
        )

        st.markdown("---")
        st.markdown("### 📈 数据统计")
        stats = get_statistics()
        st.caption(f"总仓库: {stats['total_repos']}")
        st.caption(f"平均 Stars: {stats['avg_stars']:.0f}")
        st.caption(f"质量率: {stats['quality_rate']}%")

        st.markdown("---")
        st.markdown(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 加载数据
    with st.spinner("加载数据中..."):
        df = load_data()

    if len(df) == 0:
        st.error("📭 数据库中没有数据！请先运行爬虫：")
        st.code("python main.py --awesome")
        return

    # 根据选择渲染不同页面
    if page == "📊 概览":
        render_overview(df, stats)
        render_quality_report()

    elif page == "💻 语言分布":
        render_language_distribution(df)

    elif page == "⭐ Stars 分析":
        render_stars_analysis(df)

    elif page == "📅 时间分析":
        render_temporal_analysis(df)

    elif page == "📋 数据表":
        render_repository_table(df)

    elif page == "📊 质量报告":
        render_quality_report()

    elif page == "🤖 AI 匹配":
        render_ai_matching_interface(df)


if __name__ == "__main__":
    main()

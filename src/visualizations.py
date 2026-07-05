import plotly.express as px
import plotly.graph_objects as go

BLUE_PALETTE = ['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#2563EB', '#1D4ED8', '#1E40AF', '#1E3A8A']

def apply_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8', family="Inter, -apple-system, sans-serif", size=13),
        title=dict(
            font=dict(size=24, color='#F8FAFC', family="Inter, -apple-system, sans-serif"),
            x=0.02,
            y=0.95
        ),
        xaxis=dict(
            showgrid=False, 
            zeroline=False, 
            color='#64748B',
            showline=True,
            linewidth=1,
            linecolor='#334155',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#1E293B', 
            zeroline=False, 
            color='#64748B', 
            gridwidth=1,
            showline=False,
            tickfont=dict(size=12)
        ),
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.9)',
            bordercolor='#334155',
            borderwidth=1,
            font=dict(color='#CBD5E1', size=12),
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        height=420,
        hovermode="closest"
    )
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=14,
            font_family="Inter, -apple-system, sans-serif",
            bordercolor="#3B82F6"
        )
    )
    return fig

def plot_bar(df, x, y, title, color=None, horizontal=False):
    if horizontal:
        fig = px.bar(df, x=y, y=x, title=title,
                     orientation='h',
                     color_discrete_sequence=['#3B82F6'])
    else:
        fig = px.bar(df, x=x, y=y, title=title,
                     color=color,
                     color_discrete_sequence=BLUE_PALETTE)
    return apply_theme(fig)

def plot_pie(df, names, values, title):
    fig = px.pie(df, names=names, values=values,
                 title=title,
                 color_discrete_sequence=BLUE_PALETTE)
    return apply_theme(fig)

def plot_heatmap(pivot_df, title):
    fig = px.imshow(
        pivot_df,
        title=title,
        color_continuous_scale="Blues",
        aspect="auto",
        labels=dict(x="Day of Week", y="Hour of Day", color="Transactions")
    )
    return apply_theme(fig)

def plot_line(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title,
                  markers=True,
                  color_discrete_sequence=['#3B82F6'])
    return apply_theme(fig)

def plot_treemap(df, path, values, title):
    fig = px.treemap(df, path=path, values=values, title=title,
                     color_discrete_sequence=BLUE_PALETTE)
    fig.update_traces(root_color="lightgrey")
    return apply_theme(fig)

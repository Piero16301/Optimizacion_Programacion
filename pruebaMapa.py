import plotly.graph_objects as go

mapbox_access_token = 'pk.eyJ1IjoicGllcm8xNjMwMSIsImEiOiJja3VzbDgwbWE1Zzg0MzBxajFtN2tzcDVtIn0.Xlc1UX7d_VVo4LzfmKhumw'

fig = go.Figure(go.Scattermapbox(
    lat=['-12.2237411', '-11.8869804', '-12.0620094'],
    lon=['-76.9084385', '-77.067858', '-77.0186106'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10
    ),
    text=["E/S MIGUEL ANGEL", "E/S NEOX", "E/S 28 DE JULIO"],
))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=-12.2237411,
            lon=-76.9084385
        ),
        pitch=0,
        zoom=10
    ),
)

fig.show()

import vscode

theme = vscode.ColorTheme(name='my-theme', display_name='My Theme', version='0.0.1')
theme.set_colors(
    background='#282C34',
    foreground='#1D2026',
    accent_colors=['#45C2A8', '#6EC262', '#F2B85D', '#EB5BF2']
)
vscode.build_theme(theme)

from reactpy import component, html

@component
def Title(title):
    return html.script(f'() => {{document.title = "{title}";}}')

@component
def Favicon(src):
    return html.script(f"""
        const link = document.createElement("link")
        link.rel = 'icon'
        link.type = 'image/x-icon'
        link.href = "{src}"
        document.head.appendChild(link);
    """)

@component
def Meta(meta_tags):
    return html.script(f"""
        const metaTags = {meta_tags};
        metaTags.forEach(meta => {{
            const metaElement = document.createElement("meta");
            Object.keys(meta).forEach(key => {{
                metaElement.setAttribute(key, meta[key]);
            }});
            document.head.appendChild(metaElement);
        }});
    """)
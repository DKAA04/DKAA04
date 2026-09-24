"""Usage: python package_demos.py /path/to/duck/frontend/dist"""
from pathlib import Path
import re, shutil, sys
out=Path(__file__).resolve().parent
dist=Path(sys.argv[1]).resolve()
s=(dist/'index.html').read_text()
js=next((dist/'assets').glob('*.js')); css=next((dist/'assets').glob('*.css'))
s=re.sub(r'<script type="module" crossorigin src="[^"]+"></script>',lambda m:'<script type="module">'+js.read_text().replace('</script','<\\/script')+'</script>',s)
s=re.sub(r'<link rel="stylesheet" crossorigin href="[^"]+">',lambda m:'<style>'+css.read_text()+'</style>',s)
s=s.replace('<head>',"<head><meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data: https://tile.openstreetmap.org; connect-src 'none'; base-uri 'none'; form-action 'none'\">")
s=s.replace('<body>', '<body><div style="position:fixed;top:0;left:0;right:0;z-index:9000;background:#10261f;color:#def3e9;padding:8px 16px;font:12px system-ui;line-height:1.4"><a href="./index.html" style="color:#b7ff3c">← Portfolio demos</a> · SYNTHETIC DEMO: invented records and scores · no real email, calling or enrichment.</div><style>body{padding-top:34px}.app{height:calc(100dvh - 34px)!important}</style>')
(out/'duck.html').write_text(s)
shutil.copy(dist/'duckduckgov-logo.png',out/'duckduckgov-logo.png')

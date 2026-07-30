with open('C:/Users/Lenovo/Desktop/Aurum-live-pro/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old AURUM ENGINE tab button from mode switcher
old = '  <button id="modeBtnEngine" class="mode-btn" style="flex:1;padding:10px 0;background:none;border:none;border-bottom:2px solid transparent;color:#4b5563;font-size:11px;font-weight:700;cursor:pointer;letter-spacing:0.5px;font-family:system-ui,sans-serif;">⚜ AURUM ENGINE</button>'
if old in content:
    content = content.replace(old, '')
    print('Removed AURUM ENGINE tab button')
else:
    print('Tab button not found (may already be removed)')

# Remove the engine view div (hidden)
old2 = '  <div id="engineView" style="display:none;height:calc(100vh - 41px);overflow-y:auto;background:#07090f;color:#e2e8f0;font-family:system-ui,-apple-system,sans-serif;"></div>'
if old2 in content:
    content = content.replace(old2, '')
    print('Removed engine view div')
else:
    print('Engine view div not found (may already be removed)')

with open('C:/Users/Lenovo/Desktop/Aurum-live-pro/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Cleanup done')

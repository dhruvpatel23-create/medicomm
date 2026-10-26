with open(r"D:\medullaprep\dhruv1\server.mjs", "r", encoding="utf-8") as f:
    text = f.read()

target = 'const requestedFile = /^\\/uploads\\/fmge\\/[a-zA-Z0-9_-]+\\.webp$/.test(url.pathname)\n      ? path.join("fmge", path.basename(url.pathname))\n      : path.basename(url.pathname);'

replacement = 'const requestedFile = /^\\/uploads\\/(?:fmge|grand_test)\\/[a-zA-Z0-9_-]+\\.(?:webp|jpg|jpeg|png)$/.test(url.pathname)\n      ? path.join(url.pathname.split("/")[2], path.basename(url.pathname))\n      : path.basename(url.pathname);'

if target in text:
    text = text.replace(target, replacement)
    with open(r"D:\medullaprep\dhruv1\server.mjs", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully replaced in server.mjs (LF)!")
elif target.replace('\n', '\r\n') in text:
    text = text.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))
    with open(r"D:\medullaprep\dhruv1\server.mjs", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully replaced in server.mjs (CRLF)!")
else:
    print("Could not find target in server.mjs!")

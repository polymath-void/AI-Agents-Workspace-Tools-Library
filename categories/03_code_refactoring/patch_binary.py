file_path = "/data/data/com.termux/files/home/Projects/polymath-integrated/target/release/polymath-void-agent"
with open(file_path, "rb") as f:
    data = f.read()

target = b"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
replacement = b"http://127.0.0.1:8080/generate?dummy=" + (b"a" * 56)

if len(target) != len(replacement):
    print(f"Length mismatch: {len(target)} vs {len(replacement)}")
    exit(1)

if target in data:
    new_data = data.replace(target, replacement)
    with open(file_path, "wb") as f:
        f.write(new_data)
    print("Successfully patched binary!")
else:
    print("Target string not found!")

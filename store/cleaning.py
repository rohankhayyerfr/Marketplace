import re

input_file = r"C:\Users\West\PycharmProjects\Marketplace\locale\en\LC_MESSAGES\django.po"
output_file = r"C:\Users\West\PycharmProjects\Marketplace\locale\en\LC_MESSAGES\django.po"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# الگوی یافتن هر بلوک msgid/msgstr
pattern = re.compile(r'(?:^#.*\n)*msgid ".*?"\nmsgstr ".*?"', re.DOTALL | re.MULTILINE)
blocks = pattern.findall(content)

seen = set()
clean_blocks = []

for block in blocks:
    # استخراج msgid
    msgid_match = re.search(r'msgid "(.*?)"', block, re.DOTALL)
    if msgid_match:
        msgid = msgid_match.group(1)
        if msgid not in seen:
            seen.add(msgid)
            clean_blocks.append(block)

# اضافه کردن خطوط دیگر که خارج از بلوک msgid/msgstr هستند (مثل header)
header_pattern = re.compile(r'^(.*?)(?=msgid )', re.DOTALL)
header_match = header_pattern.match(content)
header = header_match.group(1) if header_match else ''

with open(output_file, "w", encoding="utf-8") as f:
    f.write(header + "\n\n".join(clean_blocks))

print(f"پاکسازی انجام شد. خروجی در {output_file}")

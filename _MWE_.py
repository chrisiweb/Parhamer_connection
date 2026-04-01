import fitz

doc = fitz.open("Teildokument_1.pdf")
page = doc[0]   # erste problematische Seite

print("\n=== RAWDICT ===")
print(page.get_text("rawdict"))

print("\n=== BLOCKS ===")
for b in page.get_text("rawdict").get("blocks", []):
    print("BLOCK:", b.get("bbox"), "type:", b.get("type"))
    for line in b.get("lines", []):
        print("  LINE BBOX:", line.get("bbox"))
        for span in line.get("spans", []):
            print("    SPAN:", span.get("text"), "bbox:", span.get("bbox"))

print("\n=== SIMPLE TEXT ===")
print(page.get_text())
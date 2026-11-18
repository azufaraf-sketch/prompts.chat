#!/usr/bin/env python3
"""Penjana invois NHY NIAGA ENTERPRISE — ikut TEMPLATE RASMI (rujukan/TEMPLATE_RASMI_IMG_4015.jpg).

JANGAN ubah susun atur di bawah. Semua koordinat diukur terus dari gambar template rasmi
(1320 x 1878 px) dan ditukar ke A4 dengan skala S. Hanya data (JSON) yang berubah.

Guna:
  python3 buat_invois.py data/fail.json --semakan      # papar jadual semakan sahaja (tiada PDF)
  python3 buat_invois.py data/fail.json                # hasilkan PDF + PNG pratonton dalam output/
"""
import json, os, subprocess, sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, white

# ---------- FON ----------
_FONTS = {
    "LS": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "Helvetica"],
    "LSB": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "Helvetica-Bold"],
    "DV": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "Helvetica"],
    "DVB": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "Helvetica-Bold"],
}
F = {}
for k, (path, fb) in _FONTS.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(k, path)); F[k] = k
    else:
        F[k] = fb

# ---------- SKALA (px template -> pt A4) ----------
PW, PH = A4
S = 0.448
OX = (PW - 1320 * S) / 2
def X(px): return OX + px * S
def Y(py): return PH - py * S

# ---------- WARNA ----------
GREY_ROW = HexColor("#EBEBEB")
GRID = HexColor("#CFCFCF")
BOX = HexColor("#9A9A9A")
RULE = HexColor("#3A3A3A")
TEXT = HexColor("#222222")
FOOT = HexColor("#8A8A8A")
BLUE = HexColor("#1E6FD9")

# ---------- JADUAL ----------
COLS = [60, 153, 644, 752, 866, 1010, 1237]     # sempadan lajur (px)
TBL_HEAD_TOP, TBL_HEAD_BOT = 375, 428
TBL_TOP, TBL_BOT = 429, 1216                      # kawasan baris (tetap)
BARIS_TETAP = 23                                  # bilangan baris template (21 item + 2 kosong)


def money(v):
    return f"{v:,.2f}"


def qty_str(q):
    return str(int(q)) if float(q).is_integer() else f"{q:g}"


def txt(c, s, xpx, ypx, font, size, align="left", color=TEXT, maxw_px=None):
    fname = F[font]
    if maxw_px is not None:  # kecilkan fon jika teks terlalu panjang (elak terkeluar petak)
        while size > 5 and pdfmetrics.stringWidth(s, fname, size) > maxw_px * S:
            size -= 0.1
    c.setFont(fname, size); c.setFillColor(color)
    x = X(xpx)
    if align == "center": c.drawCentredString(x, Y(ypx), s)
    elif align == "right": c.drawRightString(x, Y(ypx), s)
    else: c.drawString(x, Y(ypx), s)


def rect(c, x0, y0, x1, y1, fill=None, stroke=None, lw=1):
    c.setLineWidth(lw)
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke)
    c.rect(X(x0), Y(y1), (x1 - x0) * S, (y1 - y0) * S,
           fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)


def line(c, x0, y0, x1, y1, color, lw):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(X(x0), Y(y0), X(x1), Y(y1))


def kira(data):
    items = data["items"]
    for it in items:
        it["jumlah"] = round(float(it["qty"]) * float(it["harga"]), 2)
    return items, round(sum(it["jumlah"] for it in items), 2)


def semakan(data):
    items, total = kira(data)
    print(f"SEMAKAN — {data.get('no_invois','?')}  ({data.get('tarikh','?')})")
    print(f"{'BIL':>3}  {'BUTIRAN':40s} {'QTY':>5} {'UOM':5s} {'HARGA':>9} {'JUMLAH':>10}")
    for i, it in enumerate(items, 1):
        print(f"{i:>3}  {it['butiran'][:40]:40s} {qty_str(it['qty']):>5} {it['uom']:5s} "
              f"{money(float(it['harga'])):>9} {money(it['jumlah']):>10}")
    print(f"{'':>3}  {'JUMLAH RM':>63} {money(total):>10}")


def lukis(data, out_pdf):
    items, total = kira(data)
    n_rows = max(BARIS_TETAP, len(items))
    if n_rows > 30:
        sys.exit("Lebih 30 item — pecahkan kepada 2 invois (template satu muka surat).")
    row_h = (TBL_BOT - TBL_TOP) / n_rows

    c = canvas.Canvas(out_pdf, pagesize=A4)
    c.setTitle(f"Invois {data['no_invois']}")
    c.setFillColor(white); c.rect(0, 0, PW, PH, fill=1, stroke=0)

    # --- Kepala ---
    txt(c, "NHY NIAGA ENTERPRISE", 62, 65, "LSB", 19.3, color=black)
    txt(c, "(003260805-W)", 62, 103, "LS", 10.6, color=TEXT)
    rect(c, 884, 15, 1238, 107, fill=black)
    txt(c, "INVOIS", 1061, 80, "LSB", 22.4, "center", white)
    line(c, 62, 130, 1238, 130, RULE, 1.4)

    # --- Bil kepada ---
    rect(c, 64, 168, 675, 367, stroke=BOX, lw=0.9)
    p = data.get("penerima", {})
    txt(c, "BIL KEPADA :", 88, 203, "LS", 9.4)
    txt(c, p.get("nama", "ASRAMA KASIH SAYANG"), 88, 245, "LSB", 10.1, color=black, maxw_px=570)
    alamat = p.get("alamat", ["No. 946-972, Jalan Zamrud 6,", "Taman Pekan Baru,",
                              "08000 Sungai Petani, Kedah."])
    for i, a in enumerate(alamat[:3]):
        txt(c, a, 88, 282 + i * 32, "LS", 9.7, maxw_px=570)

    # --- Maklumat invois ---
    for lbl, val, yb in [("Tarikh Invois", data["tarikh"], 197),
                         ("No. Invois", data["no_invois"], 249),
                         ("Rujukan", data.get("rujukan", "-") or "-", 300)]:
        txt(c, lbl, 701, yb, "LS", 10.8)
        txt(c, ":", 866, yb, "DV", 9.4, color=black)
        txt(c, val, 881, yb, "DV", 9.4, color=black, maxw_px=355)

    # --- Kepala jadual ---
    rect(c, COLS[0], TBL_HEAD_TOP, COLS[-1], TBL_HEAD_BOT, fill=black)
    hb = 410
    txt(c, "BIL", 107, hb, "DVB", 8.9, "center", white)
    txt(c, "BUTIRAN", 170, hb, "DVB", 8.9, "left", white)
    txt(c, "QTY", 698, hb, "DVB", 8.9, "center", white)
    txt(c, "UOM", 811, hb, "DVB", 8.9, "center", white)
    txt(c, "HARGA", 938, hb, "DVB", 8.9, "center", white)
    txt(c, "JUMLAH", 1027, hb, "DVB", 8.9, "left", white)

    # --- Baris (selang putih / kelabu) ---
    for r in range(n_rows):
        y0 = TBL_TOP + r * row_h
        rect(c, COLS[0], y0, COLS[-1], y0 + row_h, fill=GREY_ROW if r % 2 else white)
    for r in range(n_rows + 1):
        yy = TBL_TOP + r * row_h
        line(c, COLS[0], yy, COLS[-1], yy, GRID, 0.6)
    for cx in COLS:
        line(c, cx, TBL_TOP, cx, TBL_BOT, GRID, 0.6)

    fs = 7.6 if row_h >= 30 else 7.0
    for i, it in enumerate(items):
        yb = TBL_TOP + i * row_h + row_h / 2 + 6
        txt(c, str(i + 1), 106.5, yb, "DV", fs, "center")
        txt(c, it["butiran"], 167, yb, "DVB", fs, "left", black, maxw_px=COLS[2] - 167 - 8)
        txt(c, qty_str(it["qty"]), 698, yb, "DV", fs, "center")
        txt(c, it["uom"].upper(), 809, yb, "DV", fs * 0.95, "center")
        txt(c, money(float(it["harga"])), 938, yb, "DV", fs, "center")
        txt(c, money(it["jumlah"]), 1123, yb, "DV", fs, "center")

    # --- Kotak JUMLAH (hitam penuh) ---
    rect(c, 681, 1217, 1237, 1286, fill=black)
    txt(c, "JUMLAH", 710, 1262, "DVB", 11.7, "left", white)
    txt(c, "RM", 902, 1262, "DVB", 11.7, "left", white)
    txt(c, money(total), 1103, 1264, "DVB", 13.0, "center", white, maxw_px=200)

    # --- NOTA ---
    rect(c, 64, 1318, 1236, 1405, stroke=BOX, lw=0.9)
    txt(c, "NOTA", 90, 1355, "DVB", 7.8, color=black)
    nota = data.get("nota", "")
    if nota:
        txt(c, nota, 192, 1354, "DV", 6.6, maxw_px=1030)

    # --- Tandatangan (kiri) ---
    txt(c, "Sekian.", 68, 1468, "LS", 10.0)
    txt(c, "Yang Benar,", 68, 1517, "LS", 10.0)
    txt(c, "NHY NIAGA ENTERPRISE", 68, 1552, "LSB", 10.0, color=black)
    line(c, 66, 1636, 452, 1636, RULE, 0.9)
    txt(c, "Hj. Ibrahim", 68, 1672, "LS", 10.0)
    txt(c, "PENGURUS BESAR", 68, 1705, "LSB", 9.9, color=black)
    txt(c, "010-9000433", 68, 1739, "LS", 10.0)

    # --- Maklumat pembayaran (kanan) ---
    txt(c, "Maklumat Pembayaran", 753, 1468, "LSB", 9.7, color=black)
    txt(c, "Semua cek hendaklah dipalang", 753, 1509, "LS", 9.8)
    txt(c, "dan dibayar kepada:", 753, 1541, "LS", 9.8)
    txt(c, "NHY NIAGA ENTERPRISE", 753, 1591, "LSB", 9.9, color=black)
    txt(c, "Maybank No. Akaun:", 753, 1628, "LSB", 9.3, color=black)
    txt(c, "5520 5982 1273", 985, 1628, "LSB", 10.4, color=BLUE)

    # --- Kaki ---
    line(c, 62, 1795, 1238, 1795, RULE, 1.0)
    txt(c, "Barang yang dijual tidak boleh dikembalikan - Terima kasih", 650, 1823, "LS", 8.3,
        "center", FOOT)

    c.showPage(); c.save()
    return total


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    data = json.load(open(src, encoding="utf-8"))
    if "--semakan" in sys.argv:
        semakan(data); return
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, "output"); os.makedirs(outdir, exist_ok=True)
    name = f"Invois_NHY_{data['no_invois']}"
    pdf = os.path.join(outdir, name + ".pdf")
    total = lukis(data, pdf)
    try:
        subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", pdf,
                        os.path.join(outdir, name)], check=True)
    except Exception:
        pass
    semakan(data)
    print(f"\nPDF : {pdf}\nJUMLAH RM {money(total)}")


if __name__ == "__main__":
    main()

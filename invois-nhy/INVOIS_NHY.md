# INVOIS NHY NIAGA ENTERPRISE — PANDUAN TETAP UNTUK CLAUDE

> **BACA FAIL INI DULU** setiap kali pengguna sebut invois, harga, semakan, barang, atau beri gambar barang.
> Pengguna bercakap Bahasa Melayu — jawab dalam Bahasa Melayu, ringkas dan terus.

---

## 1. ALIRAN KERJA (WAJIB IKUT URUTAN)

1. **Pengguna beri maklumat** — nama barang, senarai, harga, atau **gambar barang**.
   - Jika gambar: kenal pasti setiap barang (jenama, saiz/berat, isi per kotak/guni/bundle,
     anggaran bilangan). Sebut apa yang **tidak pasti** dan tanya — jangan teka diam-diam.
2. **Beri SEMAKAN dulu** (jadual teks dalam chat sahaja):
   `BIL | BUTIRAN | QTY | UOM | HARGA | JUMLAH` + JUMLAH RM.
   - Guna `python3 invois-nhy/buat_invois.py data/<fail>.json --semakan` supaya kiraan tepat.
   - Tandakan harga yang **anggaran** (dari rekod lama) vs harga yang **disahkan pengguna**.
3. **JANGAN buat PDF invois** sehingga pengguna minta dengan jelas ("buat invois", "ok buat", "siapkan invois").
4. Bila diminta → jana PDF guna `buat_invois.py`, **lihat PNG pratonton** sebelum hantar
   (semak: tiada teks bertindih / terpotong / keluar petak, jumlah betul), kemudian hantar PDF kepada pengguna.
5. Jika pengguna betulkan nombor (cth. 6 kotak → 5 kotak) → **guna nilai TERAKHIR**.

## 2. TEMPLATE — JANGAN UBAH LANGSUNG

**Template rasmi = `rujukan/TEMPLATE_RASMI_IMG_4015.jpg`** (invois 13/11/2026, AKS-13-11-2026-46-02).
Semua susun atur sudah dikod dalam `buat_invois.py` dan telah disahkan bertindih tepat dengan gambar itu.
**Hanya ubah fail data JSON. Jangan ubah `buat_invois.py`** kecuali pengguna sendiri minta ubah template.

Ciri template (untuk semakan visual):
- A4 potret, hitam putih (kecuali no. akaun bank warna biru).
- Kiri atas: **NHY NIAGA ENTERPRISE** + `(003260805-W)`. Kanan atas: kotak hitam **INVOIS** tulisan putih. Garisan melintang di bawah.
- Kotak bergaris **BIL KEPADA :** → ASRAMA KASIH SAYANG + alamat 3 baris.
- Kanan: `Tarikh Invois :`, `No. Invois :`, `Rujukan : -`.
- Jadual: kepala hitam `BIL | BUTIRAN | QTY | UOM | HARGA | JUMLAH`; **23 baris tetap** selang putih/kelabu
  dengan garisan grid; nama barang **tebal**; nombor di tengah lajur. Baris kosong diisi sampai 23.
  (Lebih 23 item → baris dikecilkan sehingga maks 30; lebih 30 → pecah 2 invois.)
- Kotak **JUMLAH | RM | amaun** — hitam penuh, tulisan putih, di kanan bawah jadual.
- Kotak **NOTA** (teks nota pilihan, cth. "Anggaran: Kuantiti dan harga perlu disahkan sebelum invois rasmi.").
- Kiri: Sekian. / Yang Benar, / **NHY NIAGA ENTERPRISE** / garisan tandatangan / Hj. Ibrahim / **PENGURUS BESAR** / 010-9000433.
- Kanan: **Maklumat Pembayaran** / Semua cek hendaklah dipalang / dan dibayar kepada: / **NHY NIAGA ENTERPRISE** / **Maybank No. Akaun:** 5520 5982 1273 (biru).
- Kaki: garisan + "Barang yang dijual tidak boleh dikembalikan - Terima kasih" (kelabu, tengah).

### Kesilapan ChatGPT yang TIDAK BOLEH diulang
- Reka bentuk baru / tukar susun atur / tukar fon besar-kecil sesuka hati.
- Tulis teks atas PDF lama → teks bertindih, grid putus, baris kelabu terpotong.
- Kotak JUMLAH separuh putih — **mesti hitam penuh**.
- Buat invois sebelum pengguna minta; guna harga lama ganti harga yang pengguna sahkan.
- Dakwa ada fail/gambar yang sebenarnya tiada.

## 3. MAKLUMAT TETAP

| Perkara | Nilai |
|---|---|
| Pembekal | NHY NIAGA ENTERPRISE (003260805-W) |
| Pengurus | Hj. Ibrahim — PENGURUS BESAR — 010-9000433 |
| Bank | Maybank 5520 5982 1273 |
| Penerima lazim | ASRAMA KASIH SAYANG, No. 946-972, Jalan Zamrud 6, Taman Pekan Baru, 08000 Sungai Petani, Kedah. |

**No. Invois:** `AKS-dd-mm-yyyy-[minggu ISO]` dan tambah `-[siri]` jika ada (cth. `AKS-13-11-2026-46-02`).
Minggu: `date -d YYYY-MM-DD +%V`. **Sentiasa tanya/sahkan nombor siri dengan pengguna** — jangan anggap.

## 4. UOM (UNIT)

| UOM | Guna untuk |
|---|---|
| CTN | karton / kotak (sardin, santan, kicap, susu, minyak, mi segera, tepung berkotak) |
| GNI | guni (bawang, kentang, ikan bilis, bawang besar) |
| BEG | beg / guni jaring (kentang, bawang — ikut invois lama) |
| BDL | bundle (gula 1kg x 24, sup bunjut) |
| PKT | paket (bawang putih 1kg, bihun) |
| EKR | ekor — **ayam mentah** |
| PPN | papan — **telur (30 biji)** |
| UNIT | tong gas, barang satuan |

Format BUTIRAN ikut template: `Nama Jenama (saiz x bilangan)` → cth. `Santan Kara (1L x 12)`, `Bawang Merah (5kg)`.

## 5. CARA JANA INVOIS

```bash
cd invois-nhy
# 1. Salin fail data contoh, isi tarikh, no_invois, nota, items (qty, uom, harga) — jumlah dikira automatik
cp data/AKS-13-11-2026-46-02.json data/AKS-<dd-mm-yyyy-minggu>.json
# 2. Semakan
python3 buat_invois.py data/AKS-....json --semakan
# 3. Bila pengguna minta invois
python3 buat_invois.py data/AKS-....json      # → output/Invois_NHY_<no>.pdf + .png pratonton
```
Selepas jana: buka PNG, semak visual, kemudian hantar PDF (SendUserFile). Commit + push data & PDF.

## 6. REKOD HARGA (rujukan — harga pengguna sentiasa menang)

### 18/11/2026 — DISAHKAN pengguna (AKS-18-11-2026-47, JUMLAH RM992.00; siri 47 belum disahkan)
| Barang | QTY | UOM | Harga |
|---|---|---|---|
| Sardin Pertima (425g x 24) | 5 | CTN | 144.00 |
| Kentang (8kg) | 4 | GNI | 14.00 |
| Bawang India (9kg) | 4 | GNI | 26.00 |
| Bawang Putih (3.5kg) | 2 | GNI | 24.00 |
| Sup Bunjut Adabi (24 pek) | 2 | BDL | 32.00 |

### 13/11/2026 — AKS-13-11-2026-46-02 (nota: anggaran), JUMLAH RM4,213.00
Tong Gas 14kg 27.00/UNIT · Santan Kara 1L x12 182.00/CTN · Ayam mentah 18.00/EKR · Bawang Merah 5kg 35.00/GNI ·
Tepung Beras 1kg x10 42.00/CTN · Ikan Bilis Kopek 10kg 175.00/GNI · Susu Cair Tarik 390g x48 135.00/CTN ·
Kicap Mudim 900g x12 67.00/CTN · Kentang 8kg 18.00/BEG · Cili Kering 10kg 176.00/CTN · Biskut ORI Marie 3kg 55.00/CTN ·
Tepung Gandum Rose 1kg x12 26.00/CTN · Gula 1kg x24 68.40/BDL · Bawang Putih 1kg 8.00/PKT · Sos Cili Mudim 900g x12 67.00/CTN ·
Bihun Siti 4.5kg 19.80/PKT · Susu Pekat Johan 500g x48 129.00/CTN · Minyak Masak 2kg x6 72.00/CTN ·
Bawang Besar 9kg 26.00/GNI · Tepung Jagung Cap Bintang 400g x20 55.00/CTN · Mi Segera Pelbagai Perisa 45.00/CTN

### Harga lama (anggaran sahaja)
- 24/05/2026: Sardin 155.00/CTN (anggaran)
- 09/10/2026: Bawang India ±9kg 27.00/BEG · Bawang putih guni kecil 27.00/GNI · Kentang China 8kg 14.50/BEG
- 16/10/2026: Beras 10kg 30.00 · Bihun 5kg 28.00 · Telur Gred A 13.00/PPN · Ikan bilis 10kg 169.00 · Bawang besar 5kg 22.00 · Bawang putih 5kg 42.00 · Kentang 5kg 15.50
- 20/10/2026: Bawang merah 3kg 21.00/BEG

Selepas setiap invois baru yang disahkan, **tambah harga ke bahagian ini**.

## 7. FAIL

| Fail | Isi |
|---|---|
| `buat_invois.py` | Penjana PDF (template terkunci) |
| `data/*.json` | Data setiap invois |
| `output/` | PDF + PNG pratonton |
| `rujukan/TEMPLATE_RASMI_IMG_4015.jpg` | **Template rasmi** |
| `rujukan/IMG_4014.jpeg` | Gambar barang 18/11 (sardin, bawang, kentang, sup bunjut) |

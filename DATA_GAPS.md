# DATA_GAPS

Everything below is either missing from the supplier material, uncertain, or a decision I made that you should confirm.
Nothing here was filled with invented data.

**Dataset:** 15 brands · 316 products (69 equipment / 247 material) · 38 downloadable documents.
18 products have no usable photo (branded placeholder tile is shown); 133 have no spec table (the source gives none); 9 have no datasheet (promo-image-only brands and series-level JJ Tools entries).

## 1. Missing assets
- **Brand logos not supplied** for: DISC, FDT Resin, IMT Metal Powder, LUSTRA, PHT. A text wordmark is shown instead. Denpark and Yamahachi logos were cropped from their catalogue PDFs (Yamahachi is a vector crop of the cover). Please send official logo files.
- **Products without a photo:** Carbide Drills (jj-tools); CBN Series End Mills (jj-tools); E Series Heavy-Cut End Mills (jj-tools); End Mills for A.B.S (jj-tools); End Mills for Aluminum (jj-tools); End Mills for Copper (jj-tools); End Mills for Graphite (jj-tools); G Series General-Purpose End Mills (jj-tools); HARD Series High-Speed End Mills (jj-tools); JJ Series End Mills (jj-tools); Thread Mills (jj-tools); V Series Ball End Mills (jj-tools); ERGO Ceramic (renfert); Karadent (tcs); Unbreakable (tcs); ARTE SHINE (yamahachi); CERAMIC FIBER POINT (yamahachi); TIGER MULTI GOLD (yamahachi).
- **Datasheets:** FDT Resin, LUSTRA, PHT and TCS only have promotional social-media images, so those brands have no downloadable document. TCS's only PDF is a scan with hand-drawn marks (see 4).
- **Two catalogue photos are lifestyle shots** (hands), not product shots: Renfert *Grinding box* and *SIMPLEX model isolation*.

## 2. Uncertain classification (decision recorded; please confirm)
- Rule applied: **tools, burs, discs, polishers, instruments and accessories = Dental Material** unless the source presents them as equipment.
- **LUSTRA CAD/CAM block** – the material (glass-ceramic? resin?) is not stated anywhere. Filed under *Zirconia & Ceramics* on image evidence only (milling blocks with metal stem).
- **JJ Tools** – the 533-page catalogue is a *general* carbide end-mill / drill / thread-mill catalogue (steel, titanium, aluminium, graphite). It never mentions dentistry. Filed as 12 series-level *Tools* entries; decide whether to publish it at all.
- **Renfert** – *EASY view+*, *LIGHT 1*, *Mobiloskop S* and Yamahachi *LAB SCOPE S* are visualization/lighting aids (not scanners) and share the *Scanners & Visualization* sub-category. *Power pillo / Pillo* deflasking chisels sit under *Wax, Casting & Deflasking*. *help:ex* and *POWER steamer descaler* are consumables (Material); *POWER steamer water softener* is Equipment.
- **Kugel Hook** (denture attachment) and Yamahachi shade guides/teeth cabinet → *Lab Supplies & Instruments*.

## 3. Naming / country
- **DISC** – folder name is DISC; the catalogue is by *Spectra Ceram Trading L.L.C., Dubai*. Please confirm the brand name to display. Disk diameter, grit, maximum speed and material compatibility are "pending manufacturer confirmation" in the source.
- **Country** is shown only when printed in the PDFs (Renfert: Germany; BSM and Profeta: China; AUDent: Liechtenstein; ERAYLAR: Turkey; JJ Tools: Korea; Yamahachi: Japan; DISC: U.A.E. address). Not stated: Denpark, Teknik Dental (only a +90 phone and Turkish UI), FDT, IMT, LUSTRA, PHT, TCS.
- **AUDent logo** – the old file `assets/partners/AUDent.webp` is the logo of *Audent Capital Partners* (a dragon mark), a different company. `AUDents.webp` is the dental-ceramics AUDent AG logo and is the one used in the new dataset. The home page (not touched) may still use the wrong one.
- **BSM** – the old file is called BMS.webp; the brand is BSM (Besmile). Normalised copies live in `assets/brands/`.

## 4. Source quality
- **TCS catalogue PDF** is a scan with hand-drawn circles and Arabic notes (an internal marked-up copy). Product facts (iFlex, Unbreakable, Karadent, Totally Natural) were read from its clean summary page; the file is **not published**. Which TCS products Prime Hub actually stocks is unconfirmed (the circles suggest iFlex, Karadent and Totally Natural). Injection temperatures are printed in °F and kept as printed.
- **BSM-520D flyer** is named *old version* (V1.2.1) – request the current one.
- **Image-only PDFs** (BSM Artamic, Aconia Artist kit, Ultra, 520D, PF10) have no text layer; I read them visually. The small Artamic *material properties* table (CTE, solubility, strength) was too low-resolution to transcribe reliably, so it is omitted.
- **BSM Aconia fracture toughness** values for HT+, ST, SHT, ST Preshade are printed without units in the Family flyer; units are shown only where printed (Master: MPa·m½).
- **Denpark LS2 accuracy** – the source prints the inequality after "6 µm" ambiguously ("direction of the limit requires supplier confirmation"); kept as stated. IOS-C5 standard-tip scan area reads "16*7 5mm" (taken as 16 × 7.5 mm).
- **ERAY (standard)** chart is Turkish only; shade/mould counts were translated by me. The ERAY DELUXE shade range is printed as "36 shades" with VITA and IVOCLAR lists; the exact breakdown was not re-counted.
- **Yamahachi page numbers** in datasheet links are PDF page indexes of the 29-page catalogue (printed page numbers run in spreads). Several wax/abrasive/cleaning photos were matched to products from page layout; a contact-sheet check found no mismatches, but spot-check before launch.
- **Yamahachi products not yet listed** because the text or photo attribution on the page was ambiguous: PCS Form / Combination Set / Full Set packages, MIRROR BUFF, DIAMOND BRUSH, HOG HAIR BRUSH (both), MILLION BUFF, MANDRELS #303, CFP HOLDER, SILKY SHINE, BLUE SHINE, ALUMINOUS, GRAZE POWDER, TIGER MULTI, TIGER MULTI MINI, TK SILICONE CLEANER, POLISH CLEANER, LAB SCOPE S accessories, and the Waxes/abrasives not named above.
- **Renfert** – the catalogue is dated 3/2023 and notes that some end-of-range items are missing. Accessory/spare-part pages (e.g. pp. 13, 17, 33-34, 45-46, 55-56, 63, 68-69, 78-79, 85-86, 127) are not listed as separate products. Short descriptions, advantages and specs were condensed automatically from the catalogue text (metric values first); please proof-read the Renfert copy. Order numbers are kept only where cleanly parseable.
- **FDT Resin / IMT / LUSTRA / PHT** – only promotional images were supplied, so these entries carry only what is visible on the image (no specs). IMT's NiCr specs come from its datasheet image. IMT states ISO 13485, ISO 9001, CE, FDA and CFDA marks on its brochure; these are company-level claims, not verified.
- **Contact details inside promo images** (e.g. 01033447348, 01012999705) differ from the website's +20 109 000 9508. They are cropped out of product images and never reused.

## 5. Large files (3 over 8 MB)
- JJ Tools Carbide End Mills Catalogue — 47.31 MB
- Renfert Catalog 2023 — 21.82 MB
- tegra MP100S Porcelain Furnace Brochure — 10.27 MB
Total published PDFs: 142 MB. If a Vercel deployment is refused or slow, host the biggest files elsewhere and put the URL in `externalUrl` of that entry in `data/documents.json`.

## 6. Site copy that is not backed by the Materials
Existing statements on the inner pages — "since 2010", "15+ years", "1000+ customers", the About timeline (2014, 2018, 2021, 2024), "24/7 technical support", "Visa payments" — were kept as they are, since no source was supplied. The "8 brands" claim is replaced by the real number (15) computed from `data/brands.json`. Please confirm that all 15 brands are authorised partners.

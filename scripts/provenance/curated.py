# -*- coding: utf-8 -*-
"""
Curated catalogue data for Prime Hub Trading (everything except the Renfert
catalogue, which is extracted programmatically by extract_renfert.py).

Every product below was written from the supplier PDFs / images in the
"Materials" folder. `doc`/`page` point to the source PDF page; `img` tells
build-assets.py which embedded image (or page crop) to export.

Taxonomy
  Dental Equipment (equipment): scanners-imaging, milling-printing, furnaces,
      model-prep, sandblasting, cleaning, extraction, wax-casting
  Dental Material (material): zirconia-ceramics, coloring-glaze, pmma-wax, resins,
      artificial-teeth, metal-powders, tools-finishing, lab-supplies
Decision (recorded per brief): tools, burs, discs, polishers, instruments and accessories are
classified as MATERIAL unless the source presents them as equipment.
"""

# --------------------------------------------------------------------------------------
# Sub-category taxonomy
# --------------------------------------------------------------------------------------
TAXONOMY = {
    "equipment": {
        "label": "Dental Equipment",
        "sub": [
            ("scanners-imaging", "Scanners & Visualization"),
            ("milling-printing", "Milling & 3D Printing"),
            ("furnaces", "Furnaces"),
            ("model-prep", "Mixing & Model Preparation"),
            ("sandblasting", "Sandblasting"),
            ("cleaning", "Cleaning & Steaming"),
            ("extraction", "Extraction & Dust Control"),
            ("wax-casting", "Wax, Casting & Deflasking"),
        ],
    },
    "material": {
        "label": "Dental Material",
        "sub": [
            ("zirconia-ceramics", "Zirconia & Ceramics"),
            ("coloring-glaze", "Stains, Glaze & Colouring"),
            ("pmma-wax", "PMMA, Wax & Blanks"),
            ("resins", "Resins & 3D-Print Materials"),
            ("artificial-teeth", "Artificial Teeth"),
            ("metal-powders", "Metal Powders"),
            ("tools-finishing", "Tools, Polishing & Finishing"),
            ("lab-supplies", "Lab Supplies & Instruments"),
        ],
    },
}

# --------------------------------------------------------------------------------------
# Brands (folder name in Materials -> site brand)
# --------------------------------------------------------------------------------------
BRANDS = [
    dict(slug="renfert", name="Renfert", folder="RENFERT", country="Germany", logo="assets/partners/Renfert.png",
         about="Renfert GmbH develops and produces equipment, instruments and materials for dental laboratories and "
               "offices, and has done so since 1925. Its products are made in Germany under the motto “making work easy”."),
    dict(slug="bsm", name="BSM", folder="BSM", country="China", logo="assets/partners/BMS.webp",
         about="BSM (Besmile) is a digital solutions provider for restorative and implant dentistry, offering CAD/CAM "
               "materials and equipment developed and manufactured in-house."),
    dict(slug="audent", name="AUDent", folder="Audent", country="Liechtenstein", logo="assets/partners/AUDents.webp",
         about="AUDent supplies dental ceramic systems, including i-motion e-press lithium disilicate press ceramic and "
               "the i-motion LFU universal shade, stain and glaze range."),
    dict(slug="denpark", name="Denpark", folder="DENPARK", country=None, logo=None,
         about="Denpark 3D digital scanners: the LS series of desktop laboratory scanners and the IOS-C5 intraoral scanner."),
    dict(slug="disc", name="DISC", folder="DISC", country="United Arab Emirates", logo=None,
         about="Diamond cutting and separating disks, supplied in 16 profiles and three thicknesses "
               "(catalogue by Spectra Ceram Trading L.L.C., Dubai)."),
    dict(slug="eraylar", name="ERAYLAR", folder="ERAYLAR", country="Turkey", logo="assets/partners/Eraylar.webp",
         about="Eraylar Akrilik Sanayi ve Diş Ticaret A.Ş. (Ankara) manufactures acrylic artificial teeth under the ERAY "
               "and ERAY DELUXE names, certified to ISO 22112 and EN ISO 13485."),
    dict(slug="fdt-resin", name="FDT Resin", folder="FDT RESIN", country=None, logo=None,
         about="Resins for dental 3D printing, including the Pro Model Resin and Wax Resin ranges."),
    dict(slug="imt-metal-powder", name="IMT Metal Powder", folder="IMT METAL POWDER", country=None, logo=None,
         about="IMT develops metal powder materials for dental 3D printing and states ISO 13485, ISO 9001, CE and FDA "
               "certification on its brochure."),
    dict(slug="jj-tools", name="JJ Tools", folder="JJ TOOLS", country="South Korea", logo="assets/partners/JJTools.webp",
         about="JJ Tools Co., Ltd. makes carbide end mills, drills and thread mills in Korea: 18,619 tools in 278 items "
               "for steel, titanium, aluminium, graphite and composites."),
    dict(slug="lustra", name="LUSTRA", folder="LUSTRA", country=None, logo=None,
         about="LUSTRA CAD/CAM restorative blocks."),
    dict(slug="pht", name="PHT", folder="PHT", country=None, logo=None,
         about="PHT (New Technology) diamond polishing systems: Diamond Stone and Diamond Rubber polishers."),
    dict(slug="profeta", name="Profeta", folder="PROFETA", country="China", logo="assets/partners/profeta.webp",
         about="Profeta Intelligent Technology Co., Ltd. (Nanjing) builds dedicated dental metal 3D printers, sold with a "
               "one-stop package of design software, slicing software, furnace and nitrogen generator."),
    dict(slug="tcs", name="TCS", folder="TCS", country=None, logo="assets/partners/TCS.webp",
         about="TCS supplies dental resins, equipment and accessories, including thermoplastic resins for removable appliances."),
    dict(slug="teknik-dental", name="Teknik Dental", folder="TEKNIK DENTAL", country=None,
         logo="assets/partners/TeknikDental.webp",
         about="Teknik Dental has built dental furnaces since 1984 under the tegra name, from porcelain furnaces to "
               "high-speed zirconia sintering furnaces."),
    dict(slug="yamahachi", name="Yamahachi", folder="Yamahachi", country="Japan", logo=None,
         about="Yamahachi Dental Mfg., Co. (Gamagori, Aichi) supplies artificial teeth, CAD/CAM milling and 3D-print "
               "materials, resins, waxes, polishing materials and laboratory equipment."),
]

# --------------------------------------------------------------------------------------
# Documents (PDFs that are published on the Download Center)
# key -> brand, src (relative to Materials), title, type, lang, out (file name in assets/downloads/<brand>/)
# --------------------------------------------------------------------------------------
YC = "Yamahachi/prduct_catalog_2025_2026_ver1_LOW.pdf"
BD = "BSM/DENTAL MATERIALS/"
BE = "BSM/DENTAL EQUIPMENTS/"
DOCS = {
    "audent-epress-chart": dict(brand="audent", src="Audent/Audent i motion e press colour chart 2023 09 29.pdf",
                                title="i-motion e-press Colour Chart (2023)", type="datasheet", lang="EN",
                                out="i-motion-e-press-colour-chart.pdf"),
    "audent-lfu": dict(brand="audent", src="Audent/i-motion LFU catalog-compressed.pdf",
                       title="i-motion LFU Stains, Shades & Glaze", type="datasheet", lang="EN",
                       out="i-motion-lfu-stains-shades-glaze.pdf"),
    "bsm-aconia-family": dict(brand="bsm", src=BD + "BSM_Zirconia_Aconia Family_Flyer_EN 20260423 v2.1.1.pdf",
                              title="Aconia Zirconia Family Flyer", type="brochure", lang="EN", out="aconia-zirconia-family.pdf"),
    "bsm-aconia-master": dict(brand="bsm", src=BD + "BSM_Zirconia_Aconia 3D Aconia Master_Flyer_EN 20260416 v4.4.2.pdf",
                              title="3D Aconia Master Flyer", type="brochure", lang="EN", out="3d-aconia-master.pdf"),
    "bsm-aconia-ultra": dict(brand="bsm", src=BD + "BSM_Zirconia_Aconia 3D Aconia Ultra_Flyer_EN 20260403  v1.1.1.pdf",
                             title="3D Aconia Ultra Flyer", type="brochure", lang="EN", out="3d-aconia-ultra.pdf"),
    "bsm-artamic": dict(brand="bsm", src=BD + "BSM_SG_Artamic_Flyer_EN 20251011 v2.1.1.pdf",
                        title="Artamic Stain/Glaze Flyer", type="brochure", lang="EN", out="artamic-stain-glaze.pdf"),
    "bsm-artist-kit": dict(brand="bsm", src=BD + "BSM_CL _Artist Kit_Flyer_2025.06.25.pdf",
                           title="Aconia Artist Kit Flyer", type="brochure", lang="EN", out="aconia-artist-kit.pdf"),
    "bsm-artist-v1": dict(brand="bsm", src=BD + "BSM_CL _Artist V1_Flyer(vertical)_2024.pdf",
                          title="Aconia Artist V1 Opaque Liquid Flyer", type="brochure", lang="EN", out="aconia-artist-v1-opaque-liquid.pdf"),
    "bsm-520d": dict(brand="bsm", src=BE + "BSM_Milling_520D_Flyer_EN 20260127-old version.pdf",
                     title="BSM-520D 5-Axis Milling Machine Flyer", type="datasheet", lang="EN", out="bsm-520d-milling-machine.pdf"),
    "bsm-fm30": dict(brand="bsm", src=BE + "BSM_Sintering_FM30_Flyer_EN 20251011 v1.1.1.pdf",
                     title="BSM-FM30 Zirconia Sintering Furnace Flyer", type="datasheet", lang="EN", out="bsm-fm30-sintering-furnace.pdf"),
    "bsm-pf10": dict(brand="bsm", src=BE + "BSM_Porcelain_PF10_Flyer_EN 20251019 v1.1.1.pdf",
                     title="BSM-PF10 Porcelain Furnace Flyer", type="datasheet", lang="EN", out="bsm-pf10-porcelain-furnace.pdf"),
    "denpark-ls": dict(brand="denpark", src="DENPARK/Spectra_Denpark_LS_Catalogue.pdf",
                       title="Spectra Scanner by Denpark: LS Series Catalogue", type="catalog", lang="EN", out="denpark-ls-series-catalogue.pdf"),
    "denpark-ls2": dict(brand="denpark", src="DENPARK/Spectra_Denpark_LS2_Brochure.pdf",
                        title="Denpark LS2 Scanner Brochure", type="brochure", lang="EN", out="denpark-ls2-brochure.pdf"),
    "denpark-c5": dict(brand="denpark", src="DENPARK/C5 EN 2.pdf",
                       title="Denpark IOS-C5 Intraoral Scanner Datasheet", type="datasheet", lang="EN", out="denpark-ios-c5-datasheet.pdf"),
    "disc-catalog": dict(brand="disc", src="DISC/SpectraCeram_Cutting_Disks_2026_SpectraIdentity_v5.pdf",
                         title="Cutting & Separating Disks Catalogue 2026", type="catalog", lang="EN", out="cutting-separating-disks-2026.pdf"),
    "eraylar-deluxe": dict(brand="eraylar", src="ERAYLAR/eraydeluxetureng_2022-01-25_21-14-12.pdf",
                           title="ERAY DELUXE Mould Chart", type="catalog", lang="TR / EN", out="eray-deluxe-mould-chart.pdf"),
    "eraylar-eray": dict(brand="eraylar", src="ERAYLAR/erayturkce_2022-01-25_20-59-30.pdf",
                         title="ERAY Mould Chart", type="catalog", lang="TR", out="eray-mould-chart-tr.pdf"),
    "imt-nicr": dict(brand="imt-metal-powder", src="IMT METAL POWDER/472892700_122164775240272744_4389916170306438226_n.pdf",
                     title="IMT NiCr Metal Powder Datasheet", type="datasheet", lang="EN", out="imt-nicr-metal-powder.pdf"),
    "jj-catalog": dict(brand="jj-tools", src="JJ TOOLS/1785379371038992.pdf",
                       title="JJ Tools Carbide End Mills Catalogue", type="catalog", lang="EN / KO", out="jj-tools-carbide-end-mills.pdf"),
    "profeta-c120": dict(brand="profeta", src="PROFETA/C120-EN-V2.pdf", title="Profeta C120 Dental Metal 3D Printer",
                         type="datasheet", lang="EN", out="profeta-c120.pdf"),
    "profeta-c150": dict(brand="profeta", src="PROFETA/C150EN.pdf", title="Profeta C150 Dental Metal 3D Printer",
                         type="datasheet", lang="EN", out="profeta-c150.pdf"),
    "renfert-catalog": dict(brand="renfert", src="RENFERT/RENFERT_CATALOG_EN (3).PDF", title="Renfert Catalog 2023",
                            type="catalog", lang="EN", out="renfert-catalog-2023.pdf"),
    "renfert-basic-eco": dict(brand="renfert", src="RENFERT/RENFERT_Basic eco.PDF", title="Basic eco Sandblasting Unit",
                              type="datasheet", lang="EN", out="renfert-basic-eco.pdf"),
    "renfert-millo": dict(brand="renfert", src="RENFERT/RENFERT_MILLO.PDF", title="Millo / Millo pro Dental Arch Trimmer",
                          type="datasheet", lang="EN", out="renfert-millo.pdf"),
    "renfert-mt3": dict(brand="renfert", src="RENFERT/RENFERT_MT3.PDF", title="MT3 Wet Trimmer", type="datasheet",
                        lang="EN", out="renfert-mt3.pdf"),
    "renfert-power-steamer": dict(brand="renfert", src="RENFERT/RENFERT_POWER STEAMER.PDF", title="POWER steamer 1",
                                  type="datasheet", lang="EN", out="renfert-power-steamer.pdf"),
    "renfert-silent-compact": dict(brand="renfert", src="RENFERT/RENFERT_SILENT COMPACT.PDF",
                                   title="SILENT compact Extraction Unit", type="datasheet", lang="EN",
                                   out="renfert-silent-compact.pdf"),
    "renfert-silent-compactcam": dict(brand="renfert", src="RENFERT/RENFERT_Silent compact CAM.PDF",
                                      title="SILENT compactCAM Extraction Unit", type="datasheet", lang="EN",
                                      out="renfert-silent-compactcam.pdf"),
    "renfert-top-spin": dict(brand="renfert", src="RENFERT/RENFERT_TOP SPIN.PDF", title="Top spin Pin Drilling Unit",
                             type="datasheet", lang="EN", out="renfert-top-spin.pdf"),
    "renfert-twister": dict(brand="renfert", src="RENFERT/RENFERT_TWISTER&TWISTER VENTURI.PDF",
                            title="Twister & Twister venturi Vacuum Mixing Units", type="datasheet", lang="EN",
                            out="renfert-twister.pdf"),
    "renfert-vario-e": dict(brand="renfert", src="RENFERT/RENFERT_VARIO E.PDF", title="Vario E Wax Warmer",
                            type="datasheet", lang="EN", out="renfert-vario-e.pdf"),
    "renfert-waxlectric": dict(brand="renfert", src="RENFERT/RENFERT_WAX ELECTRIC.PDF",
                               title="Waxlectric I & II Electric Wax Knives", type="datasheet", lang="EN",
                               out="renfert-waxlectric.pdf"),
    "renfert-silent-xs": dict(brand="renfert", src="RENFERT/20250821_B_SILENT-XS_2pages_en (1).pdf",
                              title="SILENT XS Mobile Suction Unit", type="datasheet", lang="EN", out="renfert-silent-xs.pdf"),
    "renfert-light-1": dict(brand="renfert", src="RENFERT/LIGHT-1_2pages_en.pdf", title="LIGHT 1 Dental Worklight",
                            type="datasheet", lang="EN", out="renfert-light-1.pdf"),
    "teknik-mp100": dict(brand="teknik-dental", src="TEKNIK DENTAL/MP100_Brochure_EN.pdf",
                         title="tegra MP100S Porcelain Furnace Brochure", type="brochure", lang="EN", out="tegra-mp100s-brochure.pdf"),
    "teknik-mp1500": dict(brand="teknik-dental", src="TEKNIK DENTAL/MP1500_Speed_Multistep_Brochure_EN_20230404.pdf",
                          title="tegra MP1500 Speed Multistep Brochure", type="brochure", lang="EN",
                          out="tegra-mp1500-speed-multistep-brochure.pdf"),
    "yamahachi-catalog": dict(brand="yamahachi", src=YC, title="Yamahachi Product Catalog 2025-2026", type="catalog",
                              lang="EN", out="yamahachi-product-catalog-2025-2026.pdf"),
    "yamahachi-pmma-wax": dict(brand="yamahachi", src="Yamahachi/PMMA & WAX.pdf",
                               title="Yamahachi CAD/CAM PMMA & Wax Materials", type="brochure", lang="EN",
                               out="yamahachi-pmma-and-wax.pdf"),
}

# --------------------------------------------------------------------------------------
# Image-source helpers (consumed by build-assets.py)
# --------------------------------------------------------------------------------------
def IDX(src, page, index):            # k-th entry of page.get_image_info()
    return {"src": src, "page": page, "index": index}


def XREF(src, page, xref):
    return {"src": src, "page": page, "xref": xref}


def NTH(src, page, n):                # n-th square-ish photo on the page, left to right
    return {"src": src, "page": page, "nth": n}


def CROP(src, page, box):             # fractional crop of a rendered PDF page
    return {"src": src, "page": page, "crop": list(box)}


def FCROP(src, box):                  # fractional crop of an image file
    return {"src": src, "crop": list(box)}


LOGO_SOURCES = {          # brands without a logo file in assets/partners: exported from the supplier PDFs
    "denpark": IDX("DENPARK/Spectra_Denpark_LS_Catalogue.pdf", 1, 1),
    "yamahachi": CROP(YC, 1, (0.665, 0.048, 0.925, 0.090)),
}

PRODUCTS = []


def P(brand, name, cat, sub, summary, desc="", *, model="", specs=(), features=(), applications=(), tags=(),
      doc=None, page=None, img=None, gallery=(), featured=False, new=False, pid=None):
    PRODUCTS.append(dict(brand=brand, name=name, category=cat, subcategory=sub, summary=summary, description=desc,
                         model=model, specs=[list(s) for s in specs], features=list(features),
                         applications=list(applications), tags=list(tags), doc=doc, page=page, img=img,
                         gallery=list(gallery), featured=featured, isNew=new, pid=pid))


# ======================================================================================
# BSM
# ======================================================================================
P("bsm", "BSM-520D", "equipment", "milling-printing",
  "Intelligent 5-axis dry milling machine for zirconia, PMMA, wax and PEEK with ±0.005 mm milling accuracy.",
  "A 5-axis dental milling machine with a 60,000 rpm spindle, an automatic 6-tool changer with breakage monitoring and "
  "an integrated 9.7-inch touch-screen PC. Wide B-axis rotation and 90° vertical milling reproduce natural tooth anatomy.",
  model="BSM-520D",
  specs=[("Axes", "5"), ("Application", "Dry milling"), ("Milling accuracy", "±0.005 mm"),
         ("Spindle speed", "60,000 rpm"), ("B-axis rotation", "-30° to +40°"), ("Built-in burs", "6 (automatic changer)"),
         ("Tool types", "Zirconia: ø4 mm ball-mill (2 / 1 / 0.6 mm), ø4 × 1 mm end-mill; resin: ø4 mm (2 / 1 mm)"),
         ("Cooling", "Automatic air-cooling spindle"), ("Motor", "AC servo"), ("Voltage / power", "220 V / 2.6 kW"),
         ("Monitor", "9.7\" LCD touch screen"), ("Air pressure", "> 0.65 MPa"),
         ("Dimensions (W × D × H)", "570 × 680 × 780 mm"), ("Weight", "130 kg"),
         ("Environmental temperature", "5-40 °C"), ("Remote control", "Yes")],
  features=["Automatic tool length detection and tool-life monitoring", "1/3 holder boosts output by about 20% per block",
            "Dust-proof design extends machine lifespan", "Digital servo system, ±0.01 mm installation accuracy per axis",
            "Aerometal gantry structure for stable high-speed milling"],
  applications=["Full contour crowns", "Copings", "Inlays / onlays", "Veneers", "Crown bridges", "Zirconia abutments",
                "Zirconia implant bridges", "Non-metal frames"],
  tags=["5-axis", "dry milling", "CAD/CAM", "zirconia", "PMMA", "wax", "PEEK"], doc="bsm-520d", page=1,
  img=IDX(BE + "BSM_Milling_520D_Flyer_EN 20260127-old version.pdf", 1, 4), featured=True)

P("bsm", "BSM-FM30", "equipment", "furnaces",
  "Zirconia fast-sintering furnace holding 80+ units per cycle, with remote monitoring and 100 programs.",
  "A large-capacity zirconia sintering furnace with a dual-layer crucible, circumferential silicon-molybdenum heating "
  "and PID temperature control. A 7-inch colour touch screen and IoT cloud platform allow one-touch and remote operation.",
  model="BSM-FM30",
  specs=[("Application", "Zirconia sintering"), ("Capacity", "≥ 80 zirconia units per cycle"),
         ("Maximum withstand temperature", "1700 °C"), ("Working temperature", "≤ 1600 °C"),
         ("Heating elements", "4 × upgraded silicon molybdenum"), ("Rated power", "3 kW"), ("Power supply", "220 V / 50 Hz"),
         ("Chamber size", "ø110 × 90 mm"), ("Trays", "2 (ø105 × 40 mm)"), ("Programs", "100"),
         ("Firing types", "Standard / fast sintering"), ("Control", "High-precision type B thermocouple; 7\" true-colour touch screen"),
         ("Dimensions (D × W × H)", "400 × 590 × 870 mm"), ("Weight", "85 kg")],
  features=["Pollution-free high-purity silicon-molybdenum heating elements", "Circumferential heating for even temperature",
            "Remote monitoring from computer or mobile devices", "Fast sintering without thermal stress"],
  applications=["Zirconia crowns and bridges"], tags=["sintering", "zirconia", "IoT"], doc="bsm-fm30", page=1,
  img=IDX(BE + "BSM_Sintering_FM30_Flyer_EN 20251011 v1.1.1.pdf", 2, 6), featured=True)

P("bsm", "BSM-PF10", "equipment", "furnaces",
  "Porcelain furnace with 4.3-inch touch screen, 120 °C/min heating rate and IoT cloud platform.",
  "A compact porcelain furnace for glass-ceramic crystallisation, glazing, staining and porcelain layering, with "
  "vacuum firing, smart temperature control and more than 100 individual programs.",
  model="BSM-PF10",
  specs=[("Applications", "Glass ceramic crystallization, glazing, staining, porcelain layering"),
         ("Maximum withstand temperature", "1200 °C"), ("Heating rate", "≤ 120 °C/min"), ("Maximum vacuum", "≤ -96 kPa"),
         ("Firing chamber", "ø86 × 50 mm"), ("Heating element", "Resistance wire"), ("Sensor", "S-type thermocouple"),
         ("Rated power", "1.5 kW"), ("Power supply", "220 V / 50 Hz"), ("Programs", ">100 (expandable)"),
         ("Firing types", "Standard & two-stage heating"), ("Monitor", "4.3-inch true-colour touch screen"),
         ("Connectivity", "Internet, IoT cloud platform, mobile control"),
         ("Dimensions (W × D × H)", "310 × 360 × 610 mm"), ("Weight", "28 kg")],
  features=["±1 °C precision control", "120 °C/min fast heating", "Versatile firing programs", "Vacuum firing"],
  applications=["Glass-ceramic crystallization", "Glazing", "Staining", "Porcelain layering"],
  tags=["porcelain", "glaze", "glass ceramic"], doc="bsm-pf10", page=1,
  img=IDX(BE + "BSM_Porcelain_PF10_Flyer_EN 20251019 v1.1.1.pdf", 2, 3))

ACON = BD + "BSM_Zirconia_Aconia Family_Flyer_EN 20260423 v2.1.1.pdf"
_ac_common = [("Disc diameter", "ø98.5 mm"), ("Disc thickness", "12 / 14 / 16 / 18 / 20 / 22 / 25 mm (28 / 30 mm on request)"),
              ("Sintered density", "> 6.02 g/cm³"), ("Vickers hardness HV10", "1300 ± 50")]
P("bsm", "Aconia HT+", "material", "zirconia-ceramics",
  "High-strength zirconia disc, 1400 MPa flexural strength, 42% translucency; indicated up to 14-unit bridges.",
  "Monolithic zirconia disc combining exceptional strength with an economical profile, for crowns, bridges and "
  "implant-supported restorations.",
  specs=[("Flexural strength (3-point)", "1400 MPa"), ("Translucency", "42%"), ("Fracture toughness", "> 9")] + _ac_common,
  features=["Exceptional strength", "Economic solution"],
  applications=["Inlay / onlay", "Full contour crown", "Coping", "Full contour anterior bridge (3 units)",
                "Full contour posterior bridge (3 units)", "Full contour bridge (≤ 14 units)", "Implant-supported restorations"],
  tags=["zirconia", "HT+", "monolithic"], doc="bsm-aconia-family", page=2, img=IDX(ACON, 1, 7))
P("bsm", "Aconia ST", "material", "zirconia-ceramics",
  "All-round zirconia disc: 1250 MPa flexural strength, 43% translucency, wide indications up to 14 units.",
  "Zirconia disc with high strength and excellent millability, suited to a broad range of single and multi-unit restorations.",
  specs=[("Flexural strength (3-point)", "1250 ± 100 MPa"), ("Translucency", "43%"), ("Fracture toughness", "> 5.5")] + _ac_common,
  features=["Wide indications", "High strength with excellent millability"],
  applications=["Inlay / onlay", "Full contour crown", "Coping", "Full contour anterior bridge (3 units)",
                "Full contour posterior bridge (3 units)", "Full contour bridge (≤ 14 units)", "Implant-supported restorations"],
  tags=["zirconia", "ST", "monolithic"], doc="bsm-aconia-family", page=2, img=IDX(ACON, 1, 6))
P("bsm", "Aconia SHT", "material", "zirconia-ceramics",
  "Super-high-translucency zirconia disc (46%, 1000 MPa) for esthetic crowns and bridges up to 7 units.",
  "Zirconia disc with great translucency for esthetic single crowns, reduced crowns and short-span bridges.",
  specs=[("Flexural strength (3-point)", "1000 ± 100 MPa"), ("Translucency", "46%"), ("Fracture toughness", "> 5")] + _ac_common,
  features=["Great translucency", "Economic solution"],
  applications=["Inlay / onlay", "Full contour crown", "Coping", "Reduced crown", "Full contour anterior bridge (3 units)",
                "Full contour posterior bridge (3 units)", "Full contour bridge (≤ 7 units)"],
  tags=["zirconia", "SHT", "monolithic"], doc="bsm-aconia-family", page=2, img=IDX(ACON, 1, 5))
P("bsm", "Aconia ST Preshade", "material", "zirconia-ceramics",
  "Pre-shaded 43%-translucency zirconia disc (1250 MPa) with precise VITA shade match.",
  "Pre-shaded version of Aconia ST for precise VITA shade matching and stable edges during milling.",
  specs=[("Flexural strength (3-point)", "1250 ± 50 MPa"), ("Translucency", "43%"), ("Fracture toughness", "> 5.5")] + _ac_common,
  features=["Precise VITA shade match", "High toughness, edge stability during milling"],
  applications=["Inlay / onlay", "Full contour crown", "Coping", "Full contour anterior bridge (3 units)",
                "Full contour posterior bridge (3 units)", "Full contour bridge (≤ 14 units)"],
  tags=["zirconia", "preshade", "VITA"], doc="bsm-aconia-family", page=2, img=IDX(ACON, 1, 8))
P("bsm", "3D Aconia Master", "material", "zirconia-ceramics",
  "Multilayer zirconia (800-1200 MPa, 43-51% translucency) with patented interleaved layers; bridges up to 14 units.",
  "Next-generation multilayer zirconia whose interleaved layer structure gives a seamless colour and strength "
  "gradient, near-zero deformation and a flexible 1520-1560 °C sintering range.",
  specs=[("Flexural strength (3-point)", "800-1200 MPa"), ("Translucency", "43-51%"),
         ("Fracture toughness", "≥ 5.8 MPa·m½"), ("Vickers hardness HV10", "1250-1350"), ("Sintered density", "> 6.02 g/cm³"),
         ("Disc diameter", "ø98 mm"), ("Disc thickness", "12 / 14 / 16 / 18 / 20 / 22 / 25 mm (28 / 30 mm on request)"),
         ("Shades", "A1-D4 (16 VITA shades) plus 0M1, 0M2, 0M3"), ("Sintering range", "1520-1560 °C")],
  features=["Glaze & Go: no staining needed", "Flexible 1520-1560 °C sintering range", "Low deformation for durable bridges",
            "Pairs with Aconia V1 Opaque Liquid for masking implant abutments"],
  applications=["Implant-supported restorations", "Veneers", "Copings", "Full contour crowns", "Inlays / onlays",
                "Full contour bridges (≤ 14 units)"],
  tags=["zirconia", "multilayer", "3D Aconia"], doc="bsm-aconia-master", page=3,
  img=IDX(BD + "BSM_Zirconia_Aconia 3D Aconia Master_Flyer_EN 20260416 v4.4.2.pdf", 2, 3), featured=True)
P("bsm", "3D Aconia Ultra", "material", "zirconia-ceramics",
  "Premium multilayer zirconia, 45-55% translucency and 700-1100 MPa, for esthetic bridges up to 14 units.",
  "Multilayer zirconia with a cervical-to-incisal gradient (45% translucency / 1100 MPa to 55% / 700 MPa) and low "
  "deformation, for premium esthetics without rework.",
  specs=[("Flexural strength (3-point)", "700-1100 MPa"), ("Translucency", "45-55%"), ("Fracture toughness", "> 5"),
         ("Vickers hardness HV10", "1300 ± 50"), ("Sintered density", "> 6.02 g/cm³"), ("Disc diameter", "ø98.5 mm"),
         ("Disc thickness", "12 / 14 / 16 / 18 / 20 / 22 / 25 mm (28 / 30 mm on request)"), ("Sintering range", "1520-1560 °C")],
  features=["Premium esthetics, unmatched performance", "Flexible sintering range", "Glaze & Go finishing"],
  applications=["Implant-supported restorations", "Veneers", "Copings", "Full contour crowns", "Inlays / onlays",
                "Full contour bridges (≤ 14 units, ≤ 7 units for long spans)"],
  tags=["zirconia", "multilayer", "3D Aconia"], doc="bsm-aconia-ultra", page=1,
  img=IDX(BD + "BSM_Zirconia_Aconia 3D Aconia Ultra_Flyer_EN 20260403  v1.1.1.pdf", 2, 2))

P("bsm", "Aconia Artist Kit", "material", "coloring-glaze",
  "Zirconia coloring-liquid kit for opaque, brightness, gingival, incisal-translucency and fissure effects.",
  "A set of Aconia Artist coloring liquids (V1-V3, G1-G3, TO2-TO3, P1-P3, O1-O3) for individualising zirconia "
  "restorations by brushing or immersion before sintering.",
  specs=[("Opaque", "V1"), ("Magic value", "V2, V3"), ("Natural gingival", "G1 / G2 / G3"),
         ("Incisal translucency", "TO2, TO3"), ("Art fissure", "P1 / P2 / P3, O1 / O2, O3"),
         ("Pre-drying", "5-10 min at 80-100 °C"), ("Drying", "30 min (single crown) / 60 min (bridge) at 80-100 °C")],
  applications=["Mamelon and blue / grey incisal effects", "Natural gingival effects", "Tetracycline or discoloration effects",
                "Fissure characterization"],
  tags=["zirconia", "coloring liquid", "Aconia"], doc="bsm-artist-kit", page=2,
  img=CROP(BD + "BSM_CL _Artist Kit_Flyer_2025.06.25.pdf", 2, (0.21, 0.07, 0.43, 0.27)))
P("bsm", "Aconia Artist V1 Opaque Liquid", "material", "coloring-glaze",
  "Opaque coloring liquid that masks discolored stumps and metal abutments with one brushed layer in 2-3 seconds.",
  "Aconia Artist V1 is brushed in a single layer inside the crown to cover discolored stumps or metal abutments, "
  "keeping crown thickness unchanged for both high-translucency and ultra-thin zirconia.",
  specs=[("Type", "Opaque coloring liquid"), ("Application", "One layer, brushed on the inner crown"),
         ("Working time", "2-3 seconds (vs 45 min for the traditional opaque method)")],
  features=["Keeps crown thickness unchanged", "Works for high-translucency and ultra-thin zirconia"],
  applications=["Tetracycline teeth", "Teeth whitening", "Implant superstructure", "Necrosis teeth"],
  tags=["opaque", "Aconia", "coloring liquid"], doc="bsm-artist-v1", page=1,
  img=CROP(BD + "BSM_CL _Artist V1_Flyer(vertical)_2024.pdf", 1, (0.54, 0.24, 0.90, 0.50)))
ART = BD + "BSM_SG_Artamic_Flyer_EN 20251011 v2.1.1.pdf"
P("bsm", "Artamic Stain/Glaze", "material", "coloring-glaze",
  "Stain and glaze system for zirconia, glass ceramic and PFZ restorations, fired from 740 °C with lifelike fluorescence.",
  "Artamic stain pastes, glaze pastes, 3D glaze pastes and blending liquid give natural, predictable shades and "
  "instant glossiness in a single application. Together with Aconia, 5 disc shades plus 5 stains cover all 16 VITA shades.",
  specs=[("Firing temperature", "Down to 740 °C"), ("Suitable for", "Zirconia, glass ceramic, porcelain-fused-to-zirconia"),
         ("Components", "Stain pastes, glaze pastes, 3D glaze pastes, blending liquid")],
  features=["Lifelike fluorescence", "Predictable shade before and after firing", "Optimal paste viscosity", "Instant glossiness",
            "Wide temperature range"],
  applications=["Staining", "Glazing", "Characterization of zirconia and glass-ceramic restorations"],
  tags=["stain", "glaze", "Artamic"], doc="bsm-artamic", page=3, img=IDX(ART, 3, 2), featured=True)
P("bsm", "Artamic 3D Glaze", "material", "coloring-glaze",
  "3D glaze pastes (3D Light Pink, 3D Orange Pink) for building shapes and gingiva detail in a single firing.",
  "Pastes that let technicians build shapes, add surface texture and create gingival detail without vacuum, "
  "completing staining and glazing in one firing.",
  features=["Building shapes", "Detailing surface texture", "Efficient single-firing processing", "Gingiva shades"],
  tags=["3D glaze", "gingiva", "Artamic"], doc="bsm-artamic", page=7, img=IDX(ART, 6, 2))
P("bsm", "Artamic Master Kit", "material", "coloring-glaze",
  "Artamic kit with all essential stain and glaze pastes plus blending liquid for complete characterization.",
  "The Master Kit contains the essential stain and glaze pastes of the Artamic system and a bottle of blending liquid. "
  "A shading guide is not included.",
  specs=[("Shade groups", "Dentine, glaze, incisal, gingival and adjustment shades"), ("Includes", "Blending liquid")],
  tags=["kit", "stain", "glaze"], doc="bsm-artamic", page=6, img=IDX(ART, 5, 6))
P("bsm", "Artamic Gingiva Kit", "material", "coloring-glaze",
  "Artamic kit of 6 gingival shades, 2 3D gingiva shades and blending liquid for detailed gingival effects.",
  "Designed for creating detailed gingival effects on zirconia and glass-ceramic restorations.",
  specs=[("Includes", "6 gingival shades, 2 3D gingiva shades, 1 bottle blending liquid")],
  tags=["kit", "gingiva"], doc="bsm-artamic", page=7, img=IDX(ART, 5, 2))

# ======================================================================================
# AUDent
# ======================================================================================
P("audent", "i-motion e-press", "material", "zirconia-ceramics",
  "Lithium disilicate press ceramic in 18 medium shades plus dark, light, LT, BLT, AHT and OI ingot groups.",
  "i-motion e-press is a lithium disilicate press ceramic with a wide range of indications. It is fired with the "
  "monolithic e-press programme (400 °C start, 45 K/min, 720 °C, 2 min hold).",
  specs=[("Material", "Lithium disilicate press ceramic"),
         ("Medium shades", "A0 A1 A2 A3 A3.5 A4 B0 B1 B2 B3 B4 C1 C2 C3 C4 D2 D3 D4"),
         ("Other ingot groups", "dark 1-5, dark+ 1+-3+, light 1-3, LT BL 1-5, medium BLT, medium AHT, light OI"),
         ("Firing (e-press)", "400 °C start, 3 min dry, 4 min closing, 45 K/min, vacuum 670 °C, 720 °C final, 2 min hold")],
  tags=["lithium disilicate", "press ceramic"], doc="audent-epress-chart", page=1,
  img=CROP("Audent/Audent i motion e press colour chart 2023 09 29.pdf", 1, (0.0, 0.0, 1.0, 0.56)))
AUDLFU = "Audent/i-motion LFU catalog-compressed.pdf"
P("audent", "i-motion LFU Stains", "material", "coloring-glaze",
  "Fluorescent universal stains in 30 shades, as powder or ready-to-use paste, for all standard dental ceramics.",
  "i-motion LFU stains are universal, fluorescent and non-fluorescent stains to be used on all standard dental "
  "ceramics, available in powder and ready-to-use paste.",
  specs=[("Shades", "30 (white fluor to grey fluor, incl. snow white, vanilla, beige, yellow, orange, champagne, safari, olive, "
                    "khaki, rose, purple, red, smoke, blue, pigeon blue, green, brown, dark brown, red brown, black)"),
         ("Format", "Powder and ready-to-use paste")],
  tags=["stain", "fluorescent", "i-motion"], doc="audent-lfu", page=1,
  img=CROP(AUDLFU, 1, (0.0, 0.18, 1.0, 0.60)))
P("audent", "i-motion LFU Shades", "material", "coloring-glaze",
  "Universal fluorescent shade pastes A, B, C and D (light and standard) for ceramic characterization.",
  "Universal shade pastes for adjusting the colour of dental ceramics, in light fluor and standard fluor versions.",
  specs=[("Shades", "A, B, C, D light fluor; A, B, C, D fluor"), ("Format", "Powder and ready-to-use paste")],
  tags=["shade paste", "fluorescent", "i-motion"], doc="audent-lfu", page=1,
  img=CROP(AUDLFU, 1, (0.0, 0.60, 1.0, 0.98)))
P("audent", "i-motion LFU Glaze Paste Fluor", "material", "coloring-glaze",
  "Fluorescent glaze paste (5 g) with glaze liquid (20 ml) for all standard dental ceramics; ref. 444003P.",
  "Universal shade, stain and glaze, fluorescent and non-fluorescent, for all standard dental ceramics. Part of the "
  "LFU Stain & Shade Fluor Paste Kit (shade paste 4 × 3 g, stain fluor paste 11 × 3 g, glaze paste 5 g, glaze liquid 20 ml).",
  model="444003P",
  specs=[("Glaze paste fluor", "5 g"), ("Glaze liquid", "20 ml"), ("Reference", "444003P"),
         ("Firing: e-press / i-motion zirkon", "400 °C, 3 min dry, 4 min closing, 45 K/min, vacuum 670 °C, 720 °C, 2 min"),
         ("Firing: monolithic zirconia, Classic 920, Classic, Zirkon press",
          "400 °C, 3 min dry, 4 min closing, 45 K/min, vacuum 670 °C, 770 °C, 1 min")],
  tags=["glaze", "fluorescent", "i-motion"], doc="audent-lfu", page=2,
  img=CROP(AUDLFU, 2, (0.0, 0.0, 1.0, 0.40)))

# ======================================================================================
# Denpark
# ======================================================================================
DPL = "DENPARK/Spectra_Denpark_LS_Catalogue.pdf"
_dp_shared = [("Output formats", "STL / PLY / OBJ"), ("Light source", "Blue light"), ("Texture scanning", "True colour"),
              ("Power supply", "DC 24 V"), ("Interface", "USB 3.0"), ("Articulator scanning", "Dynamic / static; articulator transfer")]
P("denpark", "LS2 Dental Laboratory Scanner", "equipment", "scanners-imaging",
  "Dual 2.4 MP camera blue-light model scanner: 11-second full-arch scan, true-colour texture, open STL/PLY/OBJ output.",
  "A practical start to digital scanning for everyday model digitisation, with blue-light acquisition, true-colour "
  "texture capture and an open file workflow. No physical licence dongle is required.",
  model="LS2",
  specs=[("Camera configuration", "2 × 2.4 MP"), ("Accuracy (ISO 12836)", "6 µm (direction of limit to be confirmed)"),
         ("Full-arch scan", "11 s"), ("Full-arch impression scan", "27 s"), ("Scan area", "60 × 84 × 106 mm"),
         ("Scanner dimensions", "393 × 271 × 274 mm"), ("Weight", "9 kg"), ("Package dimensions", "40 × 40 × 50 cm")] + _dp_shared,
  applications=["Gypsum models", "Impressions", "Dies", "Articulators", "Wax-ups"],
  tags=["scanner", "blue light", "true colour", "LS series"], doc="denpark-ls2", page=1, img=IDX(DPL, 3, 3))
P("denpark", "LS3 Dental Laboratory Scanner", "equipment", "scanners-imaging",
  "Dual 5.0 MP camera scanner with ≤5 µm stated accuracy and a 13-second full-arch scan.",
  "Highest camera resolution in the LS series for detailed model acquisition, with true-colour texture and open STL/PLY/OBJ output.",
  model="LS3",
  specs=[("Camera configuration", "2 × 5.0 MP"), ("Accuracy (ISO 12836)", "≤ 5 µm"), ("Full-arch scan", "13 s"),
         ("Full-arch impression scan", "29 s"), ("Scan area", "94 × 89 × 60 mm"), ("Scanner dimensions", "393 × 271 × 274 mm"),
         ("Weight", "9 kg"), ("Package dimensions", "50 × 40 × 40 cm")] + _dp_shared,
  applications=["Gypsum models", "Impressions", "Dies", "Articulators", "Wax-ups"],
  tags=["scanner", "blue light", "high resolution", "LS series"], doc="denpark-ls", page=4, img=IDX(DPL, 4, 3), featured=True)
P("denpark", "LS4 Dental Laboratory Scanner", "equipment", "scanners-imaging",
  "Speed-focused laboratory scanner: 9-second full-arch scan, 19 seconds for an impression, 6 kg body.",
  "The fastest and lightest scanner in the LS series, with blue-light scanning, true-colour textures and open STL/PLY/OBJ export.",
  model="LS4",
  specs=[("Camera configuration", "2 × 2.4 MP"), ("Accuracy (ISO 12836)", "≤ 6 µm"), ("Full-arch scan", "9 s"),
         ("Full-arch impression scan", "19 s"), ("Scan area", "96 × 82 × 60 mm"), ("Scanner dimensions", "393 × 271 × 264 mm"),
         ("Weight", "6 kg"), ("Package dimensions", "50 × 40 × 40 cm")] + _dp_shared,
  applications=["Gypsum models", "Impressions", "Dies", "Articulators", "Wax-ups"],
  tags=["scanner", "fast", "lightweight", "LS series"], doc="denpark-ls", page=5, img=IDX(DPL, 5, 3))
P("denpark", "IOS-C5 Intraoral Scanner", "equipment", "scanners-imaging",
  "Lightweight 200 g intraoral scanner: 10 µm accuracy, up to 38 FPS, USB 3.0 plug-and-play, ultra-realistic texture.",
  "A handheld intraoral scanner for fast, touchless digital impressions, supplied with a standard and a mini scanning tip.",
  model="IOS-C5",
  specs=[("Accuracy (ISO 12836)", "10 µm"), ("Scanning depth", "20-25 mm"), ("Scan area (standard tip)", "16 × 7.5 mm"),
         ("Scan area (mini tip)", "12 × 7.0 mm"), ("Frame rate", "Up to 38 FPS"), ("Light source", "LED"),
         ("Dimensions", "245 × 40 × 38 mm"), ("Weight", "200 g"), ("Output", "STL, PLY, OBJ"), ("Connector", "USB 3.0"),
         ("Power input", "12 V DC")],
  features=["Fast scanning", "Single-line support, plug and play", "Touchless motion control", "Ultra-realistic texture mapping"],
  tags=["intraoral scanner", "IOS"], doc="denpark-c5", page=1,
  img=IDX("DENPARK/C5 EN 2.pdf", 2, 2), featured=True)

# ======================================================================================
# DISC (cutting and separating disks)
# ======================================================================================
_DISC = "DISC/SpectraCeram_Cutting_Disks_2026_SpectraIdentity_v5.pdf"
_disc_profiles = {1: ("Mounted", "Standard"), 2: ("Mounted", "Standard"), 3: ("Mounted", "Standard"), 4: ("Mounted", "Medium"),
                  5: ("Mounted", "Small"), 6: ("Unmounted", "Standard"), 7: ("Unmounted", "Standard"),
                  8: ("Unmounted", "Standard"), 9: ("Unmounted", "Standard"), 10: ("Unmounted", "Standard"),
                  11: ("Unmounted", "Standard"), 12: ("Mounted", "Standard"), 13: ("Unmounted", "Standard"),
                  14: ("Unmounted", "Standard"), 15: ("Unmounted", "Standard"), 16: ("Unmounted", "Standard")}
_disc_page = {1: 5, 2: 5, 3: 5, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6, 9: 7, 10: 7, 11: 7, 12: 7, 13: 8, 14: 8, 15: 8, 16: 8}
for n, (mount, size) in _disc_profiles.items():
    code = "%03d" % n
    extra = {4: "Same geometry as profile 03, medium diameter.", 5: "Same geometry as profile 03, small diameter."}.get(n, "")
    mount_txt = "integral mandrel" if mount == "Mounted" else "centre bore, fits a standard mandrel"
    P("disc", "Cutting Disk Profile %02d" % n, "material", "tools-finishing",
      "Diamond-coated %s rotary disk (%s size) in 0.15, 0.20 and 0.25 mm thicknesses." % (mount.lower(), size.lower()),
      ("Diamond-coated rotary disk for cutting and separating in dental and technical laboratories. Mount type: %s. %s "
       "Diameter and grit are pending manufacturer confirmation." % (mount_txt, extra)).strip(),
      model="SC-RD-xx%s" % code,
      specs=[("Mount type", mount), ("Size class", size), ("Thicknesses", "0.15 / 0.20 / 0.25 mm"),
             ("Order codes", "SC-RD-15%s / SC-RD-20%s / SC-RD-25%s" % (code, code, code))],
      tags=["diamond disk", "cutting", mount.lower()], doc="disc-catalog", page=_disc_page[n],
      img=NTH(_DISC, _disc_page[n], (n - 1) % 4), pid="disc-cutting-disk-profile-%02d" % n)

# ======================================================================================
# ERAYLAR
# ======================================================================================
P("eraylar", "ERAY DELUXE Acrylic Teeth", "material", "artificial-teeth",
  "Three-layer, fluorescent, cross-linked acrylic teeth: 36 shades, 33 upper anterior, 12 lower anterior, 7 posterior moulds.",
  "Premium acrylic denture teeth with anatomical design, compact colour stability and high wear resistance, "
  "supplied in sets of 6, 8 and 28. Certified to ISO 22112:2010 and EN ISO 13485:2016, CE 2292.",
  specs=[("Layers", "3 (fluorescent, cross-linked acrylic)"), ("Shades", "36 (VITA and IVOCLAR shade ranges)"),
         ("Upper anterior moulds", "33"), ("Lower anterior moulds", "12"), ("Posterior moulds", "7"),
         ("Sets", "6, 8 or 28 teeth"), ("Standards", "ISO 22112:2010, EN ISO 13485:2016, CE 2292")],
  tags=["acrylic teeth", "denture teeth", "ISO 22112"], doc="eraylar-deluxe", page=2,
  img=CROP("ERAYLAR/eraydeluxetureng_2022-01-25_21-14-12.pdf", 2, (0.26, 0.10, 0.88, 0.31)), featured=True)
P("eraylar", "ERAY Acrylic Teeth", "material", "artificial-teeth",
  "Three-layer fluorescent cross-linked acrylic teeth: 16 shades, 20 upper anterior, 7 lower anterior, 6 posterior moulds.",
  "Standard-line acrylic denture teeth with the same three-layer fluorescent construction, in sets of 6, 8 and 28. "
  "Source chart is in Turkish; details translated.",
  specs=[("Layers", "3 (fluorescent, cross-linked acrylic)"), ("Shades", "16"), ("Upper anterior moulds", "20"),
         ("Lower anterior moulds", "7"), ("Posterior moulds", "6"), ("Sets", "6, 8 or 28 teeth"),
         ("Standards", "ISO 22112:2010, EN ISO 13485:2016, CE 2292")],
  tags=["acrylic teeth", "denture teeth"], doc="eraylar-eray", page=2,
  img=CROP("ERAYLAR/erayturkce_2022-01-25_20-59-30.pdf", 2, (0.26, 0.10, 0.88, 0.31)))

# ======================================================================================
# FDT Resin / IMT / LUSTRA / PHT / TCS  (promotional images only; details limited to what is shown)
# ======================================================================================
FDT = "FDT RESIN/640975027_122143528886984518_2842161728675068164_n.jpg"
P("fdt-resin", "Pro Model Resin", "material", "resins",
  "FDT 3D-printing resin for dental models, available in several colours.",
  "Pro Model Resin is FDT's 3D-print material for dental models, shown in beige, orange, grey and white bottles.",
  tags=["3D printing", "model resin"], img=FCROP(FDT, (0.05, 0.27, 0.92, 0.88)), featured=False)
P("fdt-resin", "Wax Resin", "material", "resins",
  "FDT wax resin for 3D printing.", "Wax Resin is a 3D-print material in FDT's range, supplied in a green bottle.",
  tags=["3D printing", "wax resin"], img=FCROP(FDT, (0.395, 0.28, 0.585, 0.88)))
IMT = "IMT METAL POWDER/472892700_122164775240272744_4389916170306438226_n.jpg"
P("imt-metal-powder", "NiCr Metal Powder", "material", "metal-powders",
  "Nickel-chromium metal powder for dental 3D printing, in 10-30, 15-45 and 15-53 µm particle sizes.",
  "NiCr powder for dental 3D printing. IMT states ISO 13485, ISO 9001, CE and FDA certification in its brochure.",
  specs=[("Particle size", "10-30 µm / 15-45 µm / 15-53 µm"), ("Hall flow", "≤ 50 / ≤ 25 / ≤ 20 s per 50 g"),
         ("Composition (wt%)", "Ni 58.4-62, Cr 24-26.9, Mo 11-12.9, Si 0.56-1.6"), ("Tap density", "5.32 g/cm³"),
         ("Apparent density", "4.65 g/cm³"), ("Thermal expansivity", "13.6-13.8 ×10⁻⁶/K (20-600 °C)")],
  tags=["NiCr", "3D printing", "metal powder"], doc="imt-nicr", page=1,
  img=FCROP(IMT, (0.02, 0.52, 0.32, 0.90)),
  gallery=[FCROP("IMT METAL POWDER/473046366_122164775384272744_4999280838986915406_n.jpg", (0.0, 0.0, 1.0, 1.0))])
P("lustra", "LUSTRA CAD/CAM Block", "material", "zirconia-ceramics",
  "LUSTRA CAD/CAM restorative blocks with metal mandrel, shown in shades A1 and A3.",
  "LUSTRA blocks for chairside and laboratory milling. The material type is not stated in the supplied material.",
  tags=["CAD/CAM block"], img=FCROP("LUSTRA/641593402_122143527728984518_9065227016658325646_n.jpg", (0.10, 0.02, 0.62, 0.76)))
PHT1 = "PHT/626686995_122139592922984518_4624650351601240929_n.jpg"
PHT2 = "PHT/627865844_122139719414984518_9167817366591430566_n.jpg"
P("pht", "Diamond Stone", "material", "tools-finishing",
  "PHT Diamond Stone polishing set: mounted diamond stones and wheels on a bench tray.",
  "A tray of diamond stone polishers in cone and wheel shapes.",
  tags=["polishing", "diamond"], img=FCROP(PHT1, (0.02, 0.18, 0.98, 0.86)))
P("pht", "Diamond Rubber", "material", "tools-finishing",
  "PHT Diamond Rubber polishers in three grades, colour-coded on trays.",
  "Diamond rubber polishers in coloured wheel and point forms, supplied on trays numbered 1, 2 and 3.",
  tags=["polishing", "diamond rubber"], img=FCROP(PHT2, (0.5, 0.0, 1.0, 0.5)))
TCSJ = "TCS/643877422_122144093774984518_7424982704670682716_n.jpg"
_tcs_doc = None
P("tcs", "iFlex", "material", "resins",
  "Polyolefin thermoplastic for flexible partials: clinically unbreakable, stain-free, highly translucent.",
  "Ideal for technicians new to flexible partials. Easy to finish and polish; available in 5 translucent shades.",
  specs=[("Type", "Polyolefin thermoplastic"), ("Injection, 25 mm cartridge", "450 °F / 13 min"),
         ("Injection, 22 mm cartridge", "500 °F / 10 min"),
         ("Shades", "Light Pink, Standard Pink, Light Dark Pink, Dark Pink, Natural (clasps)")],
  features=["Clinically unbreakable", "Easy to finish and polish", "Stain-free", "High translucency"],
  tags=["thermoplastic", "flexible partial"], img=FCROP(TCSJ, (0.02, 0.27, 0.50, 0.79)))
P("tcs", "Unbreakable", "material", "resins",
  "Nylon thermoplastic for flexible partials with proven success and a guaranteed-unbreakable claim.",
  "Nylon thermoplastic with an ideal degree of flexibility, lightweight and durable; available in 5 translucent shades.",
  specs=[("Type", "Nylon thermoplastic"), ("Injection, 25 mm cartridge", "550 °F / 11 min"),
         ("Injection, 22 mm cartridge", "518 °F / 8-9 min"),
         ("Shades", "Light Pink, Standard Pink, Light Dark Pink, Dark Pink, Natural (clasps)")],
  features=["Ideal degree of flexibility", "Lightweight and durable", "Unbeatable strength"], tags=["thermoplastic", "nylon"])
P("tcs", "Karadent", "material", "resins",
  "Semi-rigid microcrystalline polymer for full dentures, clear clasps, frameworks, partials and nightguards.",
  "Semi-rigid microcrystalline polymer with no volume shrinkage and minimal water absorption; easy to repair, rebase and reline with acrylic.",
  specs=[("Type", "Semi-rigid microcrystalline polymer"), ("Injection, 25 mm cartridge", "540 °F / 14-16 min"),
         ("Injection, 22 mm cartridge", "527 °F / 11-12 min"), ("Shades", "Standard Pink, Clear")],
  features=["Exceptional fit, no volume shrinkage", "Minimal water absorption", "Quick to finish and polish"],
  applications=["Full dentures", "Clear clasps", "Frameworks", "Partial dentures", "Nightguards"], tags=["thermoplastic", "semi-rigid"])
P("tcs", "Totally Natural", "material", "resins",
  "Semi-rigid, translucent methacrylate for full dentures; light, comfortable and repairable with any acrylic.",
  "A semi-rigid, semi-clear methacrylate injection resin, available in Standard Pink.",
  specs=[("Type", "Semi-rigid methacrylate"), ("Injection, 25 mm cartridge", "550 °F / 18-20 min"),
         ("Injection, 22 mm cartridge", "554 °F / 16-18 min"), ("Shade", "Standard Pink")],
  features=["Semi-rigid", "Translucent, semi-clear", "Easy to repair with any acrylic", "Lightweight and comfortable"],
  applications=["Full dentures"], tags=["thermoplastic", "methacrylate"], img=FCROP(TCSJ, (0.50, 0.27, 0.98, 0.79)))

# ======================================================================================
# Profeta
# ======================================================================================
P("profeta", "C120 Classical Dental Printer", "equipment", "milling-printing",
  "Compact dental metal 3D printer (CoCr): ø120 × 70 mm build volume, 300 W fibre laser, 130 copings in 4-5 hours.",
  "Dedicated dental metal 3D printer for small and mid-size labs, easy to start with cobalt-chromium printing and "
  "compact enough to move through an elevator. Sold with a one-stop package (design software, slicing software, furnace, nitrogen generator).",
  model="C120",
  specs=[("Building volume", "ø120 mm, z = 70 mm"), ("Layer thickness", "20-50 µm"), ("Scanning speed", "15 m/s (max)"),
         ("Productivity", "130 copings / 4-5 h; 10 RPD frames / 3.5-4 h"), ("Laser", "Yb-fiber, 300 W"),
         ("Laser beam diameter", "40-60 µm"), ("Power", "AC 220 V, 12 A, 2.5 kW"), ("Shielding gas", "Nitrogen"),
         ("Machine dimensions", "900 × 680 × 1760 mm"), ("Weight", "480 kg"), ("Operating temperature", "18-30 °C"),
         ("Materials", "CoCr")],
  applications=["Copings", "RPD frames", "Implant bars", "Surgical guides", "Orthodontic appliances"],
  tags=["metal 3D printer", "CoCr", "SLM"], doc="profeta-c120", page=2, img=IDX("PROFETA/C120-EN-V2.pdf", 2, 0))
P("profeta", "C150 Classical Dental Printer", "equipment", "milling-printing",
  "Dental metal 3D printer with single or dual 300/500 W laser, ø158 × 70 mm volume, 220 copings in 4-4.5 hours.",
  "Economic-model metal printer for labs of all sizes, with a larger build volume, higher powder utilisation and "
  "two layer-thickness options (30/40 µm). Printing materials include CoCr, Ti and TC4.",
  model="C150",
  specs=[("Building volume", "ø158 mm, z = 70 mm"), ("Layer thickness", "20-50 µm"), ("Scanning speed", "15 m/s (max)"),
         ("Productivity", "220 copings / 4-4.5 h; 15 RPD frames / 3.5-4 h"), ("Laser", "Yb-fiber (single / dual), 300 W / 500 W"),
         ("Laser beam diameter", "40-60 µm"), ("Power", "AC 220 V, 16 A, 3.5 kW"), ("Shielding gas", "Argon / nitrogen"),
         ("Machine dimensions", "1070 × 670 × 1750 mm"), ("Weight", "500 kg"), ("Operating temperature", "18-30 °C"),
         ("Materials", "CoCr, Ti, TC4")],
  applications=["Copings", "RPD frames", "Implant bars", "Surgical guides", "Orthodontic appliances"],
  tags=["metal 3D printer", "CoCr", "titanium"], doc="profeta-c150", page=2, img=IDX("PROFETA/C150EN.pdf", 2, 1), featured=True)

# ======================================================================================
# Teknik Dental
# ======================================================================================
P("teknik-dental", "tegra MP100S Porcelain Furnace", "equipment", "furnaces",
  "Economical flagship porcelain furnace with 100 programs, 17 parameters and a large colour touch screen.",
  "A porcelain furnace built on quality electronics, resistance and precision thermocouple, compatible with all "
  "powders, with vacuum-assisted fast cooling and an energy-saving sleep mode. 2-year guarantee.",
  model="MP100S",
  specs=[("Programs", "100 (17 parameters each)"), ("Display", "Large colour touch screen"),
         ("Heaters", "Enclosed in quartz spiral glass"), ("Cooling", "Vacuum-assisted fast cooling"),
         ("Guarantee", "2 years")],
  features=["Adjustable parameters during an active cycle", "Energy-saving sleep mode", "Test functions and detailed error messages",
            "Perfect compatibility with all powders"],
  tags=["porcelain furnace", "tegra"], doc="teknik-mp100", page=1,
  img=IDX("TEKNIK DENTAL/MP100_Brochure_EN.pdf", 1, 7))
P("teknik-dental", "tegra MP1500 Speed Multistep", "equipment", "furnaces",
  "High-speed zirconia sintering furnace: 3 trays (30-60 units each), 1550 °C, single crowns in 90 minutes.",
  "Sintering furnace with 100 programs of 10 segments each, controlled cooling and a type R thermocouple, built for "
  "both urgent single-crown speed programs and non-stop batch production.",
  model="MP1500",
  specs=[("Target temperature", "100-1550 °C"), ("Heating rate", "1-40 °C/min"), ("Programs", "100, each with 10 segments"),
         ("Capacity", "3 sintering trays, 30-60 units each"), ("Chamber volume", "3.5 l"), ("Accuracy", "±1 °C"),
         ("Sensor", "Type R thermocouple"), ("Display", "7-inch colour touch screen"), ("Power", "220-230 VAC, 3200 W"),
         ("Dimensions (W × D × H)", "38 × 41 × 73 cm"), ("Weight", "55 kg"), ("Warranty", "2 years (heaters not covered)")],
  features=["Speed programs: single crowns in about 90 minutes", "Controlled lift opening and controlled cooling"],
  applications=["Monolithic, layered, pre-shaded and high-translucency zirconia"],
  tags=["sintering furnace", "zirconia", "tegra"], doc="teknik-mp1500", page=1,
  img=IDX("TEKNIK DENTAL/MP1500_Speed_Multistep_Brochure_EN_20230404.pdf", 1, 3), featured=True)

# ======================================================================================
# JJ Tools (series-level entries; the catalogue lists 18,619 tools in 278 items)
# ======================================================================================
JJ = "jj-catalog"
_jj = [
    ("JJ Series End Mills", 6, "Carbide end mills for hardened steels (HRc 52-68) with Si-based PVD coating and tight edge tolerance."),
    ("HARD Series High-Speed End Mills", 6, "End mills for pre-hardened and hardened steel (HRc 50-65) in high-speed cutting."),
    ("E Series Heavy-Cut End Mills", 7, "Heavy-cut end mills with Si coating and 0.5 µm micro-grain carbide for broad workpiece ranges."),
    ("CBN Series End Mills", 8, "PCBN end mills for precise finishing (±5 µm) of hardened steels up to HRc 72."),
    ("G Series General-Purpose End Mills", 145, "General-purpose end mills for multi-purpose machining."),
    ("V Series Ball End Mills", 169, "4-flute symmetry end mills for steel, cast iron and stainless steel."),
    ("End Mills for Graphite", 191, "3-flute diamond-coated end mills for graphite, reinforced plastics and carbon fibre."),
    ("End Mills for Copper", 213, "3-flute 45° helix corner-radius end mills for copper."),
    ("End Mills for Aluminum", 235, "End mills for aluminium, including the NEW high-feed Aluminum series."),
    ("End Mills for A.B.S", 279, "3-flute general-purpose end mills for A.B.S resin."),
    ("Carbide Drills", 301, "Carbide drills, including 2-flute step drills."),
    ("Thread Mills", 345, "Thread mills for ISO, pipe and UN threads."),
]
for nm, pg, sm in _jj:
    P("jj-tools", nm, "material", "tools-finishing", sm,
      sm + " Series-level entry from a general carbide-tooling catalogue; contact us for the exact item you need.",
      tags=["end mill", "carbide", "CNC tooling"], doc=JJ, page=pg)

# ======================================================================================
# Yamahachi
# ======================================================================================
def Y(name, cat, sub, summary, desc="", page=None, img=None, **kw):
    P("yamahachi", name, cat, sub, summary, desc, doc="yamahachi-catalog", page=page,
      img=IDX(YC, img[0], img[1]) if img else None, **kw)


_shades = "A1 A2 A3 A3.5 A4 B1 B2 B3 B4 C1 C2 C3 C4 D2 D3 D4 W0.5"
Y("NEW ACE", "material", "artificial-teeth", "Two-layer acrylic resin teeth (23 upper / 12 lower moulds, 17 shades) for full and partial dentures.",
  "Two-layer acrylic teeth that harmonise with natural teeth in shape and colour and are easy to arrange, with the wax gum festooned without difficulty.",
  page=3, img=(3, 3), specs=[("Layers", "2 (acrylic)"), ("Upper moulds", "23"), ("Lower moulds", "12"), ("Shades", _shades),
                             ("Packing", "6 pcs / set, 16 sets / box")], tags=["acrylic teeth", "AC"])
Y("NAPERCE", "material", "artificial-teeth", "Two-layer acrylic posterior teeth with a 30° cusp angle in six moulds (M28-M36).", "",
  page=3, img=(3, 5), specs=[("Layers", "2 (acrylic)"), ("Cusp angle", "30°"), ("Moulds", "M28 M30 M32 M33 M34 M36"),
                             ("Shades", _shades), ("Packing", "8 pcs / set, 12 sets / box")], tags=["acrylic teeth", "AC"])
Y("EFUCERA AC", "material", "artificial-teeth", "Two-layer acrylic posterior teeth with a 20° cusp angle in five moulds (28-36).", "",
  page=3, img=(3, 7), specs=[("Layers", "2 (acrylic)"), ("Cusp angle", "20°"), ("Moulds", "28 30 32 34 36"), ("Shades", _shades),
                             ("Packing", "8 pcs / set, 12 sets / box")], tags=["acrylic teeth", "AC"])
Y("MILLION", "material", "artificial-teeth", "One-layer acrylic posterior teeth with a 33° cusp angle in five moulds (28-32).", "",
  page=4, img=(4, 0), specs=[("Layers", "1 (acrylic)"), ("Cusp angle", "33°"), ("Moulds", "28 29 30 31 32"), ("Shades", _shades),
                             ("Packing", "8 pcs / set, 12 sets / box")], tags=["acrylic teeth", "AC"])
Y("FLAT AC", "material", "artificial-teeth", "Two-layer acrylic posterior teeth with a 0° (flat) cusp angle in moulds 30, 32 and 34.", "",
  page=4, img=(4, 2), specs=[("Layers", "2 (acrylic)"), ("Cusp angle", "0°"), ("Moulds", "30 32 34"), ("Shades", _shades),
                             ("Packing", "8 pcs / set, 12 sets / box")], tags=["acrylic teeth", "AC"])
Y("FX ANTERIOR", "material", "artificial-teeth", "Two-layer high-performance acrylic anterior teeth: 16 upper and 8 lower moulds, full 3-D natural form.",
  "A full 3-D reproduction of natural teeth with an improved labial ridge that emphasises labial surface morphology, allowing arrangements that duplicate natural teeth. Contains an abrasion-resistant filler.",
  page=5, img=(5, 0), specs=[("Layers", "2 (highly performed acrylic)"), ("Upper moulds", "16 (T4-T7, S4-S7, SS4-SS7, C4-C7)"),
                             ("Lower moulds", "8 (LA4-LA7, LB4-LB7)"), ("Shades", _shades), ("Packing", "6 pcs / set, 16 sets / box")],
  tags=["acrylic teeth", "FX"])
Y("FX POSTERIOR", "material", "artificial-teeth", "Two-layer high-performance acrylic posterior teeth with a 30° cusp angle in six moulds.", "",
  page=5, img=(5, 2), specs=[("Layers", "2 (highly performed acrylic)"), ("Cusp angle", "30°"), ("Moulds", "28 30 32 33 34 36"),
                             ("Shades", _shades), ("Packing", "8 pcs / set, 12 sets / box")], tags=["acrylic teeth", "FX"])
Y("CROWN NS", "material", "artificial-teeth", "Three-layer nanoSilica-reinforced hard acrylic anterior teeth: 24 upper and 8 lower moulds.",
  "A 3D-digital reproduction of natural anterior teeth with solid moulds that allow easy adjustment and a strong grip on the lingual gum. NS teeth (hardness Hv 25) resist abrasion about 60% better than conventional acrylic.",
  page=6, img=(6, 0), specs=[("Layers", "3 (hard acrylic with nanoSilica)"), ("Upper moulds", "24"), ("Lower moulds", "8"),
                             ("Shades", _shades), ("Hardness", "Hv 25"), ("Packing", "6 pcs / set, 16 sets / box")],
  tags=["acrylic teeth", "NS", "nanoSilica"])
Y("EFUCERA NS", "material", "artificial-teeth", "Three-layer nanoSilica-reinforced hard acrylic posterior teeth with a 20° cusp angle.", "",
  page=6, img=(6, 1), specs=[("Layers", "3 (hard acrylic with nanoSilica)"), ("Cusp angle", "20°"), ("Moulds", "28 30 32 34 36"),
                             ("Shades", _shades), ("Hardness", "Hv 25"), ("Packing", "8 pcs / set, 12 sets / box")],
  tags=["acrylic teeth", "NS", "nanoSilica"])
Y("CROWN PX", "material", "artificial-teeth", "Three-layer composite anterior teeth (Hv 45, over 5× the abrasion resistance of acrylic): 24 upper, 8 lower moulds.",
  "A 3D-digital reproduction of natural anterior teeth in stain-resistant composite, with solid moulds for easy adjustment and a strong grip on the lingual gum.",
  page=7, img=(7, 4), specs=[("Layers", "3 (composite)"), ("Upper moulds", "24"), ("Lower moulds", "8"), ("Shades", _shades),
                             ("Hardness", "Hv 45"), ("Packing", "6 pcs / set, 16 sets / box")], tags=["composite teeth", "PX"], featured=True)
Y("SOLUUT PX", "material", "artificial-teeth", "Three-layer composite anterior teeth with emphasised cervical and incisal areas for a natural appearance.",
  "Cervical and incisal areas are emphasised for a natural look, with sufficient dentin layers to avoid unnecessary translucency.",
  page=7, img=(7, 5), specs=[("Layers", "3 (composite)"), ("Upper moulds", "24 (T4-T7, S4-S7, SS4-SS7, O4-O7, C4-C7, CSP4-CSP7)"),
                             ("Lower moulds", "8 (L4-L7, LS4-LS7)"), ("Shades", _shades), ("Hardness", "Hv 45"),
                             ("Packing", "6 pcs / set, 16 sets / box")], tags=["composite teeth", "PX"])
Y("EFUCERA PX", "material", "artificial-teeth", "Three-layer composite posterior teeth, 20° cusp angle, full balanced occlusal form.",
  "Occlusal ridges are positioned eccentrically for full occlusal equilibrium, with contact points designed for denture stability and an imaginary setting line reserved for the technician's own arrangement.",
  page=8, img=(8, 15), specs=[("Layers", "3 (composite)"), ("Cusp angle", "20°"), ("Moulds", "28 30 32 34 36"), ("Shades", _shades),
                              ("Hardness", "Hv 45"), ("Packing", "8 pcs / set, 12 sets / box")], tags=["composite teeth", "PX"])
Y("Shade Guide AC", "material", "lab-supplies", "Shade guide for Yamahachi acrylic resin teeth (AC).", "", page=8, img=(8, 11), tags=["shade guide"])
Y("Shade Guide NS", "material", "lab-supplies", "Shade guide for Yamahachi hard acrylic resin teeth (NS).", "", page=8, img=(8, 7), tags=["shade guide"])
Y("Shade Guide PX", "material", "lab-supplies", "Shade guide for Yamahachi composite resin teeth (PX).", "", page=8, img=(8, 5), tags=["shade guide"])
Y("Teeth Cabinet", "material", "lab-supplies", "Six-pallet drawer cabinet; each pallet stores 48 anterior or 36 posterior Yamahachi tooth sets.", "",
  page=8, img=(8, 9), specs=[("Capacity per pallet", "48 anterior or 36 posterior sets"), ("Unit", "6-pallet drawer"),
                             ("Dimensions (1 unit)", "W285 × D310 × H220 mm")], tags=["storage"])

Y("ARTESANO Hybrid Composite Block", "material", "pmma-wax", "CAD/CAM hybrid composite resin block with pin for crowns and inlays; 194 MPa flexural strength.",
  "CAD/CAM milling hybrid composite resin block, fluorescent, for crowns and inlays.", page=10, img=(10, 10),
  specs=[("Type", "Block with pin"), ("Sizes", "S 10 × 12 × 15 mm; M 12 × 14 × 18 mm"), ("Packing", "5 pcs / box"),
         ("Shades", "A1 A2 A3 A3.5 A4"), ("3-point flexural strength", "194 MPa (JDMAS 245:2020)"),
         ("Compression strength", "526 MPa (independent test)"), ("Vickers hardness", "61 (JDMAS 245:2020)"), ("Fluorescence", "Yes")],
  applications=["Crowns", "Inlays"], tags=["CAD/CAM", "hybrid composite"], featured=True)
Y("PMMA Block (with Pin)", "material", "pmma-wax", "CAD/CAM acrylic blocks with pin (15.4 × 19 × 39 mm / 15.5 × 19 × 55 mm) for temporaries and casting frameworks.", "",
  page=10, img=(10, 14), specs=[("Sizes", "S 15.4 × 19 × 39 mm; M 15.5 × 19 × 55 mm"), ("Packing", "10 pcs / box"),
                                ("Shades", _shades + " Clear (other than A1-A3: minimum 5 boxes)")],
  applications=["Temporary crowns and bridges", "Model framework for casting"], tags=["PMMA", "CAD/CAM"])
Y("PMMA Block for ROLAND DWX-4", "material", "pmma-wax", "76 × 40 × 20 mm PMMA blocks without pin for Roland DWX-4 (A1-A3).", "",
  page=10, img=(10, 12), specs=[("Size", "76 × 40 × 20 mm"), ("Packing", "5 pcs / box"), ("Shades", "A1 A2 A3")],
  applications=["Temporary crowns and bridges", "Model framework for casting"], tags=["PMMA", "Roland"])
Y("PMMA Disk Mono-Layer", "material", "pmma-wax", "Single-colour PMMA disc, ø98.5 mm, 10-30 mm thick, in 17 shades plus clear.",
  "Open-system PMMA discs for temporaries and casting frameworks; clear discs are also available for nightguards, splints and surgical guides.",
  page=10, img=(10, 8), specs=[("Diameter", "ø98.5 mm (open); ø95 mm Zirkonzahn; ø101 mm Amann Girrbach"),
                               ("Thickness (open)", "10 12 14 15 16 18 20 22 25 30 mm (clear also 35 mm)"),
                               ("Packing", "1 pc / box"), ("Shades", _shades + " Clear")],
  applications=["Temporary crowns and bridges", "Model framework for casting", "Clear: nightguards, splints, surgical guides"],
  tags=["PMMA", "disc"], featured=True)
Y("PMMA Disk V-Pink", "material", "pmma-wax", "Pink PMMA denture-base disc, ø98.5 mm, in 18-30 mm thicknesses.", "",
  page=10, img=(10, 4), specs=[("Diameter", "ø98.5 mm (open)"), ("Thickness", "18 20 22 25 30 mm"), ("Packing", "1 pc / box"), ("Colour", "V-Pink")],
  applications=["Denture production"], tags=["PMMA", "denture"])
Y("PMMA Disk Multi-Layer", "material", "pmma-wax", "8-layer PMMA disc with a natural colour gradient, ø98.5 × 20 mm, for crowns, bridges and denture teeth.", "",
  page=10, img=(10, 7), specs=[("Layers", "8-layer concept"), ("Diameter", "ø98.5 mm (open)"), ("Thickness", "20 mm"),
                               ("Packing", "1 pc / box"), ("Shades", "A3 (A1, A2 etc. coming soon)")],
  applications=["Crowns and bridges", "Denture teeth production"], tags=["PMMA", "multilayer"])
Y("PMMA Disk Dual Color", "material", "pmma-wax", "Two-colour PMMA disc (V-Pink + tooth shade), 35 mm (17.5 + 17.5), for dentures.", "",
  page=10, img=(10, 1), specs=[("Diameter", "ø98.5 mm (open)"), ("Thickness", "35 mm (17.5 + 17.5 mm)"), ("Packing", "1 pc / box"),
                               ("Shades", "V-Pink + A1, A2, A3, A3.5, B2, C2")],
  applications=["Denture production", "Copy denture", "Temporary denture"], tags=["PMMA", "dual color"])
Y("Wax Disk", "material", "pmma-wax", "CAD/CAM milling wax disc, ø98.5 mm, 10-25 mm thick, in green, ivory or blue.", "",
  page=11, img=(11, 5), specs=[("Diameter", "ø98.5 mm (open); ø95 mm Zirkonzahn; ø101 mm Amann Girrbach"),
                               ("Thickness (open)", "10 12 14 15 16 18 20 22 25 mm"), ("Packing", "1 pc / box"),
                               ("Colour", "Green, Ivory, Blue")], applications=["Model framework for casting"], tags=["wax", "CAD/CAM"])
Y("Wax Disk α", "material", "pmma-wax", "Gray CAD/CAM wax disc for frameworks invested with cristobalite for rapid-heating casting.", "",
  page=11, img=(11, 7), specs=[("Diameter", "ø98.5 mm (open)"), ("Thickness", "10 12 14 15 16 18 20 22 25 mm"),
                               ("Packing", "1 pc / box"), ("Colour", "Gray")],
  applications=["Frameworks invested in cristobalite for rapid heating (gold and palladium alloys)", "Model framework for casting"],
  tags=["wax", "CAD/CAM"])
Y("Wax Block for ROLAND DWX-4", "material", "pmma-wax", "76 × 40 × 20 mm green wax blocks without pin for Roland DWX-4.", "",
  page=11, img=(11, 1), specs=[("Size", "76 × 40 × 20 mm"), ("Packing", "5 pcs / box"), ("Colour", "Green")],
  applications=["Model framework for casting"], tags=["wax", "Roland"])

Y("TrinDy Model", "material", "resins", "TPO-free 3D-printing resin for dental models: 65-75 MPa flexural strength, 1,000 g bottle.",
  "Designed for dental model fabrication with excellent printing accuracy, high-temperature elasticity and liquid stability. Tested on an ASIGA MAX with Otoflash post-curing (1 × 2000 flashes).",
  page=13, img=(13, 2), specs=[("Flexural strength (ISO 178)", "65-75 MPa"), ("Flexural modulus (ISO 178)", "≥ 2300 MPa"),
                               ("Shore hardness (ISO 48-4)", "≥ D80"), ("Viscosity", "450-550 mPa·s"),
                               ("Packing", "1,000 g bottle"), ("Colours", "Gray, Beige, Yellow, Brown")],
  applications=["Thermoforming models", "Orthodontic models", "Crown and bridge models", "Diagnostic models", "Implant analog models"],
  tags=["3D printing", "TPO free"], featured=True)
Y("TrinDy Cast", "material", "resins", "TPO-free castable 3D-printing resin with clean burn-out for casting and pressing patterns.",
  "Designed for dental cast fabrication with excellent printing accuracy and clean burn-out on micro-wax. Tested on an ASIGA MAX.",
  page=13, img=(13, 9), specs=[("Flexural strength (ISO 178)", "20 MPa"), ("Flexural modulus (ISO 178)", "640 MPa"),
                               ("Shore hardness (ISO 48-4)", "≥ D65"), ("Viscosity", "300-400 mPa·s"),
                               ("Packing", "1,000 g / 500 g bottle"), ("Colour", "Yellow")],
  applications=["Patterns for casting and pressing", "Crown and bridge", "Removable partial denture frameworks"], tags=["3D printing", "castable"])
Y("TrinDy Mask", "material", "resins", "TPO-free elastic 3D-printing resin for gingiva masks and soft tissue on implant models.",
  "Designed for gingiva mask fabrication, with elasticity and tear strength that let operators feel gum tissue on simulation models.",
  page=14, img=(14, 18), specs=[("Tensile strength (ASTM D412)", "2 MPa"), ("Elongation at break (ASTM D412)", "110%"),
                                ("Shore hardness (ISO 48-4)", "≥ A65"), ("Viscosity", "850-950 mPa·s"),
                                ("Packing", "1,000 g bottle"), ("Colour", "Pink")],
  applications=["Gingiva masks", "Soft tissue for implant models"], tags=["3D printing", "elastic"])

Y("BASIS", "material", "resins", "Heat-curing acrylic resin for denture bases (78.7 MPa flexural strength, ISO 20795-1).",
  "Heat-curing denture-base acrylic made of particles of various sizes that reinforce denture solidity. Cure in boiling water for 30-40 minutes.",
  page=15, img=(15, 6), specs=[("Powder / liquid ratio", "100 : 43 g:mL"), ("Flexural strength", "78.7 MPa"), ("Flexural modulus", "2813 MPa"),
                               ("Sorption", "25.1 µg/mm³"), ("Solubility", "0 µg/mm³"),
                               ("Shades", "Clear, O Pink*, V Pink*, LF Pink*, LFα*, Light Pink, Pink, Dark Pink (*vein-fibre shades)")],
  tags=["denture base", "heat-curing"])
Y("BASIS HI", "material", "resins", "Impact-resistant heat-curing denture base resin allowing thinner bases (79.3 MPa).",
  "More impact-resistant than standard denture base resin, so the base can be made thinner.", page=15, img=(15, 5),
  specs=[("Powder / liquid ratio", "100 : 43 g:mL"), ("Flexural strength", "79.3 MPa"), ("Flexural modulus", "2558 MPa"),
         ("Sorption", "24.8 µg/mm³"), ("Solubility", "0.2 µg/mm³"), ("Residual monomer", "0.64 wt%"),
         ("Shades", "O Pink, V Pink, LF Pink, LFα (all vein-fibre)")], tags=["denture base", "heat-curing"])
Y("BASIS TWIN CURE", "material", "resins", "Denture base resin for both heat-shock and microwave curing (3 min at 500 W).",
  "Cure by heat shock (15 min in boiling water) or microwave (3 min at 500 W in an SS FRP flask), reducing porosity compared with conventional resin.",
  page=15, img=(15, 2), specs=[("Powder / liquid ratio", "100 : 40 g:mL"), ("Flexural strength", "79.5 MPa (heat shock) / 68.9 MPa (microwave)"),
                               ("Flexural modulus", "2842 / 2387 MPa"), ("Residual monomer", "0.99 / 0.51 wt%")],
  tags=["denture base", "microwave"])
Y("BASIS FLOW II", "material", "resins", "Multipurpose self-curing pourable acrylic (cold-curing) with 77.6 MPa flexural strength.",
  "Pourable cold-curing acrylic; pressure-cure for 30-60 minutes at 55 °C and 0.2 MPa.", page=15, img=(15, 29),
  specs=[("Powder / liquid ratio", "100 : 60 g:mL"), ("Flexural strength", "77.6 MPa"), ("Flexural modulus", "2578 MPa"),
         ("Shades", "Clear, O Pink*, V Pink*, LF Pink*, LFα*")], tags=["denture base", "self-curing"])
Y("BASIS ELAST", "material", "resins", "Monomer-free polyamide thermoplastic for non-metal-clasp dentures, with moderate elasticity.",
  "A rigid-type, monomer-free polyamide denture base with moderate elasticity, injected at 290 °C; repairable with self-curing resin and relinable.",
  page=16, img=(16, 39), specs=[("Material", "Polyamide thermoplastic"), ("Flexural strength", "55.3 MPa"), ("Flexural modulus", "1252 MPa"),
                                ("Sorption", "30.4 µg/mm³"), ("Injection", "290 °C, 17 min, 0.8 MPa; flask 60-90 °C"),
                                ("Packing", "300 g"), ("Shade", "Marble α")], tags=["thermoplastic", "polyamide"])
Y("ACRY PELLET", "material", "resins", "Thermoplastic acrylic denture-base pellets (47.9 MPa) with a vascular pattern, 1 kg.",
  "Acrylic thermoplastic injection pellets; dry for 6 hours at 80 °C before injection.", page=16, img=(16, 35),
  specs=[("Material", "Thermoplastic acrylic"), ("Flexural strength", "47.9 MPa"), ("Flexural modulus", "1517 MPa"),
         ("Sorption", "24.9 µg/mm³"), ("Injection", "275 °C, 22 min, 9 atm; flask 100 °C"), ("Packing", "1 kg"), ("Shade", "Marble H")],
  tags=["thermoplastic", "acrylic"])
Y("BASIS PC", "material", "resins", "Semi-flexible polycarbonate injection resin (92.4 MPa), odourless and allergen-free, for full and partial dentures.",
  "New semi-flexible thermoplastic injection resin that is allergic-reaction-free, odourless and easy to polish.", page=16, img=(16, 37),
  specs=[("Material", "Polycarbonate thermoplastic"), ("Flexural strength", "92.4 MPa"), ("Flexural modulus", "2255 MPa"),
         ("Sorption", "5.9 µg/mm³"), ("Solubility", "0.2 µg/mm³"), ("Injection", "305 °C, 25 min, 0.9 MPa; flask 90 °C"),
         ("Packing", "1 kg"), ("Shades", "Clear, Clear Pink, Marble, Pink")], applications=["Full dentures", "Partial dentures"],
  tags=["thermoplastic", "polycarbonate"])
Y("PROVIFINE", "material", "resins", "Fast-setting self-curing resin (3-5 min) with high flow when pouring and low sag when brush-loading.",
  "Self-curing resin for inlays, crowns, bridges and denture repairs; easy to build up with a brush and shape without hanging.",
  page=16, img=(16, 13), specs=[("Powder / liquid ratio", "100 : 50 g:mL"), ("Hardening time (23 °C)", "5 min (normal) / 3 min (fast)"),
                                ("Flexural strength", "72.1 / 75.9 MPa"), ("Shades", "Clear, LF Pink, LFα, A1, A2, A3"),
                                ("Packing", "Powder 50 g / 250 g; liquid 100 mL / 260 mL")],
  applications=["Inlays, crowns and bridges", "Denture repairs"], tags=["self-curing", "repair"])
Y("PATTERN BRIGHT", "material", "resins", "Self-curing pattern acrylic with 0.05% incineration residue and low polymerization shrinkage.",
  "Self-curing resin for patterns on metal plates, lingual and palatal bars, clasps, telescope crowns and bonded bridges; also for implant jigs.",
  page=17, img=(17, 1), specs=[("Powder / liquid ratio", "100 : 50 g:mL"), ("Hardening time (23 °C)", "3 min 27 s"),
                               ("Flexural strength", "68 MPa (JIS T6518:2011)"), ("Polymerization shrinkage", "0.60% (5 min) / 0.91% (24 h)"),
                               ("Incineration residue (700 °C)", "0.05% (ISO 1584:2021)"), ("Packing", "100 g powder + 100 mL liquid, pink")],
  tags=["pattern resin", "self-curing"])
Y("RE-FINE BRIGHT", "material", "resins", "Fast-setting self-curing acrylic (3 min 15 s) for inlays, temporaries and denture repairs.",
  "Self-curing resin available in vein-fibre pinks and tooth shades A2-A3.5.", page=17, img=(17, 8),
  specs=[("Powder / liquid ratio", "1 : 0.5"), ("Hardening time (23 °C)", "3 min 15 s"), ("Flexural strength", "56 MPa"),
         ("Shades", "Clear, O Pink, V Pink, LF Pink, LFα, Pink, A2, A3, A3.5"), ("Packing", "250 g powder + 260 mL liquid")],
  applications=["Inlays", "Temporary crowns and bridges", "Denture repairs"], tags=["self-curing", "repair"])
Y("BASING RESIN", "material", "resins", "Non-adhesive self-curing acrylic for custom trays and base plates (and the wax-adherent BASING RESIN α).",
  "Moulds by spatula or fingers; BASING RESIN α is formulated for firmer adherence of wax on bases and trays.",
  page=17, img=(17, 19), specs=[("Powder / liquid ratio", "100 : 35 g:mL"),
                                ("Hardening time (normal / slow liquid)", "5 min 5 s / 7 min 48 s (α: 5 min 32 s / 7 min 20 s)"),
                                ("Colours", "Pink, Blue"), ("Packing", "1 kg powder + 500 mL liquid")],
  tags=["custom tray", "base plate"])
Y("LIGHT RESIN PLATE", "material", "resins", "Pre-formed light-curing plates for custom trays and base plates, cured in about 30 seconds.",
  "No powder/liquid mixing; uniform thickness; polymerises with LED TRAY CURE in roughly 30 seconds.", page=17, img=(17, 6),
  specs=[("Colour", "Pink"), ("Effective wavelength", "360-400 nm"), ("Thickness", "2.2 mm or 1.5 mm (50 pcs / box)")],
  applications=["Custom trays", "Base plates"], tags=["light-curing", "custom tray"])
Y("ORTHO BRIGHT", "material", "resins", "Self-curing orthodontic acrylic (~8 min working time) for splints, appliances and temporary dentures.",
  "Sprinkle, mixing, packing or brush-on techniques; about 8 minutes of working time.", page=18, img=(18, 0),
  specs=[("Shades", "Clear, Pink"), ("Starter kit", "100 g powder + 70 mL liquid"), ("Retail", "500 g powder + 250 mL liquid")],
  applications=["Splints", "Functional orthodontic appliances", "Deciduous dentures", "Temporary dentures", "Individual trays"],
  tags=["orthodontic", "self-curing"])
Y("ORTHO BRIGHT COLOR", "material", "resins", "Coloured self-curing orthodontic acrylic in Clear, Blue, Red, Orange and Green.",
  "Colour variant of ORTHO BRIGHT for orthodontic appliances.", page=18, img=(18, 1),
  specs=[("Shades", "Clear, Blue, Red, Orange, Green"), ("Starter kit", "50 g × 5 shades + 70 mL liquid"),
         ("Retail", "250 g powder + 250 mL liquid")], tags=["orthodontic", "self-curing"])

Y("PARAFFIN WAX", "material", "pmma-wax", "Dental paraffin wax sheets (146 × 74 mm or 170 × 85 mm, 1.4 mm) in soft and medium.", "",
  page=19, img=(19, 2), specs=[("Packing", "500 g / 1 kg / 5 lbs"), ("Type", "Soft / medium"), ("Colour", "Light pink, pink"),
                               ("Size", "Regular 146 × 74 × 1.4 mm; large 170 × 85 × 1.4 mm")], tags=["wax"])
Y("ROLLING WAX", "material", "pmma-wax", "Pliable pink sprue wax in 5, 6, 7 and 8 mm diameters with a protective dispenser box.", "",
  page=19, img=(19, 0), specs=[("Packing", "270 g / box"), ("Diameter", "5, 6, 7, 8 mm"), ("Colour", "Pink")],
  features=["Pliable for straightforward sprue applications", "Dispenser box protects the wax"], tags=["wax", "sprue"])
Y("CARVING WAX", "material", "pmma-wax", "Carving wax cylinders and sticks that burn out clean, in ivory, gray, red, blue and green.",
  "For modelling and waxing-up. Superb solidity, high opacity and colour stability, minimal chipping.", page=19, img=(19, 1),
  specs=[("Type", "Cylinder 50 g; stick 140 g (60 sticks)"), ("Colours", "Ivory, gray, red, blue, green")],
  features=["Unaffected by atmospheric conditions", "Burns out clean", "Non-sticky to hands and instruments"], tags=["wax", "carving"])
Y("BITE RIM STICK", "material", "pmma-wax", "Pre-fabricated 25 cm wax sticks for occlusion rims, in two sizes; one stick fits two full dentures.", "",
  page=19, img=(19, 3), specs=[("Sizes", "S (short), L (long)"), ("Length", "25 cm"), ("Packing", "50 sticks / box"),
                               ("Colour", "Red, light pink")], tags=["wax", "occlusion rim"])
Y("DIPPING WAX", "material", "pmma-wax", "Coping dipping wax with 65-75 °C melting range that burns out clean (200 g, yellow).", "",
  page=19, img=(19, 6), specs=[("Net weight", "200 g"), ("Colour", "Yellow"), ("Melting range", "65-75 °C"),
                               ("Coping thickness vs temperature", "0.57 / 0.49 / 0.45 mm at 80 / 85 / 90 °C")],
  features=["Optimum elasticity", "Burns out clean", "Minimal shrinkage", "Excellent colour stability after repeat use"], tags=["wax", "dipping"])
Y("PRO UTILITY WAX", "material", "pmma-wax", "Soft or hard red utility wax in long (5 × 280 mm) and short (5 × 140 mm) strips.", "",
  page=19, img=(19, 9), specs=[("Sizes", "Long 5 × 280 mm; short 5 × 140 mm"), ("Hardness", "Soft / hard"), ("Colour", "Red"),
                               ("Packing", "125 g / box")], tags=["wax", "utility"])
Y("KOLBEN WAX", "material", "pmma-wax", "Red base-margin forming line wax (ø2.2 × 200 mm), 500 pieces per box.", "",
  page=19, img=(19, 7), specs=[("Size", "ø2.2 × 200 mm"), ("Packing", "500 pcs / box"), ("Colour", "Red")],
  features=["Time-saving base margin and shape moulding", "Easy to use"], tags=["wax"])
Y("BITE WAX PRE-CUT TYPE", "material", "pmma-wax", "Pre-cut hard bite wax sheets (137 × 73 mm) for occlusion registration.", "",
  page=19, img=(19, 8), specs=[("Sheet size", "137 × 73 mm"), ("Pre-cut strip", "15 × 73 mm"), ("Packing", "500 g / box")],
  tags=["wax", "bite"])
Y("PRO LINE WAX", "material", "pmma-wax", "Pre-fabricated casting-line waxes for sprues, clasps, palatal and lingual bars (YR, YH, YP, YL).",
  "Recommended for casting alloys for bases, clasps and sprue lines; elastic and weldable with a smooth, glossy surface that lets metal flow easily.",
  page=20, img=(20, 0), specs=[("Sprue / retention lines (YR)", "0.5-6.0 mm"), ("Clasps (YH)", "1.4-2.8 mm"),
                               ("Palatal bars (YP I, II)", "4.0 × 1.0 / 1.5 mm"), ("Lingual bars (YL I, II)", "3.1 × 1.4 / 3.5 × 2.0 mm")],
  tags=["wax", "casting"])

Y("SILICONE BIG", "material", "tools-finishing", "Silicone polishing points in coarse, medium and fine grades; max 15,000 rpm.", "",
  page=23, img=(23, 0), specs=[("Size", "23 × 9.5 mm"), ("Working speed", "Max. 15,000 rpm"), ("Packing", "10 / 100 pcs per box"),
                               ("Grades", "Coarse (C-2, C-3), medium (M-1 to M-3), fine (F-2, F-3)")], tags=["polisher", "silicone"])
Y("NEW SILICONE POINTS II", "material", "tools-finishing", "Medium-texture silicone intermediate polishers for metal alloys, palladium alloys and acrylic.", "",
  page=23, img=(23, 8), specs=[("Working speed", "Max. 30,000 rpm (#162: 15,000 rpm)"), ("Packing", "12 / 72 pcs per box"),
                               ("Shapes", "#10 #13 #13S #28 #114 #162, cup, cylinder")], tags=["polisher", "silicone"])
Y("MANDREL CYLINDERS", "material", "tools-finishing", "Handpiece mandrels for New Silicone Point II and cylinder-type polishers (12 per pack).", "",
  page=23, img=(23, 9), specs=[("Packing", "12 pcs / pack")], tags=["mandrel"])
Y("URETHANE BIG", "material", "tools-finishing", "Urethane polishing points for soft linings, mouthguards, splints, nylon, acrylic and metals; max 15,000 rpm.", "",
  page=23, img=(23, 13), specs=[("Size", "24.5 × 9.5 mm"), ("Working speed", "Max. 15,000 rpm"), ("Packing", "10 pcs / box")],
  tags=["polisher", "urethane"])
Y("URETHANE DISK", "material", "tools-finishing", "Urethane polishing wheels (22 × 3.2 mm) in blue #100 coarse and green #320 medium.", "",
  page=23, img=(23, 14), specs=[("Size", "22 × 3.2 mm"), ("Packing", "20 pcs / box"), ("Working speed", "Max. 15,000 rpm")],
  tags=["polisher", "urethane"])
Y("ART POLISHER", "material", "tools-finishing", "Silicone polishing wheels for cobalt-chrome modifications; hard (blue) and soft (light blue).", "",
  page=23, img=(23, 18), specs=[("Size", "22.0 × 3.2 mm"), ("Working speed", "Max. 20,000 rpm"),
                                ("Types", "Hard / blue: cobalt-chrome; soft / light blue: Au, Ag, Pd alloys")], tags=["polisher", "cobalt-chrome"])
Y("YAMAHACHI CUTTING DISK", "material", "tools-finishing", "Sprue cutting disks for silver, palladium, nickel-chrome and cobalt-chrome alloys; max 15,000 rpm.", "",
  page=23, img=(23, 21), specs=[("Type A", "25 × 0.35 mm, 50 pcs"), ("Type B", "25 × 0.60 mm, 30 pcs"),
                                ("Type C", "38 × 0.60 mm, 50 pcs"), ("Type E (ceramic)", "22 × 0.23 mm, 50 pcs")],
  tags=["cutting disk"])
Y("CREAMY SAND", "material", "tools-finishing", "Creamy polishing sand that gives a brilliant lustre and cuts polishing time by 50% (3 kg × 2).", "",
  page=24, img=(24, 8), specs=[("Packing", "3 kg × 2 / pack")], tags=["polishing", "sand"])
Y("SULFONE SAND", "material", "tools-finishing", "Polishing sand for sulfone and acrylic dentures with excellent lustre (1.5 kg × 2).", "",
  page=24, img=(24, 9), specs=[("Packing", "1.5 kg × 2 / pack")], tags=["polishing", "sand"])
Y("GLASS BEADS", "material", "tools-finishing", "Blasting glass beads: #705 for sandblaster, #733 for pencil blaster (2 kg packs).", "",
  page=24, img=(24, 10), specs=[("#705", "149-250 µm, for sandblaster"), ("#733", "44-88 µm, for pencil blaster"), ("Packing", "2 kg / pack")],
  tags=["blasting"])
Y("MP POWDER", "material", "tools-finishing", "Dust-free polishing powder used with MP BUFF for composite resin and palladium alloys.", "",
  page=24, img=(24, 5), specs=[("Packing", "1 kg / pack; 1 kg × 3 / box; 7 kg / can")], tags=["polishing", "powder"])
Y("MP BUFF", "material", "tools-finishing", "Buff used with MP POWDER after trimming and before final polishing (ø90 × 7 mm).", "",
  page=24, img=(24, 6), specs=[("Size", "ø90 × 7 mm"), ("Packing", "1 pc / pack")], tags=["polishing", "buff"])
Y("TIGER MULTI GOLD", "material", "tools-finishing", "Multi-purpose medium polisher for gold, silver and gold-silver-palladium alloys.", "",
  page=25, specs=[("Uses", "Gold alloy, silver alloy, gold-silver-palladium alloy")], tags=["polishing", "precious metal"])
Y("ARTE SHINE", "material", "tools-finishing", "Final polishing paste (Fine red / Extra-fine blue, 25 g) for zirconia, porcelain, glass ceramic and hybrid resin.", "",
  page=25, specs=[("Types", "Fine (red), extra fine (blue)"), ("Package", "25 g")],
  applications=["Zirconia", "Porcelain", "Glass ceramic", "CAD/CAM", "Hybrid resin", "Hard resin"], tags=["polishing", "paste"])
Y("CERAMIC FIBER POINT", "material", "tools-finishing", "Alumina-fibre polishing points for pit fissures, air bubbles and ceramic shape modification; <20,000 rpm.", "",
  page=23, specs=[("Grades", "Green coarse #140-#180; orange medium #320-#400; red fine #1200-#2000"), ("Dimension", "ø2.35 × 50 mm")],
  tags=["polisher", "alumina"])

_sep = [("CLEAN UP", 21, 0, "Non-heating gold and palladium alloy cleaning liquid (500 mL)."),
        ("TRAY WASH", 21, 1, "Cleaning agent for alginate impression material on trays, corrosion-resistant to aluminium, nickel and chrome-plated trays (liquid)."),
        ("PIPE CLEAN", 21, 2, "Dental drain-pipe cleaner with sterilising and deodorising action (liquid)."),
        ("DOWEL PINS CLEANER", 21, 3, "Powerful solvent for instant glue on dowel pins (300 mL)."),
        ("TRAY CLEANER", 21, 4, "Fast-acting powder cleaner for alginate impression material that also sterilises and deodorises trays (1 kg)."),
        ("BRUSH CLEANER", 21, 6, "Brush cleaner for self-curing resin."),
        ("APOLLON SEP (Normal)", 21, 9, "Denture-base separating agent with sodium alginate solution for flasks and plaster separation (500 mL / 2 L / 18 L)."),
        ("APOLLON SEP (Low Viscosity)", 21, 10, "Low-viscosity denture-base separating agent for easier application, also usable with a spray bottle."),
        ("MIRROR CLEANER", 21, 11, "Rouge-type abrasive cleaning liquid for prosthetic appliances (1000 mL)."),
        ("HAND CLEANER", 21, 12, "Powder hand-wash soap for removing dirt, sand and abrasives after polishing (1 kg)."),
        ("BREAK", 21, 13, "Plaster dissolution agent for gypsum on dentures and cast materials (1 L / 2 L / 18 L)."),
        ("WAX PATTERN CLEANER", 21, 14, "Spray wax-pattern strewing agent that enables smooth investment painting (180 mL)."),
        ("WAX PATTERN CLEANER AQUA", 21, 15, "Ethanol-free spray that lubricates wax and resin patterns and prevents bubbles (spray type)."),
        ("APOLLON VARNISH", 21, 16, "Surfactant-based wax-pattern separating agent in paint form (100 mL).")]
for nm, pg, ix, sm in _sep:
    Y(nm, "material", "lab-supplies", sm, "", page=pg, img=(pg, ix), tags=["cleaning", "separating agent"])

Y("LAB SCOPE S", "equipment", "scanners-imaging", "10× laboratory microscope with flexible arm, 120 mm working distance and optional LED circle light.",
  "Compact microscope for inspecting impressions, margins, castings and finished prostheses.", page=26, img=(26, 18),
  specs=[("Magnification", "10×"), ("Eye lens", "WF 10×; view 20 mm; real view 25 mm"), ("Working distance", "120 mm"),
         ("Mirror body", "Straight type, rotates 360°"), ("Eye width adjustment", "55-75 mm"), ("Base diameter", "148 mm"),
         ("Maximum working height", "400 mm"), ("Flexible arm length", "190 mm"),
         ("Optional lenses", "WF5 (5×) and WF20 (20×); LED circle light 100-240 V")],
  applications=["Inspection of impressions and plaster models", "Margin check after waxing and casting",
                "Final inspection of finished prostheses"], tags=["microscope"])
Y("KUGEL HOOK", "material", "lab-supplies", "Bolt-and-socket attachment that turns a tooth base into a denture hook, preserving the natural tooth.",
  "Male/female attachment for denture mechanical stability; the plastic female part is fixed inside the denture with self-curing resin.",
  page=27, img=(27, 0), specs=[("Male", "1 pc / box, 5 pcs / pack"), ("Female", "1 pc / box (setting film × 2); 5 pcs / pack (× 10)")],
  tags=["attachment"])
Y("GLOSSY COAT COLOR", "material", "coloring-glaze", "Light-curing polymer colouring material for crown surfaces; free tuning by mixing brown and clear.", "",
  page=28, img=(28, 6), specs=[("Packaging", "Clear 8 mL / brown 5 mL"), ("Effective wavelength", "365-410 nm"),
                               ("Curing time", "About 3 min in LED CURE BOX PLUS / LED TRAY CURE")], tags=["glaze", "light-curing"])
Y("GLOSSY COAT", "material", "coloring-glaze", "Photo-polymerizable surface glazing resin with stain and abrasion resistance (8 mL).", "",
  page=28, img=(28, 3), specs=[("Package", "8 mL"), ("Effective wavelength", "365-410 nm"),
                               ("Curing time", "About 3 min in LED CURE BOX PLUS / LED TRAY CURE")], tags=["glaze", "light-curing"])
Y("METAL LOCK", "material", "lab-supplies", "Adhesive for bonding metal to resin on facing crowns and dentures (Co-Cr, Au-Ag-Pd, Au, Ti, Ni-Cr); 15 mL.", "",
  page=28, img=(28, 8), specs=[("Package", "15 mL"), ("Applicable metals", "Co-Cr, Au-Ag-Pd, Au, Ti, Ni-Cr")],
  applications=["Metal-to-resin adhesion for facing crowns", "Metal-to-denture-resin adhesion"], tags=["adhesive"])

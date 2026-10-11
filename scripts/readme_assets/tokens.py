"""Design tokens from the caru.moe Figma file (Foundations page)."""

# Colours come from ichika's eyes. Text sits only on pale surfaces or white;
# the vivid colours are reserved for shapes.
SURFACE, RULE = "#FBFCFF", "#C3D4E0"
INK, INK2 = "#0E2336", "#3A536B"
IRIS, IRIS_TINT = "#176297", "#DAECFD"
CYAN, CYAN_INK, CYAN_TINT = "#1BE5EE", "#06707E", "#CBF6FB"
MINT, MINT_TINT = "#5BDFB7", "#D0F7E8"
LILAC, LILAC_TINT = "#C8A5F0", "#EFE4FD"
R_HERO, R_PANEL, R_INSET = 32, 28, 16

# README column on the profile page is ~900px wide, so assets are drawn 1:1.
W = 900

FONT_URLS = {
    "figtree": "https://raw.githubusercontent.com/google/fonts/main/ofl/figtree/Figtree%5Bwght%5D.ttf",
    "mplus2": "https://raw.githubusercontent.com/google/fonts/main/ofl/mplus2/MPLUS2%5Bwght%5D.ttf",
}

# Section marks (Figma "Shape", 100x100): pentagon=Projects, square=Skills,
# circle=History, triangle=Blog. In the logo: C=circle A=triangle R=pentagon U=square.
_PENTAGON = (
    "M46.586 12.3623C48.6401 10.941 51.3599 10.941 53.4141 12.3623L86.2158 35.0593"
    "C88.4219 36.5859 89.3466 39.3915 88.4803 41.9307L76.073 78.298C75.2441 80.7276 "
    "72.9615 82.3607 70.3944 82.3607H29.6056C27.0385 82.3607 24.7559 80.7276 23.927 "
    "78.298L11.5197 41.9307C10.6534 39.3915 11.5781 36.5859 13.7842 35.0593L46.586 12.3623Z"
)
_TRIANGLE = (
    "M60.428 12.6469L94.9756 73.5168C97.0826 77.2294 97.0575 81.7801 94.9102 85.4687"
    "C92.7618 89.1572 88.816 91.4255 84.5486 91.4255H15.4514C11.184 91.4255 7.23821 "
    "89.1572 5.08982 85.4687C2.94252 81.7801 2.91745 77.2294 5.02442 73.5168L39.572 "
    "12.6469C41.7029 8.894 45.6847 6.57448 50 6.57448C54.3153 6.57448 58.2971 8.894 60.428 12.6469Z"
)
# kind -> (svg body in a 100x100 box, section tint)
SHAPES = {
    "pentagon": (f'<path d="{_PENTAGON}" fill="{IRIS}"/>', IRIS_TINT),
    "square": (f'<rect x="10" y="10" width="80" height="80" rx="16" fill="{MINT}"/>', MINT_TINT),
    "circle": (f'<circle cx="50" cy="50" r="44" fill="{CYAN}"/>', CYAN_TINT),
    "triangle": (f'<path d="{_TRIANGLE}" fill="{LILAC}"/>', LILAC_TINT),
}

# Jacket colours rotate through the eye colours in item-number order.
JACKET_COLOURS = ("iris", "mint", "cyan", "lilac")

"""What the README shows. Edit this, then run `uv run scripts/build_assets.py`."""

USER = "caru-ini"
FEED_URL = "https://caru.moe/blog/feed.json"

HERO = {
    "name": "Caru",
    "role": "Student / Web engineer",
    "intro": (
        "Aspiring engineer studying at INIAD, Toyo University (class of 2028). "
        "I love building for the web and have been programming since junior high school."
    ),
}

# (file stem, label, icon in scripts/logos, primary?)
BUTTONS = [
    ("btn-portfolio", "caru.moe", "icon-globe", True),
    ("btn-runa", "Runa.dev", "runa", False),
    ("btn-blog", "Blog", "icon-filetext", False),
    ("btn-zenn", "Zenn", "zenn", False),
]

# (file stem, label, icon)
FOOTER_LINKS = [
    ("link-github", "GitHub", "github"),
    ("link-x", "X", "x"),
    ("link-discord", "Discord", "discord"),
    ("link-mail", "Mail", "icon-envelope"),
]

AWARDS = {
    "award-giiku-2024-vol18": "技育CAMP Hackathon 2024 Vol.18 · Effort Award",
    "award-giiku-2025-vol1": "技育CAMP Hackathon 2025 Vol.1 · Excellence Award",
    "award-giikuhaku-2025-vol2": "技育博 2025 Vol.2 · DeNA Award · CARTA Award",
}

# Repos that get a StarChip (stars-<repo>.svg).
STAR_REPOS = [
    "frourios/magnito",
    f"{USER}/discord-bot-template",
    f"{USER}/modal-comfyui",
    f"{USER}/novelai-sdk",
    f"{USER}/next-authjs-template",
]

# (file stem, title, description, mark)
BANDS = [
    (
        "band-projects", "Projects",
        "Hackathon winners, templates, SDKs and OSS contributions, grouped by who I built them with.", "pentagon",
    ),
    ("band-skills", "Skills", "Languages and tools I use at work and on side projects, rated on a three-step scale.", "square"),
]

# (level, title, description, [(label, icon), ...])
LEVELS = [
    (
        3,
        "Work-ready",
        "Used in real work, such as internships.",
        [
            ("TypeScript", "typescript"), ("Next.js", "nextjs"), ("React", "react"), ("Prisma", "prisma"),
            ("Tailwind CSS", "tailwindcss"), ("Python", "python"), ("Docker", "docker"),
            ("Cloudflare Workers", "cloudflare-workers"), ("Claude Code", "claude"), ("Codex", "openai"),
            ("Orca", "orca"),
        ],
    ),
    (
        2,
        "Side-project ready",
        "Can ship working things in side projects and hackathons.",
        [
            ("Auth.js", "authjs"), ("Better Auth", "betterauth"), ("shadcn/ui", "shadcnui"), ("Hono", "hono"),
            ("Fastify", "fastify"), ("Frourio", "frourio"), ("FastAPI", "fastapi"), ("Pydantic", "pydantic"),
            ("PostgreSQL", "postgresql"), ("Drizzle ORM", "drizzle"), ("OpenAI API", "openai"), ("Git", "git"),
            ("pnpm workspace", "pnpm"), ("Turborepo", "turborepo"), ("Cloudflare D1", "cloudflare"),
            ("Modal", "modal"),
        ],
    ),
    (
        1,
        "Have tried",
        "Touched in tutorials, small experiments, or with heavy AI assistance.",
        [("GCP", "gcp"), ("Ruby on Rails", "rails")],
    ),
]

# Newest first; the History panel shows the top three.
HISTORY = [
    ("2026.9", "MIXI, Inc. — Dive into MIXI internship"),
    ("2026.7", "DMM.com LLC — DMM_Core internship"),
    ("2026.3", "Alaia Inc. — internship"),
]

HISTORY_DESC = "Awards and internships, in order since I started programming at 14."
BLOG_DESC = "Notes on things I tripped over while building, and tools that turned out to be worth it."

# Design Notes: Paranthaman V — Portfolio Theme Extraction

Extracted directly from [Paranthaman V's Portfolio](https://portfolio-app-two-ashen.vercel.app/) and `style.css`.

---

## 1. Color Palette

### Light Mode (Portfolio Native Palette)
| Token / Name | Hex Code | Usage |
|:---|:---:|:---|
| `--cream` | `#F6ECD9` | Primary background color (warm paper / cream) |
| `--cream-alt` | `#EEE0C8` | Alternative surface, badge hover, secondary background |
| `--cream-dark` | `#E3D0B2` | Borders, subtle dividers, horizontal rules |
| `--cream-card` | `#FDF6EC` | Card and container background surface |
| `--brown-dark` | `#1A0F08` | Primary headings, brand titles, high contrast text |
| `--brown-mid` | `#3D2B1F` | Body copy, paragraph text |
| `--brown-light` | `#7A6A5A` | Secondary text, subtitles, meta text |
| `--brown-muted` | `#A89380` | Muted captions, tag borders, subtle icons |
| `--pink` (Primary Accent) | `#E91E8C` | Hot pink accent: "PV." logo, primary buttons, highlights |
| `--pink-light` | `rgba(233, 30, 140, 0.10)` | Translucent pink chip and pill badge background |
| `--pink-mid` | `rgba(233, 30, 140, 0.22)` | Translucent pink borders and hover glows |
| `--indigo` | `#4F46E5` | Secondary accent badge (Node.js, full-stack tags) |
| `--teal` | `#0D9488` | Secondary accent badge (Render, cloud tags) |
| `--orange` | `#F97316` | Accent badge (Git, alerts) |
| `--yellow` | `#F5E03E` | Warm yellow highlight / badge background |

### Dark Mode (Harmonized Warm Obsidian Palette)
Designed to complement GitHub Dark (`#0D1117`) while preserving the portfolio's warm espresso and hot pink DNA:
| Token / Name | Hex Code | Usage |
|:---|:---:|:---|
| Canvas Background | `#120D0A` / `#0D1117` | Dark mode background with subtle warm espresso undertones |
| Surface / Card | `#1C1510` / `#161B22` | Card surface container |
| Border / Rule | `#3D2B1F` / `#30363D` | Borders, subtle dividers |
| Primary Accent | `#E91E8C` / `#FF2A9D` | Vibrant hot pink branding and active indicators |
| Primary Text | `#F6ECD9` | Warm cream heading text |
| Body Text | `#E3D0B2` | Readable warm cream/beige text |
| Muted Text | `#A89380` | Muted captions, borders, metadata |

---

## 2. Typography & Heading Style

- **Heading Font**: `Montserrat`, sans-serif (Weights: 600, 700, 800, 900)
  - Letter-spacing: `-0.02em`
  - Style: Bold, tight letter spacing, high visual authority, modern editorial finish.
- **Body Font**: `Open Sans`, sans-serif (Weights: 400, 500, 600)
  - Line-height: `1.7`
  - Clean, accessible, highly readable across all viewports.
- **Heading Elements**:
  - `h1`: 900 weight, `#1A0F08` (light) / `#F6ECD9` (dark) with `#E91E8C` accents
  - `h2`: 900 weight, centered section titles with subtle underlines / badges
  - `h3`: 700 weight, crisp category and project titles

---

## 3. Visual Tone & Logo Treatment

- **Visual Tone**:
  - Warm editorial chic with retro-modern brutalist elements.
  - Replaces sterile cold neon blues/purples with a warm cream/espresso base energized by vivid hot pink (`#E91E8C`).
  - Tactile card surfaces, rounded pill badges, crisp clean borders, and generous whitespace.
- **Logo Treatment**:
  - Text: **`PV.`**
  - Font: `Montserrat`, 900 Ultra-Bold
  - Color: `#E91E8C` (Hot Pink)
  - Tracking: `-0.02em`

---

## 4. Section Structure & Naming

From portfolio navigation:
1. **Home** (Hero banner, typing role rotation, quick badges, social CTAs)
2. **About** ("Building the future, one endpoint at a time.")
3. **Skills** (Frontend, Backend, Tools & Platform)
4. **Projects** (Featured cards: ConnectHub, Nxt Trendz, Repo Scout)
5. **Experience & Certifications** (Certifications, Current Status, Achievements)
6. **Get In Touch** (Contact, email, LinkedIn, internship availability)

---

## 5. Taglines & Brand Copy

- **Primary Tagline**: *"Turning Ideas into Scalable Web Applications"*
- **Secondary Motto**: *"Building the future, one endpoint at a time."*
- **Role Targets**: Full-Stack Developer · Frontend Developer · Backend Developer


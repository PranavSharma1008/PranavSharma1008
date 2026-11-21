# Project Memory: PranavSharma1008 (GitHub Profile README)

## 1. Project Overview
- **Owner**: Pranav Sharma
- **Repository**: `PranavSharma1008/PranavSharma1008` (Special GitHub profile repository)
- **Role Alignment**: Dedicated **Full Stack Engineer / Full Stack Developer** with a strong foundation in Computer Science & DSA.
- **Purpose**: Showcase full-stack engineering competencies, end-to-end web architectures, DSA problem-solving, and contact channels.

## 2. Tech Stack & Tools
- **Core Focus**: Full Stack Engineering & Systems (React, Node.js, Express, MongoDB, MySQL, TypeScript, Tailwind CSS, Python/Java).
- **Markdown / HTML**: GitHub Flavored Markdown (GFM) with aligned HTML elements.
- **Badges**: Shields.io custom styled badges.
- **Dynamic Assets**: GitHub Readme Typing SVG, Contribution Snake Animation (`assets/github-contribution-grid-snake-dark.svg`), Dynamic LeetCode Profile Statistics Card (`assets/leetcode-stats.svg`).
- **Asset Delivery**: Native raw asset URLs for GitHub rendering; jsDelivr CDN (`cdn.jsdelivr.net`) used for serving PDF files with native `application/pdf` headers.
- **Automation / CI/CD**:
  - `.github/workflows/snake.yml`: automates regular contribution snake graph updates.
  - `.github/workflows/leetcode-sync.yml`: automates dynamic LeetCode stats sync every 6 hours via `scripts/generate_leetcode_card.py`.

## 3. Architecture & Section Layout
1. **Header Banner**: Dynamic machine animation banner (`https://raw.githubusercontent.com/PranavSharma1008/PranavSharma1008/main/assets/machine.gif`).
2. **Typing Intro & Status Badges**: Profile views, Open To Work, Full Stack & DSA badges.
3. **Connect & Platforms**: Portfolio, Resume (`Resume | Print PDF`), LinkedIn, GitHub, LeetCode, GFG, YouTube, Instagram, Monkeytype, Email.
4. **About Me**:
   - Class-based JavaScript representation (`class Developer`) focused on Full Stack engineering (`name`, `role: Full Stack Developer`, `status`, `location`, `focus: Full Stack`) and `philosophy()`.
   - Right-aligned animated coffee/desk GIF expanded to `width="420"` side-by-side with code block and `<br clear="right"/>`.
   - Core engineering highlights and bullet points.
5. **Tech Stack & Engineering Competencies**: Languages, Frontend, Backend & DB, DevOps & Cloud, Core CS.
6. **Featured Projects**: FlashDrop, RecalLC, LeetComete, CampusFix, BloodOcean, Crop Diagnostics.
7. **Contribution Graph**:
   - Dynamic Snake Animation (`assets/github-contribution-grid-snake-dark.svg` and `assets/github-contribution-grid-snake.svg`).
   - Automated via `.github/workflows/snake.yml`.
8. **LeetCode Statistics Card**:
   - Dynamic SVG card (`assets/leetcode-stats.svg`) embedded directly below the contribution snake animation.
   - Clickable image linked to `https://leetcode.com/u/SharmaPranav1008/`.
   - Exact replica of the official LeetCode profile widget: 270° multi-colored circular gauge (316/4114 Solved, green checkmark Solved, 9 Attempting) and 3 pill cards (Easy 201/976, Med. 109/2148, Hard 6/990).
   - Automatically updated every 6 hours via GitHub Actions (`.github/workflows/leetcode-sync.yml`).
9. **Footer**:
   - Contact action buttons and Full Stack Engineer hiring pitch.
   - Get In Touch / Hire Me, View Resume (PDF), Web Portfolio, Connect on LinkedIn, Connect on Instagram.

## 4. Important Decisions
- **Full Stack Alignment**: Profile is tailored for Full Stack Engineering roles across banners, badges, About Me class, and footer.
- **Color Palette & Eye Comfort**: Removed high-glare neon green (`#00FF9D`) badges and the waving footer bar. Transitioned badges to soothing, professional brand tones (Gmail Red `#EA4335`, Google Blue `#4285F4`, and Teal `#00C7B7`) for comfortable dark mode reading without eye strain.
- **Visual Section Sequence**: Contribution Graph Snake Animation is followed directly by the LeetCode stats card, which in turn leads into the Frontend Engineer hiring footer.
- **Official LeetCode Card Replica**: Generated via Python script querying LeetCode's public GraphQL API for matched user submission and question progress stats. Completely self-hosted SVG within the repository to eliminate third-party downtime and rate limits.
- **Clickable Profiles**: LeetCode card opens user's profile `https://leetcode.com/u/SharmaPranav1008/` in a new browser tab.

## 5. Completed Tasks
- Expanded coffee animation GIF width to `420px`.
- Removed `typing_speed`, `youtube_channel`, and `instagram` from `class Developer`.
- Changed `focus` to `"Full Stack"` and updated `role` to `"Full Stack Developer"`.
- Aligned entire README (typing SVG, badges, bullet points, footer) to Full Stack Engineering.
- Added live Chrome Web Store buttons/links for **RecalLC** and **LeetComete** featured projects.
- Restored Contribution Snake Animation in README.md.
- Built `scripts/generate_leetcode_card.py` querying LeetCode GraphQL API to generate pixel-accurate `assets/leetcode-stats.svg`.
- Created GitHub Actions workflow `.github/workflows/leetcode-sync.yml` to automatically refresh stats every 6 hours.
- Integrated LeetCode card in `README.md` after Snake Animation and before the footer pitch, linked to `https://leetcode.com/u/SharmaPranav1008/`.
- Halved the speed of the contribution snake animation (doubled duration from 74.5s to 149s) across dark and light SVG assets and automated in `.github/workflows/snake.yml`.
- Removed nested SVG anchor wrapper in `assets/leetcode-stats.svg` to prevent browser click event swallowing and ensure seamless profile navigation.

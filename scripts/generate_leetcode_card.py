#!/usr/bin/env python3
import json
import math
import os
import ssl
import sys
import urllib.request

USERNAME = "SharmaPranav1008"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_SVG = os.path.join(REPO_ROOT, "assets", "leetcode-stats.svg")

def fetch_leetcode_stats(username):
    url = "https://leetcode.com/graphql"
    ctx = ssl._create_unverified_context()

    query1 = {
        "query": """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """,
        "variables": {"username": username}
    }

    query2 = {
        "query": """
        query userProfileUserQuestionProgressV2($userSlug: String!) {
            userProfileUserQuestionProgressV2(userSlug: $userSlug) {
                numFailedQuestions {
                    count
                    difficulty
                }
            }
        }
        """,
        "variables": {"userSlug": username}
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://leetcode.com/u/{username}/"
    }

    try:
        req1 = urllib.request.Request(url, data=json.dumps(query1).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req1, context=ctx, timeout=10) as resp:
            data1 = json.loads(resp.read().decode('utf-8'))

        req2 = urllib.request.Request(url, data=json.dumps(query2).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req2, context=ctx, timeout=10) as resp:
            data2 = json.loads(resp.read().decode('utf-8'))

        all_q = {q['difficulty']: q['count'] for q in data1['data']['allQuestionsCount']}
        ac_subs = {s['difficulty']: s['count'] for s in data1['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum']}

        failed_q = 0
        try:
            failed_list = data2['data']['userProfileUserQuestionProgressV2']['numFailedQuestions']
            failed_q = sum(item['count'] for item in failed_list)
        except Exception:
            failed_q = 9  # Fallback

        return {
            "all_total": all_q.get("All", 4114),
            "all_solved": ac_subs.get("All", 316),
            "easy_total": all_q.get("Easy", 976),
            "easy_solved": ac_subs.get("Easy", 201),
            "med_total": all_q.get("Medium", 2148),
            "med_solved": ac_subs.get("Medium", 109),
            "hard_total": all_q.get("Hard", 990),
            "hard_solved": ac_subs.get("Hard", 6),
            "attempting": failed_q
        }
    except Exception as e:
        print(f"Error fetching from LeetCode API: {e}", file=sys.stderr)
        return {
            "all_total": 4114,
            "all_solved": 316,
            "easy_total": 976,
            "easy_solved": 201,
            "med_total": 2148,
            "med_solved": 109,
            "hard_total": 990,
            "hard_solved": 6,
            "attempting": 9
        }

def describe_arc(cx, cy, r, start_angle, end_angle):
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    x1 = cx + r * math.cos(start_rad)
    y1 = cy + r * math.sin(start_rad)
    x2 = cx + r * math.cos(end_rad)
    y2 = cy + r * math.sin(end_rad)

    delta = (end_angle - start_angle) % 360
    large_arc = 1 if delta > 180 else 0
    sweep = 1

    return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} {sweep} {x2:.2f} {y2:.2f}"

def generate_svg(stats):
    cx = 274.5
    cy = 168.5
    r = 135
    total_q = stats["all_total"]

    # Arc spans from 135 deg to 45 deg clockwise (270 degrees total)
    start_deg = 135.0
    total_arc = 270.0

    easy_span = (stats["easy_total"] / total_q) * total_arc
    med_span = (stats["med_total"] / total_q) * total_arc
    hard_span = (stats["hard_total"] / total_q) * total_arc

    easy_start = start_deg
    easy_end = easy_start + easy_span

    med_start = easy_end
    med_end = med_start + med_span

    hard_start = med_end
    hard_end = hard_start + hard_span

    # Solved spans
    easy_solved_span = (stats["easy_solved"] / stats["easy_total"]) * easy_span if stats["easy_total"] else 0
    med_solved_span = (stats["med_solved"] / stats["med_total"]) * med_span if stats["med_total"] else 0
    hard_solved_span = (stats["hard_solved"] / stats["hard_total"]) * hard_span if stats["hard_total"] else 0

    track_easy = describe_arc(cx, cy, r, easy_start, easy_end)
    track_med = describe_arc(cx, cy, r, med_start, med_end)
    track_hard = describe_arc(cx, cy, r, hard_start, hard_end)

    solved_easy = describe_arc(cx, cy, r, easy_start, easy_start + max(easy_solved_span, 0.1))
    solved_med = describe_arc(cx, cy, r, med_start, med_start + max(med_solved_span, 0.1))

    # Dot coordinates for hard solved
    hard_rad = math.radians(hard_start)
    hard_dot_x = cx + r * math.cos(hard_rad)
    hard_dot_y = cy + r * math.sin(hard_rad)

    svg = f"""<svg width="714" height="326" viewBox="0 0 714 326" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .card-bg {{
      fill: #282828;
    }}
    .pill-bg {{
      fill: #353535;
    }}
    .text-title {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 600;
      font-size: 19px;
      text-anchor: middle;
      dominant-baseline: central;
    }}
    .text-ratio {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 700;
      font-size: 21px;
      fill: #FFFFFF;
      text-anchor: middle;
      dominant-baseline: central;
    }}
    .center-total {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 700;
      font-size: 52px;
      fill: #FFFFFF;
      text-anchor: end;
      dominant-baseline: central;
    }}
    .center-max {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 500;
      font-size: 32px;
      fill: #8A8A8A;
      text-anchor: start;
      dominant-baseline: central;
    }}
    .center-solved {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 600;
      font-size: 22px;
      fill: #FFFFFF;
      dominant-baseline: central;
    }}
    .center-attempting {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-weight: 500;
      font-size: 20px;
      fill: #8A8A8A;
      text-anchor: middle;
      dominant-baseline: central;
    }}
  </style>

  <a href="https://leetcode.com/u/{USERNAME}/" target="_blank" rel="noopener noreferrer">
    <!-- Card Container -->
    <rect width="714" height="326" rx="16" class="card-bg" />

    <!-- Circular Gauge Background Tracks -->
    <path d="{track_easy}" stroke="#3c504a" stroke-width="11" stroke-linecap="round" />
    <path d="{track_med}" stroke="#51452d" stroke-width="11" stroke-linecap="round" />
    <path d="{track_hard}" stroke="#4d2f2d" stroke-width="11" stroke-linecap="round" />

    <!-- Circular Gauge Active Solved Highlights -->
    <path d="{solved_easy}" stroke="#58b8b9" stroke-width="11" stroke-linecap="round" />
    <path d="{solved_med}" stroke="#f4ba40" stroke-width="11" stroke-linecap="round" />
    <circle cx="{hard_dot_x:.2f}" cy="{hard_dot_y:.2f}" r="5.5" fill="#e24a41" />

    <!-- Center Gauge Numbers -->
    <g transform="translate(0, 0)">
      <text x="256" y="145" class="center-total">{stats['all_solved']}</text>
      <text x="256" y="151" class="center-max">/{stats['all_total']}</text>
      
      <!-- Checkmark + Solved centered as a group -->
      <g transform="translate(226, 192)">
        <path d="M 0 0 L 6 6 L 16 -6" stroke="#2cbb5d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" />
        <text x="24" y="0" class="center-solved">Solved</text>
      </g>

      <!-- Attempting count -->
      <text x="274.5" y="242" class="center-attempting">{stats['attempting']} Attempting</text>
    </g>

    <!-- Right Difficulty Pill Cards -->
    <!-- Easy Pill -->
    <g transform="translate(531, 33)">
      <rect width="161" height="78" rx="10" class="pill-bg" />
      <text x="80.5" y="27" class="text-title" fill="#58b8b9">Easy</text>
      <text x="80.5" y="56" class="text-ratio">{stats['easy_solved']}/{stats['easy_total']}</text>
    </g>

    <!-- Medium Pill -->
    <g transform="translate(531, 127)">
      <rect width="161" height="78" rx="10" class="pill-bg" />
      <text x="80.5" y="27" class="text-title" fill="#f4ba40">Med.</text>
      <text x="80.5" y="56" class="text-ratio">{stats['med_solved']}/{stats['med_total']}</text>
    </g>

    <!-- Hard Pill -->
    <g transform="translate(531, 221)">
      <rect width="161" height="78" rx="10" class="pill-bg" />
      <text x="80.5" y="27" class="text-title" fill="#e24a41">Hard</text>
      <text x="80.5" y="56" class="text-ratio">{stats['hard_solved']}/{stats['hard_total']}</text>
    </g>
  </a>
</svg>
"""
    return svg

def main():
    print(f"Fetching LeetCode stats for {USERNAME}...")
    stats = fetch_leetcode_stats(USERNAME)
    print(f"Fetched stats: {stats}")

    os.makedirs(os.path.dirname(OUTPUT_SVG), exist_ok=True)
    svg_content = generate_svg(stats)

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_SVG}")

if __name__ == "__main__":
    main()

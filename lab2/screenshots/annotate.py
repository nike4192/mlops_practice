"""Аннотация скриншотов lab2 — рисует красные рамки + подписи.

Запуск:
    python annotate.py

Координаты подобраны по brightness-scan и визуальной разметке для
скринов 1920x1080. Сохраняет файлы под именами SHOTLIST.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
RED = (220, 38, 38, 255)
RED_FILL = (220, 38, 38, 235)
WHITE = (255, 255, 255, 255)
BORDER = 6


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_rect(draw, w, h, box_pct, thickness=BORDER):
    x1, y1, x2, y2 = box_pct
    draw.rectangle((int(w * x1), int(h * y1), int(w * x2), int(h * y2)),
                   outline=RED, width=thickness)


def draw_caption(draw, w, h, text):
    f = font(28)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 24, 14
    bar_x0 = (w - tw - pad_x * 2) // 2
    bar_y0 = h - th - pad_y * 2 - 24
    bar_x1 = bar_x0 + tw + pad_x * 2
    bar_y1 = bar_y0 + th + pad_y * 2
    draw.rounded_rectangle((bar_x0, bar_y0, bar_x1, bar_y1), radius=12, fill=RED_FILL)
    draw.text((bar_x0 + pad_x, bar_y0 + pad_y - bbox[1]), text, fill=WHITE, font=f)


def annotate(src, dst, *, rects=(), caption=""):
    img = Image.open(ROOT / src).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for r in rects:
        draw_rect(draw, w, h, r)
    if caption:
        draw_caption(draw, w, h, caption)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(ROOT / dst, "PNG", optimize=True)
    print(f"  ✓ {dst}")


# Все скрины 1920x1080. Координаты в долях [0..1].
SCREENS = [
    dict(
        src="Screenshot from 2026-04-28 18-55-01.png",
        dst="01-gitlab-login-page.png",
        rects=[
            (0.378, 0.485, 0.620, 0.535),   # Username field "root"
            (0.378, 0.525, 0.620, 0.575),   # Password field "ChangeMe-2026!"
        ],
        caption="Вход root / ChangeMe-2026!",
    ),
    dict(
        src="Screenshot from 2026-04-28 18-56-49.png",
        dst="02-gitlab-main-page.png",
        rects=[
            (0.000, 0.085, 0.130, 0.420),   # left menu
            (0.926, 0.045, 0.985, 0.085),   # admin avatar top right
        ],
        caption="Вход выполнен — учётка root",
    ),
    dict(
        src="Screenshot from 2026-04-28 18-59-26.png",
        dst="03-new-project-form.png",
        rects=[
            (0.295, 0.300, 0.785, 0.350),   # Project name input "lab2-mlops"
            (0.293, 0.625, 0.500, 0.665),   # Initialize repository checkbox row
        ],
        caption="lab2-mlops · Private · без Initialize README",
    ),
    dict(
        src="Screenshot from 2026-04-28 18-59-41.png",
        dst="04-empty-project-page.png",
        rects=[
            (0.157, 0.190, 0.500, 0.250),   # Project header "lab2-mlops"
        ],
        caption="Проект создан — репозиторий пустой, командные инструкции ниже",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-08-19.png",
        dst="05-settings-cicd-runners.png",
        rects=[
            (0.760, 0.471, 0.918, 0.520),   # "Create project runner" button
        ],
        caption="Жми «Create project runner» — генерим токен",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-10-40.png",
        dst="06-runner-token.png",
        rects=[
            (0.135, 0.690, 0.770, 0.770),   # Step 1 command block with token
        ],
        caption="Скопируй токен — он в команде register --token <ТУТ>",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-12-32.png",
        dst="07-runner-online.png",
        rects=[
            (0.155, 0.385, 0.770, 0.460),   # runner row with green online dot
        ],
        caption="Runner подключился — статус online",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-26-40.png",
        dst="09-pipeline-all-green.png",
        rects=[
            (0.225, 0.330, 0.275, 0.395),   # Passed badge
            (0.595, 0.330, 0.660, 0.395),   # 4 green stage circles
        ],
        caption="Pipeline #1 — все 4 stage прошли",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-27-13.png",
        dst="10-test-job-log.png",
        rects=[
            (0.075, 0.530, 0.510, 0.640),   # metrics block (Accuracy/Precision/...)
        ],
        caption="Метрики из model_testing.py в логе job test",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-29-27.png",
        dst="11-artifacts-browse.png",
        rects=[
            (0.220, 0.310, 0.860, 0.460),   # file list with evaluation_report.txt + testing.log
        ],
        caption="Артефакты сохранены — можно скачать",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-32-44.png",
        dst="12-lint-failed-pipeline.png",
        rects=[
            (0.225, 0.330, 0.275, 0.395),   # Failed badge (row #3)
            (0.595, 0.330, 0.660, 0.395),   # red lint + 2 skipped circles
        ],
        caption="Линтер упал → ML-стейджи skipped",
    ),
    dict(
        src="Screenshot from 2026-04-28 19-32-53.png",
        dst="12b-lint-job-log.png",
        rects=[
            (0.075, 0.560, 0.520, 0.760),   # tail of log with ci_lint.py errors
        ],
        caption="Вывод ci_lint.py — отсутствует stage test",
    ),
]


def main():
    for s in SCREENS:
        annotate(**s)
    print("Готово.")


if __name__ == "__main__":
    main()

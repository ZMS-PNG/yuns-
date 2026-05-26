from __future__ import annotations

from pathlib import Path


class PaddleOCRClient:
    """Optional OCR adapter. Keeps OCR separate from scoring business logic."""

    def extract_text(self, image_path: str) -> str:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        try:
            from paddleocr import PaddleOCR  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("paddleocr is not installed. Install paddleocr or pass ocr_context directly.") from exc

        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(str(path), cls=True)
        texts = []
        for page in result or []:
            for line in page or []:
                try:
                    texts.append(line[1][0])
                except Exception:
                    continue
        return "\n".join(texts)

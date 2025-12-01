import os
import argparse

DEFAULT_INPUT_FILE = "input.txt"
DEFAULT_OUTPUT_FILE = "output.txt"


def parse_args() -> argparse.Namespace:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Duplicate Cleaner: удаление дублирующихся строк из текстового файла."
    )
    parser.add_argument(
        "-i",
        "--input",
        default=DEFAULT_INPUT_FILE,
        help=f"Путь к входному файлу (по умолчанию {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Путь к выходному файлу (по умолчанию {DEFAULT_OUTPUT_FILE})",
    )
    return parser.parse_args()


def load_lines(file_path: str) -> list[str]:
    """Загружает строки из файла и очищает лишние пробелы."""
    if not os.path.exists(file_path):
        print(f"[!] Файл {file_path} не найден.")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line]  # удаляем пустые строки


def remove_duplicates(lines: list[str]) -> list[str]:
    """Удаляет дубли, сохраняя порядок."""
    seen = set()
    unique = []

    for line in lines:
        if line not in seen:
            unique.append(line)
            seen.add(line)

    return unique


def save_report_and_data(
    file_path: str, total: int, unique_count: int, removed: int, unique_lines: list[str]
):
    """Сохраняет отчёт и уникальные строки в один файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        # Записываем отчёт
        f.write("=== Отчёт ===\n")
        f.write(f"Всего строк:       {total}\n")
        f.write(f"Уникальных строк:  {unique_count}\n")
        f.write(f"Удалено дублей:    {removed}\n\n")

        # Разделитель
        f.write("--- Уникальные строки ---\n")

        # Сами строки
        for line in unique_lines:
            f.write(line + "\n")


def main():
    print("=== Duplicate Cleaner ===")

    args = parse_args()
    input_path = args.input
    output_path = args.output

    print(f"Входной файл:  {input_path}")
    print(f"Выходной файл: {output_path}")

    lines = load_lines(input_path)
    if not lines:
        print("[!] Нет данных для обработки.")
        return

    total = len(lines)
    unique_lines = remove_duplicates(lines)
    unique_count = len(unique_lines)
    removed_count = total - unique_count

    save_report_and_data(output_path, total, unique_count, removed_count, unique_lines)

    print("\n=== Отчёт ===")
    print(f"Всего строк:       {total}")
    print(f"Уникальных строк:  {unique_count}")
    print(f"Удалено дублей:    {removed_count}")
    print(f"Результат сохранён в: {output_path}")


if __name__ == "__main__":
    main()

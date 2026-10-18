[English](./README.md) · **Українська**

# Проєкт 01: Базовий та мінімальний harness

Порівняйте, як слабкий harness (лише промпт) та явний harness (файли правил і механізми верифікації) впливають на показник виконання завдань агентом AI-кодування.

## Структура каталогів

| Каталог | Призначення |
|------|------|
| `starter/` | **Відправна точка**: лише розмитий `task-prompt.md`, без AGENTS.md і без feature_list.json. Це версія зі «слабким harness», яку передають агенту. |
| `solution/` | **Еталонна реалізація**: той самий код застосунку, але з повними файлами harness (AGENTS.md, feature_list.json, init.sh, claude-progress.md). Це версія з «явним harness». |

## Як використовувати

```sh
# 1. Запустіть завдання агента один раз із starter (слабкий harness)
cd starter
npm install
# Передайте вміст task-prompt.md як промпт до Claude Code / Codex
# Попросіть агента виконати: запуск вікна, список документів, панель QA, каталог даних
# Не надавайте агенту файли solution під час цього запуску.

# 2. Запустіть те саме завдання із solution (явний harness)
cd ../solution
npm install
# Попросіть агента прочитати AGENTS.md, init.sh, feature_list.json і claude-progress.md
# перед тим як торкатися коду. Код продукту вже має задовольняти ті самі чотири функції.

# 3. Порівняйте два результати
# - Чи було виконано завдання?
# - Скільки повторних спроб знадобилося?
# - Чи оголосив агент «готово» занадто рано?
```

## Точний контракт завдання

Стартовий промпт навмисно розмитий (`starter/task-prompt.md` містить лише
«Build an Electron app that can show documents and answer questions.»). Використовуйте
solution harness, щоб зробити цей розмитий запит конкретним:

| Функція | Докази в starter для перевірки | Докази в solution для порівняння |
|------|------|------|
| Запуск вікна | `src/main/main.ts`, `src/preload/preload.ts` | елемент `window-launch` у feature_list.json |
| Панель списку документів | `src/renderer/components/DocumentList.tsx` | елемент `document-list` у feature_list.json |
| Панель запитань | `src/renderer/components/QuestionPanel.tsx` | елемент `question-panel` у feature_list.json |
| Каталог даних | `src/services/persistence-service.ts` | елемент `data-directory` у feature_list.json |

Цей проєкт є експериментом, а не звичайним завданням «заповни starter, поки він не дорівнюватиме
solution». Навчальний результат — це виміряна різниця між запуском лише з промптом
і запуском, що починається з явних правил репозиторію та артефактів верифікації.

## Охоплені функції

- Electron-вікно успішно запускається
- UI відображає область списку документів
- UI відображає панель QA
- Застосунок створює та використовує локальний каталог даних

## Пов'язані лекції

- [Лекція 01: Чому здатні агенти все одно зазнають невдачі](../../docs/en/lectures/lecture-01-why-capable-agents-still-fail/index.md)
- [Лекція 02: Що таке harness насправді](../../docs/en/lectures/lecture-02-what-a-harness-actually-is/index.md)

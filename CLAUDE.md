# CLAUDE.md

Це навчальний репо: я проходжу курс harness engineering. Ти — наставник, а не виконавець за мене.

## Правила
- Спілкуйся українською. Терміни (harness, Definition of Done тощо) лишай англійською з поясненням.
- Оригінальний курс: `../learn-harness-engineering` (лекції в `docs/uk/lectures/`, еталони в `projects/*/solution/`).
  Якщо його немає: `git clone --depth 1 https://github.com/walkinglabs/learn-harness-engineering ../learn-harness-engineering`.
  Не показуй `solution/`, доки я сам не спробував і не попросив.
- На початку сесії читай `PROGRESS.md`; наприкінці — онови його (фаза, що далі, рядок у журналі).
- Конспект кожної лекції — `notes/LNN-<коротка-назва>.md`: 5–10 ключових тез + мої відповіді на вправи.

## Перевірка проєктів
```sh
cd projects/project-NN/starter
npm install
npm run check   # typecheck
npm run test    # vitest
```
Задача не «готова», доки `check` і `test` не зелені.

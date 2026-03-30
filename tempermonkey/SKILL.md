---
name: tampermonkey-script-writer
description: >
  Writes a new Tampermonkey userscript for the Avito internal tools repo and scaffolds all required files.
  Use this skill whenever the user describes a browser automation problem, wants to inject a UI element into
  a web page, wants to copy something to the clipboard from a page, wants to add a button or link to an
  internal Avito tool (Jira, Stash, PaaS, AB platform, TeamRetro), or says anything like "хочу скрипт
  который", "напиши скрипт", "добавь кнопку на страницу", "tampermonkey", "userscript", "внедри в страницу".
  Also use when the user pastes an HTML snippet and asks how to interact with it via a browser script.
---

# Tampermonkey Script Writer

Помогает написать новый Tampermonkey-скрипт для репозитория и создать всю необходимую структуру файлов.

## Рабочий процесс: две фазы

Скилл работает в два этапа, чтобы сэкономить токены: **планирование** делается на текущей (дорогой) модели, **реализация** делегируется субагенту на дешёвой модели `claude-haiku-4-5-20251001`.

---

## Фаза 1 — Планирование (текущая модель)

### Что спросить у пользователя

Если какой-то из этих пунктов не указан в запросе — спроси **одним сообщением**:

1. **Проблема** — что сейчас неудобно или чего не хватает на странице?
2. **Решение** — как должен работать скрипт? Какой UI добавить?
3. **URL страницы** — на каком сайте/паттерне URL должен работать скрипт (например `https://stash.msk.avito.ru/projects/*/repos/*`)?
4. **HTML-фрагмент** — вставь кусок HTML страницы рядом с местом, куда нужно внедриться (достаточно 5-15 строк из DevTools → Inspect).

Если HTML не предоставлен, но URL есть — спроси, какой CSS-селектор или элемент является целевым якорем.

### Что решить в фазе планирования

Получив ответы от пользователя, прими следующие решения:

- **slug** папки (kebab-case, например `stash-my-feature`)
- **`@match`** паттерн
- **`@grant`** — нужен ли `GM.setClipboard`?
- **Нужен ли MutationObserver?** (да, если страница SPA или React)
- **Нужен ли перехват `history.pushState`?** (да, если URL меняется без перезагрузки)
- **Целевой CSS-селектор якоря** — куда вставляем элемент
- **Метод вставки** — `insertAdjacentElement`, `appendChild`, `insertBefore`
- **Нужна ли защита от дублирования** и какая (`id` или `data-атрибут`)

Сформируй компактное **техническое задание** для субагента (см. ниже).

### Формат ТЗ для субагента

```
Напиши Tampermonkey-скрипт и создай все файлы.

slug: {slug}
Название скрипта: {название}
URL-паттерн (@match): {url}
@grant: {none | GM.setClipboard}
Описание: {что делает скрипт}

Архитектура:
- MutationObserver: {да/нет, почему}
- history.pushState перехват: {да/нет}
- Якорный селектор: {CSS-селектор}
- Метод вставки: {insertAdjacentElement('afterend') / appendChild / ...}
- Защита от дублирования: {id="..." / data-атрибут "..."}
- @grant GM.setClipboard: {да/нет}

Логика скрипта:
{описание бизнес-логики — что копировать, какую ссылку строить, что показывать}

Константы для настройки (если есть):
- {КОНСТАНТА}: {описание}

Репозиторий: /Users/iandvolkov/GO/iandvolkov/tampermonkey
Создать файлы:
- {slug}/index.js
- {slug}/README.md (с разделами: описание, Где работает, Скриншоты, Установка, Настройка если нужна)
- {slug}/assets/.gitkeep
Обновить: README.md в корне (добавить строку в таблицу скриптов)

Паттерны кода: следуй инструкциям из SKILL.md по архитектуре (IIFE, MutationObserver, SPA, дублирование, GM.setClipboard).
```

Передай это ТЗ субагенту (фаза 2).

---

## Фаза 2 — Реализация (субагент на дешёвой модели)

Запусти Agent с параметром `model: claude-haiku-4-5-20251001` и передай ему ТЗ из фазы 1 вместе с содержимым этого SKILL.md (чтобы субагент знал паттерны).

Субагент должен:
1. Создать `{slug}/index.js` по шаблонам ниже
2. Создать `{slug}/README.md`
3. Создать `{slug}/assets/.gitkeep`
4. Добавить строку в корневой `README.md`

---

---

## Структура файлов для каждого скрипта

```
{slug}/
  index.js      ← сам скрипт
  README.md     ← описание, скриншоты, установка, настройка
  assets/       ← папка для скриншотов (создаём пустой .gitkeep)
```

Slug — это kebab-case имя скрипта, например `stash-pr-copy-link`.

После создания скрипта добавь строку в таблицу `README.md` в **корне репозитория**.

---

## Шаблон Tampermonkey-заголовка

```js
// ==UserScript==
// @name         {Читаемое название}
// @namespace    {базовый URL сайта}
// @author       {автор}
// @version      1.0
// @description  {Краткое описание на языке автора}
// @match        {URL-паттерн}
// @grant        {none | GM.setClipboard}
// ==/UserScript==
```

- `@grant none` — если буфер обмена не нужен.
- `@grant GM.setClipboard` — если нужно копировать в буфер (`GM.setClipboard(text)`). Не используй `navigator.clipboard`.
- `@namespace` — обычно базовый URL сайта (`https://stash.msk.avito.ru/`).

---

## Архитектурные паттерны (всегда применяй)

### 1. Обёртка IIFE

```js
(function () {
    'use strict';
    // ...
})();
```

### 2. Защита от дублирования

Всегда проверяй, не добавлена ли кнопка/элемент уже:

```js
const BUTTON_ID = 'my-unique-btn-id';
if (document.getElementById(BUTTON_ID)) return;
```

Или через data-атрибут на строках/элементах:

```js
const ATTR = 'data-my-script-done';
if (row.hasAttribute(ATTR)) return;
row.setAttribute(ATTR, '1');
```

### 3. MutationObserver для динамического контента

Используй, если страница рендерится на React/Angular или DOM меняется после загрузки:

```js
const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {
            if (!(node instanceof Element)) continue;
            tryPatch(node);
        }
    }
});
observer.observe(document.body, { childList: true, subtree: true });
```

Для атрибутов (например, модальные окна Ant Design, которые прячутся через `display:none`):

```js
observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['style', 'class'],
});
```

### 4. SPA-навигация (history.pushState)

Используй, если сайт — SPA и URL меняется без перезагрузки страницы:

```js
const originalPushState = history.pushState.bind(history);
history.pushState = function (...args) {
    originalPushState(...args);
    setTimeout(init, 500);
};
window.addEventListener('popstate', () => setTimeout(init, 500));
```

### 5. Ожидание появления элемента (init + observer)

```js
function init() {
    const anchor = document.querySelector('.target-selector');
    if (!anchor) return; // ещё не отрендерилось
    if (document.getElementById(BUTTON_ID)) return; // уже добавили
    insertButton(anchor);
}

function startObserver() {
    const obs = new MutationObserver(() => {
        if (document.querySelector('.target-selector') && !document.getElementById(BUTTON_ID)) {
            init();
        }
    });
    obs.observe(document.body, { childList: true, subtree: true });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { init(); startObserver(); });
} else {
    init();
    startObserver();
}
```

### 6. Кнопка в стиле Stash (AUI)

```js
const li = document.createElement('li');
const a = document.createElement('a');
a.id = BUTTON_ID;
a.href = '#';
a.className = 'aui-nav-item';
a.innerHTML = `<span class="aui-icon aui-icon-small icon-link"></span>
               <span class="aui-nav-item-label">Моя кнопка</span>`;
a.addEventListener('click', (e) => { e.preventDefault(); doSomething(); });
li.appendChild(a);
anchorLi.insertAdjacentElement('afterend', li);
```

### 7. Обычная кнопка (не AUI)

```js
const btn = document.createElement('button');
btn.id = BUTTON_ID;
btn.textContent = 'Нажми меня';
btn.style.cssText = 'padding:6px 14px;font-weight:bold;background:#F7F7F7;border:1px solid #DDD;border-radius:4px;cursor:pointer;font-size:13px;';
btn.addEventListener('click', handleClick);
targetElement.insertAdjacentElement('afterend', btn);
```

Визуальная обратная связь после клика:

```js
btn.textContent = 'Скопировано!';
btn.style.background = '#4CAF50';
setTimeout(() => {
    btn.textContent = 'Скопировать';
    btn.style.background = '#F7F7F7';
}, 1000);
```

### 8. Копирование в буфер

```js
// В заголовке: @grant GM.setClipboard
GM.setClipboard(text);
```

---

## Как читать HTML-фрагмент пользователя

Чтобы понять, куда внедряться:

1. Найди ближайший **стабильный якорь** — элемент с id, уникальным классом или data-атрибутом, который не меняется при SPA-переходах.
2. Используй `insertAdjacentElement('afterend', el)` или `parentNode.insertBefore(el, ref)`.
3. Избегай позиционных селекторов вида `:nth-child(3)` — они хрупкие.
4. Если HTML принадлежит React-компоненту (классы вида `D5KzX` — хэши), используй MutationObserver — элемент может пересоздаваться.

---

## Шаблон README.md для нового скрипта

```markdown
# {Название скрипта}

{Описание в 1-2 предложениях.}

**Где работает:** `{URL-паттерн}`

## Скриншоты

![описание](assets/1.png)

## Установка

1. Установить [Tampermonkey](https://www.tampermonkey.net/)
2. Открыть дашборд Tampermonkey → **+ New script**
3. Скопировать содержимое [`index.js`](index.js) → сохранить (Ctrl+S / Cmd+S)

## Настройка

- `КОНСТАНТА` (строка N): {что изменить — только если есть личные настройки}
```

Раздел **Настройка** добавляй только если в скрипте есть константы, которые пользователь должен менять под себя (имена команд, пути к файлам и т.п.).

---

## Чек-лист перед финальной отдачей

- [ ] Заголовок `==UserScript==` заполнен корректно
- [ ] `@grant` соответствует использованию `GM.setClipboard`
- [ ] Есть защита от дублирования (id или data-атрибут)
- [ ] Если DOM динамический — используется MutationObserver
- [ ] Если SPA — перехвачен `history.pushState` и `popstate`
- [ ] Созданы файлы: `{slug}/index.js`, `{slug}/README.md`, `{slug}/assets/.gitkeep`
- [ ] README.md содержит раздел `## Скриншоты` — он **обязателен**, даже если скриншоты ещё не добавлены (секция остаётся с placeholder-ссылками `assets/1.png`)
- [ ] Добавлена строка в таблицу корневого `README.md`
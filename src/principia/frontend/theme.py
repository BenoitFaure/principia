"""Centralized frontend theme choices."""

from __future__ import annotations

from nicegui import ui

_THEME_CSS = """
:root {
  --principia-bg: #e5f5e8;
  --principia-pane: #effaf1;
  --principia-pane-muted: #d7eddb;
  --principia-text: #123d1f;
  --principia-border: #7dbb85;
  --principia-border-strong: #3d7d49;
  --principia-control: #ffffff;
  --principia-control-hover: #d7efdc;
  --principia-shadow: 0 18px 50px rgba(24, 81, 38, 0.12);
  --principia-separator-gap: 6vh;
  --principia-pane-radius: 24px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --principia-bg: #06190d;
    --principia-pane: #0b2414;
    --principia-pane-muted: #10301b;
    --principia-text: #d7f5dc;
    --principia-border: #346a3f;
    --principia-border-strong: #7fd28d;
    --principia-control: #13301d;
    --principia-control-hover: #1b4529;
    --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
  }
}

body.body--light {
  --principia-bg: #e5f5e8;
  --principia-pane: #effaf1;
  --principia-pane-muted: #d7eddb;
  --principia-text: #123d1f;
  --principia-border: #7dbb85;
  --principia-border-strong: #3d7d49;
  --principia-control: #ffffff;
  --principia-control-hover: #d7efdc;
  --principia-shadow: 0 18px 50px rgba(24, 81, 38, 0.12);
}

body.body--dark {
  --principia-bg: #06190d;
  --principia-pane: #0b2414;
  --principia-pane-muted: #10301b;
  --principia-text: #d7f5dc;
  --principia-border: #346a3f;
  --principia-border-strong: #7fd28d;
  --principia-control: #13301d;
  --principia-control-hover: #1b4529;
  --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
}

.principia-stage-supervised-learning {
  --principia-bg: #e5f5e8;
  --principia-pane: #effaf1;
  --principia-pane-muted: #d7eddb;
  --principia-text: #123d1f;
  --principia-border: #7dbb85;
  --principia-border-strong: #3d7d49;
  --principia-control: #ffffff;
  --principia-control-hover: #d7efdc;
  --principia-shadow: 0 18px 50px rgba(24, 81, 38, 0.12);
}

.principia-stage-reinforcement-learning {
  --principia-bg: #eeeeee;
  --principia-pane: #f8f8f8;
  --principia-pane-muted: #dddddd;
  --principia-text: #252525;
  --principia-border: #a9a9a9;
  --principia-border-strong: #696969;
  --principia-control: #ffffff;
  --principia-control-hover: #e1e1e1;
  --principia-shadow: 0 18px 50px rgba(60, 60, 60, 0.12);
}

@media (prefers-color-scheme: dark) {
  .principia-stage-supervised-learning {
    --principia-bg: #06190d;
    --principia-pane: #0b2414;
    --principia-pane-muted: #10301b;
    --principia-text: #d7f5dc;
    --principia-border: #346a3f;
    --principia-border-strong: #7fd28d;
    --principia-control: #13301d;
    --principia-control-hover: #1b4529;
    --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
  }

  .principia-stage-reinforcement-learning {
    --principia-bg: #171717;
    --principia-pane: #222222;
    --principia-pane-muted: #2f2f2f;
    --principia-text: #eeeeee;
    --principia-border: #5c5c5c;
    --principia-border-strong: #c4c4c4;
    --principia-control: #292929;
    --principia-control-hover: #3a3a3a;
    --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
  }
}

body.body--light .principia-stage-supervised-learning {
  --principia-bg: #e5f5e8;
  --principia-pane: #effaf1;
  --principia-pane-muted: #d7eddb;
  --principia-text: #123d1f;
  --principia-border: #7dbb85;
  --principia-border-strong: #3d7d49;
  --principia-control: #ffffff;
  --principia-control-hover: #d7efdc;
  --principia-shadow: 0 18px 50px rgba(24, 81, 38, 0.12);
}

body.body--light .principia-stage-reinforcement-learning {
  --principia-bg: #eeeeee;
  --principia-pane: #f8f8f8;
  --principia-pane-muted: #dddddd;
  --principia-text: #252525;
  --principia-border: #a9a9a9;
  --principia-border-strong: #696969;
  --principia-control: #ffffff;
  --principia-control-hover: #e1e1e1;
  --principia-shadow: 0 18px 50px rgba(60, 60, 60, 0.12);
}

body.body--dark .principia-stage-supervised-learning {
  --principia-bg: #06190d;
  --principia-pane: #0b2414;
  --principia-pane-muted: #10301b;
  --principia-text: #d7f5dc;
  --principia-border: #346a3f;
  --principia-border-strong: #7fd28d;
  --principia-control: #13301d;
  --principia-control-hover: #1b4529;
  --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
}

body.body--dark .principia-stage-reinforcement-learning {
  --principia-bg: #171717;
  --principia-pane: #222222;
  --principia-pane-muted: #2f2f2f;
  --principia-text: #eeeeee;
  --principia-border: #5c5c5c;
  --principia-border-strong: #c4c4c4;
  --principia-control: #292929;
  --principia-control-hover: #3a3a3a;
  --principia-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
}

body,
.nicegui-content {
  background: var(--principia-bg);
}

.nicegui-content {
  padding: 0 !important;
}

.principia-screen {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: var(--principia-bg);
  color: var(--principia-text);
  padding: 0;
}

.principia-shell {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 1px minmax(0, 1fr);
  gap: 0;
  align-items: stretch;
}

.principia-pane {
  min-width: 0;
  min-height: 0;
  border: none;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  overflow: hidden;
}

.principia-pane-left {
  display: grid;
  grid-template-rows: auto 1fr;
}

.principia-pane-right {
  display: flex;
  flex-direction: column;
}

.principia-vertical-separator {
  width: 1px;
  height: calc(100vh - (2 * var(--principia-separator-gap)));
  align-self: center;
  background: linear-gradient(
    transparent,
    var(--principia-border-strong),
    transparent
  );
}

.principia-toolbar-shell {
  padding: 18px 20px 0;
}

.principia-toolbar {
  display: flex;
  gap: 0;
  align-items: center;
}

.principia-toolbar-divider {
  height: 1px;
  margin: 16px 22px 0;
  background: linear-gradient(
    90deg,
    transparent,
    var(--principia-border-strong),
    transparent
  );
}

.principia-toolbar-button {
  min-width: 38px;
  height: 42px;
  border: none;
  border-radius: 0;
  background: transparent;
  color: var(--principia-text);
  padding: 0 10px;
}

.principia-toolbar-button + .principia-toolbar-button {
  border-left: 1px solid var(--principia-border-strong);
}

.principia-toolbar-button:hover {
  background: var(--principia-control-hover);
}

.principia-language-button {
  min-width: 46px;
}

.principia-language-menu {
  background: var(--principia-pane);
  color: var(--principia-text);
  border: 1px solid var(--principia-border);
  border-radius: 16px;
}

.principia-language-scroll {
  max-height: 160px;
  min-width: 86px;
}

.principia-settings-dialog .q-dialog__inner {
  padding: 24px;
}

.q-dialog__backdrop {
  background: rgba(6, 21, 13, 0.46);
}

.principia-settings-card {
  width: min(420px, calc(100vw - 48px));
  border: 1px solid var(--principia-border-strong);
  border-radius: 22px;
  background: var(--principia-pane);
  color: var(--principia-text);
  box-shadow: var(--principia-shadow);
  padding: 24px;
  gap: 18px;
}

.principia-settings-title {
  color: var(--principia-text);
  font-size: 1.25rem;
  font-weight: 650;
}

.principia-settings-control {
  width: 100%;
}

.principia-settings-card .q-field__label,
.principia-settings-card .q-field__native,
.principia-settings-card .q-field__append,
.principia-settings-card .q-field__control {
  color: var(--principia-text);
}

.principia-settings-card .q-field__control::before {
  border-color: var(--principia-border);
}

.principia-settings-card .q-field__control::after {
  background: var(--principia-border-strong);
}

.principia-settings-actions {
  width: 100%;
  justify-content: flex-end;
  gap: 0;
}

.principia-settings-button {
  border-radius: 0;
  color: var(--principia-text);
}

.principia-settings-save {
  border-left: 1px solid var(--principia-border-strong);
}

.principia-pane-content {
  min-height: 0;
  padding: 22px;
  overflow: auto;
}

.principia-window-title {
  color: var(--principia-text);
  width: 100%;
  font-size: clamp(1.35rem, 2.7vw, 2.25rem);
  font-weight: 650;
  letter-spacing: -0.04em;
  line-height: 1;
  text-align: center;
}

.principia-constitution-list {
  margin: 24px 0 0;
  padding-left: 1.2rem;
  color: var(--principia-text);
}

.principia-placeholder {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: var(--principia-pane-muted);
  color: var(--principia-text);
  letter-spacing: 0.02em;
}

@media (max-width: 760px) {
  .principia-screen {
    padding: 0;
    overflow: auto;
  }

  .principia-shell {
    min-height: 100%;
    grid-template-columns: 1fr;
    grid-template-rows: minmax(420px, 1fr) 1px minmax(420px, 1fr);
  }

  .principia-vertical-separator {
    width: calc(100vw - 12vh);
    height: 1px;
    justify-self: center;
    background: linear-gradient(
      90deg,
      transparent,
      var(--principia-border-strong),
      transparent
    );
  }
}
"""


def apply_theme() -> None:
    """Inject Principia's shared frontend theme CSS for the current page."""
    ui.add_head_html(f"<style>{_THEME_CSS}</style>")

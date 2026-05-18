"""Centralized frontend theme choices."""

from __future__ import annotations

from nicegui import ui

from principia.frontend.language import ThemeMode, get_user_theme_mode

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
  border-radius: 6px;
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
  border-radius: 8px;
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

.principia-window-title-button {
  min-height: auto;
  border-radius: 0;
  padding: 0;
}

.principia-window-title-button .q-btn__content {
  width: 100%;
  justify-content: center;
}

.principia-edit-navigation-title {
  color: var(--principia-text);
  width: 100%;
  justify-content: flex-start;
  border-radius: 0;
  font-size: clamp(1.3rem, 2.4vw, 2rem);
  font-weight: 650;
  opacity: 0.42;
  padding: 0 0 22px;
}

.principia-edit-navigation-title-enabled {
  opacity: 1;
}

.principia-edit-navigation-title-enabled:hover {
  background: var(--principia-control-hover);
}

.principia-constitution-stack {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 26px;
}

.principia-example-stack {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 26px;
}

.principia-test-stack {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.principia-link-row {
  width: 100%;
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 10px;
  align-items: stretch;
}

.principia-link-marker {
  width: 44px;
  height: 100%;
  min-height: 108px;
  align-self: stretch;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-control);
}

.principia-link-marker:hover,
.principia-link-marker-dirty {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-link-marker-selected {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
  box-shadow: inset 0 0 0 1px var(--principia-border-strong);
}

.principia-link-marker-muted {
  opacity: 0.52;
}

.principia-test-save-marker {
  font-size: 1.15rem;
  font-weight: 650;
}

.principia-constitution-widget {
  width: 100%;
  min-height: 108px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane-muted);
  color: var(--principia-text);
  padding: 16px 18px;
  text-align: left;
}

.principia-constitution-widget:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-constitution-widget .q-btn__content {
  width: 100%;
  justify-content: flex-start;
}

.principia-constitution-critique {
  width: 100%;
  color: var(--principia-text);
  display: -webkit-box;
  line-clamp: 4;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  white-space: normal;
  line-height: 1.45;
}

.principia-constitution-add {
  width: 100%;
  min-height: 58px;
  border: 1px dashed var(--principia-border-strong);
  border-radius: 6px;
  color: var(--principia-text);
  font-size: 1.8rem;
}

.principia-example-widget {
  width: 100%;
  min-height: 108px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane-muted);
  color: var(--principia-text);
  padding: 16px 18px;
  text-align: left;
}

.principia-example-widget:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-example-widget .q-btn__content {
  width: 100%;
  justify-content: flex-start;
}

.principia-link-widget-selected {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
  box-shadow: inset 0 0 0 1px var(--principia-border-strong);
}

.principia-example-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.principia-example-user {
  width: 100%;
  color: var(--principia-text);
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  white-space: normal;
  line-height: 1.45;
}

.principia-example-hash {
  width: 100%;
  color: var(--principia-text);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  line-height: 1.35;
  opacity: 0.68;
  overflow-wrap: anywhere;
}

.principia-example-add {
  width: 100%;
  min-height: 58px;
  border: 1px dashed var(--principia-border-strong);
  border-radius: 6px;
  color: var(--principia-text);
  font-size: 1.8rem;
}

.principia-example-add:hover {
  background: var(--principia-control-hover);
}

.principia-constitution-add:hover {
  background: var(--principia-control-hover);
}

.principia-red-team-widget {
  width: 100%;
  min-height: 108px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane-muted);
  color: var(--principia-text);
  padding: 16px 18px;
  text-align: left;
}

.principia-red-team-widget:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-red-team-widget .q-btn__content {
  width: 100%;
  justify-content: flex-start;
}

.principia-red-team-preview {
  width: 100%;
  color: var(--principia-text);
  display: -webkit-box;
  line-clamp: 4;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  white-space: normal;
  line-height: 1.45;
}

.principia-red-team-dialog .q-dialog__inner {
  padding: 24px;
}

.principia-red-team-card {
  width: min(1080px, calc(100vw - 48px));
  border: 1px solid var(--principia-border-strong);
  border-radius: 8px;
  background: var(--principia-pane);
  color: var(--principia-text);
  box-shadow: var(--principia-shadow);
  padding: 24px;
  gap: 18px;
}

.principia-red-team-title {
  color: var(--principia-text);
  font-size: 1.25rem;
  font-weight: 650;
}

.principia-red-team-list {
  width: 100%;
  min-height: 0;
  max-height: min(66vh, 620px);
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow: auto;
}

.principia-red-team-selector {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(220px, 0.42fr) minmax(280px, 0.58fr);
  gap: 18px;
  align-items: stretch;
}

.principia-dev-prompt-widget {
  width: 100%;
  min-height: 86px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane-muted);
  color: var(--principia-text);
  padding: 14px 16px;
  text-align: left;
}

.principia-dev-prompt-widget:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-dev-prompt-widget-selected {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
  box-shadow: inset 0 0 0 1px var(--principia-border-strong);
}

.principia-dev-prompt-widget .q-btn__content {
  width: 100%;
  justify-content: flex-start;
}

.principia-dev-prompt-user {
  width: 100%;
  color: var(--principia-text);
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  white-space: normal;
  line-height: 1.45;
}

.principia-red-team-chat {
  min-height: min(66vh, 620px);
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 14px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-control);
  padding: 16px;
}

.principia-red-team-chat-messages {
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow: auto;
}

.principia-chat-bubble {
  max-width: 82%;
  border: 1px solid var(--principia-border);
  border-radius: 14px;
  color: var(--principia-text);
  padding: 12px 14px;
  white-space: pre-wrap;
  line-height: 1.45;
}

.principia-chat-bubble-user {
  align-self: flex-end;
  border-bottom-right-radius: 4px;
  background: var(--principia-control-hover);
}

.principia-chat-bubble-bot {
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  background: var(--principia-pane-muted);
}

.principia-red-team-empty {
  color: var(--principia-text);
  opacity: 0.68;
}

.principia-red-team-select {
  width: 100%;
  min-height: 48px;
  border: 1px solid var(--principia-border-strong);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-pane-muted);
}

.principia-red-team-select:hover {
  background: var(--principia-control-hover);
}

.principia-red-team-selector-button {
  width: 100%;
  min-height: 46px;
  margin-top: 18px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-pane-muted);
}

.principia-red-team-selector-button:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-prompt-test-chat {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 14px;
  padding: 14px;
  max-height: min(60vh, 520px);
  overflow-y: auto;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-control);
}

.principia-prompt-test-action {
  width: 100%;
  min-height: 48px;
  margin-top: 14px;
  border: 1px solid var(--principia-border-strong);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-pane-muted);
}

.principia-prompt-test-action:hover {
  border-color: var(--principia-border-strong);
  background: var(--principia-control-hover);
}

.principia-constitution-edit-dialog .q-dialog__inner {
  padding: 24px;
}

.principia-example-edit-dialog .q-dialog__inner {
  padding: 18px;
}

.principia-constitution-edit-card {
  width: min(760px, calc(100vw - 48px));
  border: 1px solid var(--principia-border-strong);
  border-radius: 8px;
  background: var(--principia-pane);
  color: var(--principia-text);
  box-shadow: var(--principia-shadow);
  padding: 24px;
  gap: 18px;
}

.principia-example-edit-card {
  width: min(1240px, calc(100vw - 36px));
  height: min(840px, calc(100vh - 36px));
  max-width: none;
  border: 1px solid var(--principia-border-strong);
  border-radius: 8px;
  background: var(--principia-pane);
  color: var(--principia-text);
  box-shadow: var(--principia-shadow);
  padding: 18px;
  gap: 14px;
  display: flex;
  flex-direction: column;
}

.principia-constitution-edit-title {
  color: var(--principia-text);
  font-size: 1.25rem;
  font-weight: 650;
}

.principia-example-edit-title {
  color: var(--principia-text);
  font-size: 1.25rem;
  font-weight: 650;
}

.principia-example-edit-header {
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.principia-example-edit-close {
  min-width: 42px;
  min-height: 42px;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-control);
}

.principia-example-edit-close:hover {
  background: var(--principia-control-hover);
}

.principia-example-edit-body {
  width: 100%;
  min-height: 0;
  flex: 1;
  display: grid;
  grid-template-columns: minmax(360px, 0.92fr) minmax(0, 1.08fr);
  gap: 18px;
}

.principia-example-editor-pane,
.principia-example-chat-pane {
  width: 100%;
  min-width: 0;
  min-height: 0;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane-muted);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.principia-example-editor-pane {
  overflow-y: auto;
}

.principia-example-chat-title {
  color: var(--principia-text);
  font-size: 1rem;
  font-weight: 650;
}

.principia-example-chat-hint {
  color: var(--principia-text);
  opacity: 0.7;
  font-size: 0.9rem;
}

.principia-example-chat-history {
  width: 100%;
  min-width: 0;
  min-height: 0;
  flex: 1;
  overflow-y: auto;
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  background: var(--principia-pane);
  padding: 14px;
  gap: 10px;
}

.principia-example-chat-bubble {
  max-width: 88%;
  padding: 10px 12px;
  border-radius: 8px;
  line-height: 1.45;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  border: 1px solid var(--principia-border);
}

.principia-example-chat-bubble-user {
  align-self: flex-end;
  background: var(--principia-control-hover);
}

.principia-example-chat-bubble-assistant {
  align-self: flex-start;
  background: var(--principia-control);
}

.principia-example-chat-send-row {
  width: 100%;
  min-width: 0;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 48px;
  gap: 8px;
  align-items: stretch;
}

.principia-example-chat-input {
  width: 100%;
  min-width: 0;
}

.principia-example-chat-input .q-field__inner {
  width: 100%;
}

.principia-example-chat-send,
.principia-example-chat-action {
  border: 1px solid var(--principia-border);
  border-radius: 6px;
  color: var(--principia-text);
  background: var(--principia-control);
}

.principia-example-chat-send:hover,
.principia-example-chat-action:hover {
  background: var(--principia-control-hover);
}

.principia-example-chat-actions {
  width: 100%;
  min-width: 0;
  gap: 10px;
  justify-content: flex-end;
}

.principia-example-chat-action {
  min-width: 150px;
}

.principia-constitution-edit-field {
  width: 100%;
}

.principia-example-edit-field {
  width: 100%;
}

.principia-constitution-edit-field textarea {
  min-height: 140px;
}

.principia-example-edit-field textarea {
  min-height: 110px;
}

.principia-constitution-edit-card .q-field__label,
.principia-constitution-edit-card .q-field__native,
.principia-constitution-edit-card .q-field__control,
.principia-example-edit-card .q-field__label,
.principia-example-edit-card .q-field__native,
.principia-example-edit-card .q-field__control {
  color: var(--principia-text);
}

.principia-constitution-edit-card .q-field__control::before,
.principia-example-edit-card .q-field__control::before {
  border-color: var(--principia-border);
}

.principia-constitution-edit-card .q-field__control::after,
.principia-example-edit-card .q-field__control::after {
  background: var(--principia-border-strong);
}

.principia-constitution-edit-actions {
  width: 100%;
  justify-content: flex-end;
  gap: 12px;
}

.principia-example-edit-actions {
  width: 100%;
  justify-content: flex-end;
  gap: 12px;
}

.principia-constitution-edit-button {
  border-radius: 6px;
  min-width: 96px;
}

.principia-example-edit-button {
  border-radius: 6px;
  min-width: 96px;
}

.principia-constitution-edit-save {
  background: #2f9e44;
  color: #ffffff;
}

.principia-example-edit-save {
  background: #2f9e44;
  color: #ffffff;
}

.principia-constitution-edit-delete {
  background: #c92a2a;
  color: #ffffff;
}

.principia-example-edit-delete {
  background: #c92a2a;
  color: #ffffff;
}

.principia-placeholder {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
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

  .principia-red-team-selector {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .principia-example-edit-card {
    height: calc(100vh - 24px);
    width: calc(100vw - 24px);
  }

  .principia-example-edit-body {
    grid-template-columns: 1fr;
  }

  .principia-example-chat-pane {
    min-height: 480px;
  }
}
"""


def apply_theme() -> None:
    """Inject Principia's shared frontend theme CSS for the current page."""
    if get_user_theme_mode() == ThemeMode.DARK:
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()

    ui.add_head_html(f"<style>{_THEME_CSS}</style>")

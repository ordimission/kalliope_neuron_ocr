# Translate

## Synopsis

Neuron to translate sentence with google API

## Installation

```bash
kalliope install --git-url TODO
```

## Options

| parameter | required | default | choices                                | comments                                                                       |
|-----------|----------|---------|----------------------------------------|--------------------------------------------------------------------------------|
| lang_out  | yes      |         | E.g: "en", "fr", "Spanish", "Français" | Language to translate sentence: langage id ("en") or language name ("Spanish") |
| lang_in   | no       |  auto   | E.g: "auto", "en", "fr"                | Language of original sentence: "auto" for automatique detection or lang id     |
| sentence  | yes      |         |                                        | Sentence translate                                                             |

## Return Values

| Name     | Description           | Type   | sample          |
|----------|-----------------------|--------|-----------------|
| result   | Result of translation | string | "Buenas noches" |
| lang_in  | lang id in            | string | "en"            |
| lang_out | lang id out           | string | "es"            |

## Synapses example

```yml
  - name: "translate-es"
    signals:
      - order: "translate {{sentence}} in Spanish"
    neurons:
      - translate:
          lang_in: "fr"
          lang_out: "es"
          args:
            - sentence
          say_template: "{{ result }}"
          tts:
            pico2wave:
              language: "es-ES"
```


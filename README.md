# Ocr

## Synopsis

Neuron to perform OCR with google cloud vision API or tesseract

## Installation

```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fra

export GOOGLE_APPLICATION_CREDENTIALS=/path_to_google_key.json

kalliope install --git-url https://github.com/ordimission/kalliope_neuron_ocr
```

## Options

| parameter | required | default | choices                                | comments                                                                         |
|-----------|----------|---------|----------------------------------------|----------------------------------------------------------------------------------|
| engine    | no       |         | E.g: "en", "fr", "Spanish", "Français" | Language to translate sentence: langage code ("en") or language name ("Spanish") |
| lang      | no       |  auto   | E.g: "auto", "en", "fr"                | Language of original sentence: "auto" for automatique detection or lang code     |
| image_path| yes      |         |                                        | Sentence translate                                                               |

[Langage support and ISO-639-1 Code](https://cloud.google.com/translate/docs/languages) 

## Return Values

| Name     | Description           | Type   | sample          |
|----------|-----------------------|--------|-----------------|
| result   | Result of detection   | string | "Buenas noches" |
| lang     | detected language     | string | "en"            |
| 
## Synapses example with override voice parameter

```yml
- name: "ocr-fr"
  signals:
    - order: "reconnais le texte"
  neurons:
    - ocr:
        lang: "fr"
        engine: "tesseract"
        image_path: /path/to.png
        say_template: 
          - "{{ result }}"
        tts:             
          pico2wave:
            language: "fr-FR"
            cache: False
```

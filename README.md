# GitHub Manager - CLI

Una aplicació per gestionar GitHub des de la línia de comandaments. Aquesta aplicació et permet interactuar amb diversos aspectes de GitHub, com gestionar repositoris, organitzacions, membres, etc., directament des del terminal via l'api oficial de github.

## Setup

Per començar a utilitzar l'aplicació, primer cal generar un `.env`. Això ho podem fer duplicant el `.env-example` i afegint el nostre token corresponent de github. [Documentació oficial](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28)   

## Instal·lació

Ara cal instal·lar les dependències necessàries. Pots fer-ho amb el següent comandament:

```bash
pip install -r requirements.txt
```

## Execució

Per executar l'aplicació, simplement crida el fitxer principal (`app.py`) des del terminal:

```bash
python app.py
```

Això iniciarà la interfície de línia de comandaments on podràs interactuar amb les funcionalitats de l'aplicació.

## Docker
També pots executar l'aplicació utilitzant Docker. Primer, assegura't de tenir Docker i Docker Compose instal·lats.

Construir la imatge Docker

```bash
docker-compose build
```

Executar l'aplicació amb Docker

```bash
docker-compose up
```

Això iniciarà l'aplicació dins d'un contenidor Docker.


## Tests

Per assegurar-te que l'aplicació funciona correctament, pots executar els tests unitats. Per a això, utilitzem la biblioteca `unittest`. Per executar-los, utilitza el següent comandament:

```bash
python -m unittest discover src/tests
```

Aquest comandament descobrirà i executarà tots els tests definits en el directori `src/tests` de l'aplicació.

## Documentació de l'API utilitzada

L'aplicació fa servir l'API de **GitHub REST** per realitzar diverses operacions. [Documentació oficial](https://docs.github.com/en/rest)

---


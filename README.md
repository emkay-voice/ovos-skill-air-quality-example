# Ask the web: air quality and UV

Ask **"how is the air quality?"** or **"what is the UV index today?"** and the
skill asks a web service – [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api),
free, no account, no key – about the place your device is set to, and says
the answer, in all twelve of [Emkay](https://emkay.ai)'s languages.

**👉 The friendly guide: <https://dev.emkay.ai>**

## What it shows

- **Calling a web service:** `requests.get(URL, params=..., timeout=10)`,
  then `.json()`. In Emkay this runs in your browser, so the service must
  allow it (CORS) – Open-Meteo does. Emkay's *What's happening?* view shows
  every call the skill makes and where it went.
- **Where the device is:** `self.location` (the coordinates) and
  `self.location_pretty` (the place name), from Settings → location.
- **When it goes wrong:** no location, no network, a service that does not
  answer – the skill says so (`no_location.dialog`, `no_connection.dialog`)
  instead of staying silent.
- **Two intents, one skill:** `air.intent` and `uv.intent`.
- **Words per language for numbers:** `air_levels.list` and `uv_levels.list`
  hold the word for each level, one per line, in order.

## Try changing

- `CURRENT` – Open-Meteo knows more (pollen in Europe, dust, ozone …): add one
  and a third intent that asks for it;
- the words for the levels, or what it says (`air_now.dialog`, `uv_now.dialog`);
- or point it at another free service – the shape stays the same.

## Try it

- **Emkay Dev (VS Code):** *Emkay: Run the skill in Emkay* (Ctrl+Alt+E) opens
  Emkay next to your code and loads the skill; type under Emkay to talk to it.
  Every save loads it again. *Emkay: Test the skill* sends the golden
  utterances and shows ✓ / ✗ in the Testing view. Emkay's menu →
  *Guardian* → *What's happening?* shows which skill took a sentence, and why.
- **ovos-tui-client (Codespaces, Dev Container):** run `ovos-tui` in the
  terminal, type to talk, `Ctrl+P` → *Test* runs the same golden utterances
  against a full OpenVoiceOS.
- **pytest:** `pytest -q` – no OpenVoiceOS needed.

When you make a repository from this template ("Use this template"), a
small workflow renames the skill after your repository and then removes
itself.

## Show it, on your own Emkay, and into the store

To show it in [See my skill](https://dev.emkay.ai/#gallery) on dev.emkay.ai –
ready or not – add the topic `emkay-skill` to the repository (the ⚙ next to
*About*). Remove the topic, or make the repository private, to take it away.

*Emkay: Send to my Emkay* shows a QR code that installs this skill from
GitHub on the Emkay you scan it with. To get it into the
[Emkay store](https://store.emkay.ai): topics `ovos` and `openvoiceos` on the
repository, a release on GitHub (`publish.yml` puts it on PyPI), and the
store's nightly test does the rest – <https://dev.emkay.ai/#store>.

More on writing skills:
[the OpenVoiceOS technical manual](https://openvoiceos.github.io/ovos-technical-manual/).

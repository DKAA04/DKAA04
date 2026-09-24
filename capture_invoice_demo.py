"""Capture the real local application with synthetic examples, no network I/O."""
from pathlib import Path
import json, os, sys
from unittest.mock import patch
import httpx

repo=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
os.chdir(repo)
sys.path.insert(0,str(repo))
for key in list(os.environ):
    if any(x in key for x in ('GOOGLE_API','GEMINI_API','E_INVOICE','EINVOICE','COMPANY_','DEMO_CUSTOMER','PEPPOL_ID')):
        del os.environ[key]
os.environ['CREATE_REAL_UBL']='0'
from fastapi.testclient import TestClient
with patch("dotenv.load_dotenv", return_value=False):
    from main import app
from demo_scenarios import DEMO_SCENARIOS

# TestClient dispatches in process; external HTTP must fail if accidentally used.
with patch('compliance.send_einvoice_document', side_effect=AssertionError('External transmission blocked')):
    client=TestClient(app)
    fixtures={p:client.get(p).json() for p in ['/health','/demo/scenarios','/chart-of-accounts']}
    fixtures['/reset']=client.post('/reset').json()
    fixtures['examples']={}
    for scenario in DEMO_SCENARIOS:
        client.post('/reset')
        response=client.post('/chat',json={'message':scenario['message']})
        response.raise_for_status()
        data=response.json()
        assert not data['compliance']['transmission_attempted']
        fixtures['examples'][scenario['message']]=data

# Omit even the original demo bank/address identifiers from the public replay.
serialized=json.dumps(fixtures,ensure_ascii=False)
for original, replacement in [('BE68539007547034','TEST-ONLY-NO-BANK-ACCOUNT'),('BE0999970129','TEST-VAT-ID'),('0208:0999970129','TEST-PEPPOL-ID'),('Wetstraat 1, 1000 Brussels','Synthetic example address')]:
    serialized=serialized.replace(original,replacement)
(out/'invoice-fixtures.json').write_text(serialized)
s=(repo/'static/index.html').read_text()
s=s.replace('PEPPOL compliance proof plus Belgian double-entry accounting','Recorded local demo · synthetic inputs · no live AI or invoice sending')
s=s.replace('WhatsApp-simple invoice agent','Explore four bookkeeping scenarios')
s=s.replace('Send a normal sentence or PDF. The backend extracts intent, creates compliance evidence, allocates a PCMN account, and posts balanced books.','Choose a sample to inspect an actual response captured from the Python backend. Each sample starts with an empty ledger. Identifiers are deliberately invalid test placeholders.')
s=s.replace('Start with the golden path: supplier bill, client invoice, client payment. Every step updates the proof stack and ledger in real time.','Select a scenario above. This replay lets you inspect document checks, journal entries and the trial balance without uploading any data.')
s=s.replace('<label class="fileBtn">Upload PDF<input id="pdfInput" type="file" accept="application/pdf" hidden></label>','<input id="pdfInput" type="file" hidden disabled>')
s=s.replace('<input class="input" id="messageInput"','<input class="input" id="messageInput" readonly aria-label="Selected synthetic example"')
s=s.replace('>Send</button>','>Replay</button>').replace(' : "Send";', ' : "Replay";')
s=s.replace('Compliance Proof','Document checks').replace('Compliance proof','Document checks')
s=s.replace('Working through extraction, compliance, VAT, allocation, and balanced posting...','Loading the recorded Python response...')
a=s.index('async function api(path, options) {');b=s.index('\nasync function sendMessage',a)
s=s[:a]+'const recorded = '+serialized.replace('</','<\\/')+''';
async function api(path, options) {
  if (path === "/chat") {
    const message=JSON.parse(options.body).message;
    if (!recorded.examples[message]) throw new Error("Choose one of the four recorded examples");
    return structuredClone(recorded.examples[message]);
  }
  if (!(path in recorded)) throw new Error("This action requires running the source locally");
  return structuredClone(recorded[path]);
}
'''+s[b:]
s=s.replace('<body>','<body><div style="padding:10px 20px;background:#172535;color:#c7d5e6;font:13px system-ui"><a style="color:#7ee2c0" href="./index.html">← Portfolio demos</a> · <a style="color:#7ee2c0" href="https://github.com/DKAA04/Stripe_hackathon_Einvoicing">Source code</a> · Recorded demonstration; not accounting advice.</div>')
s=s.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; img-src data:; base-uri \'none\'; form-action \'none\'">')
(out/'invoice.html').write_text(s)
print('Captured four real synthetic-input responses; replay has no network API calls.')

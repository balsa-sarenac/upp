"""Preview the existing Reveal.js slides; rebuild HTML after saving Markdown."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import threading
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--class', dest='lesson', choices=['class1', 'class2'], default='class2')
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--no-open', action='store_true')
args = parser.parse_args()
folder = ROOT / '2026-2027/vjezbe' / args.lesson
source = folder / f'{args.lesson}.md'
target = source.with_suffix('.html')
lock = threading.Lock()
state = {'signature': None, 'revision': 0, 'error': ''}


def rebuild():
    files = [source, ROOT / 'Makefile', * (ROOT / 'common').glob('*.css'),
             *folder.glob('*.css'), *(folder / 'bpmn-class2').glob('*.svg')]
    signature = [(str(p), p.stat().st_mtime_ns) for p in files]
    with lock:
        if signature != state['signature']:
            result = subprocess.run(['make', str(target.relative_to(ROOT))], cwd=ROOT,
                                    capture_output=True, text=True)
            state['signature'] = signature
            state['error'] = result.stderr if result.returncode else ''
            if result.returncode:
                print(state['error'], flush=True)
            else:
                state['revision'] += 1
                print(f'Updated {target.name}', flush=True)
        return {'revision': state['revision'], 'error': state['error']}


SCRIPT = '''<script>
let revision;
setInterval(async () => {
  try {
    const state = await (await fetch('/__revision', {cache:'no-store'})).json();
    let error = document.getElementById('preview-error');
    if (state.error) {
      if (!error) {
        error = document.createElement('pre'); error.id = 'preview-error';
        error.style.cssText = 'position:fixed;inset:0 0 auto;z-index:99999;background:#fee;color:#800;padding:20px;white-space:pre-wrap;font:16px monospace';
        document.body.append(error);
      }
      error.textContent = state.error;
    } else {
      if(error) error.remove();
      if(revision !== undefined && revision !== state.revision) location.reload();
      revision = state.revision;
    }
  } catch (_) {}
}, 1000);
</script>'''


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/__revision':
            data = json.dumps(rebuild()).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
        elif self.path.split('?')[0] == '/' + str(target.relative_to(ROOT)):
            rebuild()
            data = target.read_text().replace('</body>', SCRIPT + '</body>').encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

    def log_message(self, *unused):
        pass


if __name__ == '__main__':
    rebuild()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT)))
    url = f'http://127.0.0.1:{args.port}/{target.relative_to(ROOT)}'
    print(f'Edit: {source}\nPreview: {url}\nCtrl+C to stop.', flush=True)
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

# stub
# A Streamlit component for secure ML inference in a sandboxed iframe
import streamlit as st
import streamlit.components.v1 as components

def secure_ml_component(
    coop_enabled: bool = False,
    coep_enabled: bool = False,
    sandbox_opts: str = "allow-scripts",
    allow_same_origin: bool = False,
    allowed_sources: list[str] = None,
    allow_inline_scripts: bool = False,
    message_types: list[str] = None,
    height: int = 600
):
    """Renders the secure ML inference component in the Streamlit app."""
    if allowed_sources is None:
        allowed_sources = ["cdn.jsdelivr.net", "storage.googleapis.com"]
    if message_types is None:
        message_types = ["sandbox-info", "fetch-log", "status", "model-loaded", "inference-result"]
    sb_attrs = sandbox_opts
    if allow_same_origin:
        sb_attrs += " allow-same-origin"
    coop_meta = (f'<meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin"/>'
                if coop_enabled else "")
    coep_meta = (f'<meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp"/>'
                if coep_enabled else "")
    connect_src = " ".join([f"https://{d}" for d in allowed_sources] + ["'self'"])
    csp_meta = (
        "<meta http-equiv='Content-Security-Policy' "
        f"content=\"default-src 'none'; script-src 'self' 'unsafe-inline' https:; "
        f"style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
        f"connect-src {connect_src}; frame-src 'self';\">"
    )
    perm_meta = "<meta http-equiv='Permissions-Policy' content=\"camera=(), microphone=(), geolocation=()\">"
    html_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"UTF-8\">
    {coop_meta}
    {coep_meta}
    {csp_meta}
    {perm_meta}
    <style>
      body {{ font-family: sans-serif; color: #333; margin: 0; padding: 0; }}
      .status {{ background: #f0f0f0; padding: 0.5em; font-size: 0.9em; }}
      .controls {{ padding: 0.5em; }}
      .log {{ font-family: monospace; font-size: 0.85em; max-height: 8em; overflow-y: auto; background: #eef; margin: 0.5em 0; padding: 0.5em; }}
    </style>
  </head>
  <body>
    <div class=\"controls\">
      <p><b>Secure Context:</b> <span id=\"secure-status\">Unknown</span></p>
      <p>
        <label>Model source:
          <select id=\"model-source\">
            <option value=\"upload\">Upload Model File</option>
            <option value=\"url\">Fetch from URL</option>
          </select>
        </label>
      </p>
      <p id=\"upload-section\">
        <input type=\"file\" id=\"file-input\" accept=\".onnx,.json,.bin,.model\" />
      </p>
      <p id=\"url-section\" style=\"display:none;\">
        <input type=\"text\" id=\"model-url\" placeholder=\"https://example.com/model.onnx\" size=\"40\"/>
        <button id=\"fetch-btn\">Fetch Model</button>
      </p>
    </div>
    <div class=\"status\">
      <span id=\"secure-status\"></span> –  
      <span id=\"isolation-status\"></span>
    </div>
    <div><button id=\"run-inference\" disabled>Run Inference</button></div>
    <div class=\"log\" id=\"log\"></div>
    <iframe id=\"sandboxFrame\" sandbox=\"{sb_attrs}\" allow=\"cross-origin-isolated\"></iframe>
    <script>
      "use strict";
      // Outer frame script
      document.addEventListener('DOMContentLoaded', () => {
        const secureStatusEl = document.getElementById('secure-status');
        const isolationStatusEl = document.getElementById('isolation-status');
        secureStatusEl.textContent = 'isSecureContext: ' + window.isSecureContext;
        isolationStatusEl.textContent = 'crossOriginIsolated: ' + window.crossOriginIsolated;
        document.getElementById('model-source').onchange = function() {
          const val = this.value;
          document.getElementById('upload-section').style.display = val==='upload'?'block':'none';
          document.getElementById('url-section').style.display = val==='url'?'block':'none';
        };
        function log(msg) {
          const logEl = document.getElementById('log');
          const entry = document.createElement('div');
          entry.textContent = msg;
          logEl.appendChild(entry);
          logEl.scrollTop = logEl.scrollHeight;
        }
        function sendModel(buffer, name) {
          const frame = document.getElementById('sandboxFrame');
          frame.contentWindow.postMessage({type:'load-model', modelBuffer: buffer, name}, '*');
        }
        document.getElementById('file-input').onchange = e => {
          const file = e.target.files[0]; if(!file) return;
          file.arrayBuffer().then(buf => sendModel(buf, file.name));
        };
        document.getElementById('fetch-btn').onclick = async () => {
          const url = document.getElementById('model-url').value;
          if(!url.startsWith('https://')) { log('HTTPS only'); return; }
          if(!allowed_sources.some(d=>url.includes(d))) { log('Domain not allowed'); return; }
          try {
            const r=await fetch(url); const buf=await r.arrayBuffer(); sendModel(buf, url.split('/').pop());
          } catch(e) { log('Fetch error: '+e); }
        };
        const sandboxHtml = `<!DOCTYPE html><html><head>
          <meta charset="UTF-8">
          <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.12.0/dist/tf.min.js"
                  integrity="sha256-QWo7LDvxbWT2tbbQ97B53yJnYU3WhH/C8ycbRAkjPDc=" crossorigin="anonymous"></script>
          <script>
            "use strict";
            let model;
            const origFetch=window.fetch;
            window.fetch=(...args)=>{postMessage({type:'fetch-log',url:typeof args[0]==='string'?args[0]:args[0].url},'*');return origFetch.apply(this,args);};
            window.onmessage=async e=>{const d=e.data;
              if(d.type==='load-model'){const buf=new Uint8Array(d.modelBuffer);try{postMessage({type:'status',status:'Loading model...'},'*');const blob=new Blob([buf]),u=URL.createObjectURL(blob);model=await tf.loadGraphModel(u,{fromTFHub:false});URL.revokeObjectURL(u);postMessage({type:'model-loaded',success:true},'*');}catch(err){postMessage({type:'model-loaded',success:false,error:err.message},'*');}}
              if(d.type==='run-inference'){if(!model){postMessage({type:'inference-result',error:'No model'},'*');return;}try{const inp=tf.randomNormal(model.inputs[0].shape||[1]),out=await model.executeAsync(inp);const res=out.array?await out.array():out;postMessage({type:'inference-result',result:JSON.stringify(res).slice(0,100)},'*');}catch(err){postMessage({type:'inference-result',error:err.message},'*');}}
            };
            window.onload=()=>postMessage({type:'sandbox-info',isSecure:window.isSecureContext,isIsolated:window.crossOriginIsolated},'*');
          <\/script></head><body></body></html>`;
        document.getElementById('sandboxFrame').srcdoc=sandboxHtml;
        window.addEventListener('message', e=>{const d=e.data; if(!d||!d.type||!message_types.includes(d.type)) return; log(JSON.stringify(d)); if(d.type==='model-loaded'&&d.success)document.getElementById('run-inference').disabled=false;});
        document.getElementById('run-inference').onclick=_=>document.getElementById('sandboxFrame').contentWindow.postMessage({type:'run-inference'},'*');
      });
"""
    components.html(html_content, height=height)
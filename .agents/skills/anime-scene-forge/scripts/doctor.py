#!/usr/bin/env python3
"""Read-only capability probe; does not infer unavailable host image tools."""
import argparse,json,platform,shutil,subprocess,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',type=Path,default=Path.cwd());a=p.parse_args()
    root=a.workspace.resolve()
    if not root.exists():p.error('workspace does not exist')
    tools={}
    for name,flag in [('node','--version'),('npm','--version'),('ffmpeg','-version'),('ffprobe','-version'),('git','--version'),('uv','--version')]:
        path=shutil.which(name)
        if path:
            try:
                r=subprocess.run([path,flag],capture_output=True,text=True,timeout=10,shell=(platform.system()=='Windows' and name=='npm'))
                version=(r.stdout or r.stderr).splitlines()[0] if r.stdout or r.stderr else None
                tools[name]={'available':r.returncode==0,'executable':path,'version':version}
            except (OSError,subprocess.TimeoutExpired) as e:tools[name]={'available':False,'reason':type(e).__name__}
        else:tools[name]={'available':False}
    memory=None
    if platform.system()=='Darwin':
        r=subprocess.run(['sysctl','-n','hw.memsize'],capture_output=True,text=True)
        if r.returncode==0:memory=int(r.stdout)
    elif Path('/proc/meminfo').exists():
        first=Path('/proc/meminfo').read_text().splitlines()[0].split();memory=int(first[1])*1024
    report={'python':sys.version.split()[0],'platform':platform.system(),'machine':platform.machine(),'total_memory_bytes':memory,'free_disk_bytes':shutil.disk_usage(root).free,'tools':tools,'mlx_platform_candidate':platform.system()=='Darwin' and platform.machine()=='arm64','agent_capabilities_to_discover':['image generation or supplied artwork','image inspection','video playback','chosen TTS/video service access'],'scope':'Availability probe only; no model inference, application integration or artistic quality is certified.'}
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

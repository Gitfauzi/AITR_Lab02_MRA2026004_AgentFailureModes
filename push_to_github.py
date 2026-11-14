import urllib.request
import urllib.error
import json
import ctypes
import ctypes.wintypes
import subprocess

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', ctypes.wintypes.DWORD),
        ('Type', ctypes.wintypes.DWORD),
        ('TargetName', ctypes.wintypes.LPWSTR),
        ('Comment', ctypes.wintypes.LPWSTR),
        ('LastWritten', ctypes.wintypes.FILETIME),
        ('CredentialBlobSize', ctypes.wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', ctypes.wintypes.DWORD),
        ('AttributeCount', ctypes.wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', ctypes.wintypes.LPWSTR),
        ('UserName', ctypes.wintypes.LPWSTR),
    ]

# --- Read stored GitHub credential ---
advapi32 = ctypes.windll.advapi32
cred_ptr = ctypes.POINTER(CREDENTIAL)()
advapi32.CredReadW('git:https://github.com', 1, 0, ctypes.byref(cred_ptr))
c = cred_ptr.contents
token = bytes(c.CredentialBlob[:c.CredentialBlobSize]).decode('utf-16-le').strip()
username = c.UserName
advapi32.CredFree(cred_ptr)

print("Using GitHub account:", username)
print("Token prefix:", token[:8])

# --- Create the GitHub repository via API ---
repo_name = 'AITR_Lab02_MRA2026004_AgentFailureModes'
api_url = 'https://api.github.com/user/repos'
payload = json.dumps({
    'name': repo_name,
    'description': 'IEEE Research Paper: Failure Modes in Chained Tool-Calling LLM Agents | Lab Assignment 02 | IIIT-A AI Tools for Research | MRA2026004',
    'private': False,
    'auto_init': False,
    'has_issues': True,
    'has_wiki': False
}).encode('utf-8')

req = urllib.request.Request(api_url, data=payload, method='POST')
req.add_header('Authorization', 'token ' + token)
req.add_header('Accept', 'application/vnd.github+json')
req.add_header('Content-Type', 'application/json')
req.add_header('User-Agent', 'aitr-lab-push/1.0')

clone_url = None
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        clone_url = data['clone_url']
        html_url  = data['html_url']
        print("Repository created successfully!")
        print("URL:", html_url)
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    msg = body.get('message', str(body))
    print("API response:", msg)
    clone_url = 'https://github.com/' + username + '/' + repo_name + '.git'
    html_url  = 'https://github.com/' + username + '/' + repo_name
    print("Will try push to:", clone_url)

# --- Authenticated push ---
repo_dir = r'C:\Users\Sachin Kumar\.gemini\antigravity\scratch\AITR_Lab02_MRA2026004_AgentFailureModes'
auth_url = clone_url.replace('https://', 'https://' + username + ':' + token + '@')

subprocess.run(['git', 'remote', 'set-url', 'origin', auth_url], cwd=repo_dir)
result = subprocess.run(
    ['git', 'push', '-u', 'origin', 'main'],
    cwd=repo_dir,
    capture_output=True,
    text=True
)

print("\n--- Push Output ---")
if result.stdout:
    print(result.stdout)
if result.stderr:
    print(result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("\nSUCCESS! Repository is live at:", html_url)
    print("Paper direct link:", html_url + '/blob/main/paper/main.tex')
else:
    print("\nPush failed. Check token scope (needs 'repo' permission).")

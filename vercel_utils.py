import requests
import os
import base64

def deploy_to_vercel(VERCEL_TOKEN,PROJECT_NAME,FOLDER_PATH):
    def is_binary_file(filepath):
        binary_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.woff', '.woff2', '.ttf']
        return os.path.splitext(filepath)[1].lower() in binary_extensions

    def get_files(folder):
        files = []
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, folder)
                if is_binary_file(path):
                    with open(path, 'rb') as f:
                        encoded_data = base64.b64encode(f.read()).decode('utf-8')
                    files.append({
                        'file': rel_path.replace("\\", "/"),
                        'data': encoded_data,
                        'encoding': 'base64'
                    })
                else:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        text_data = f.read()
                    files.append({
                        'file': rel_path.replace("\\", "/"),
                        'data': text_data,
                        'encoding': 'utf-8'
                    })
        return files

    files = get_files(FOLDER_PATH)
    
    payload = {
        "name": PROJECT_NAME,
        "files": [{"file": f["file"], "data": f["data"], "encoding": f["encoding"]} for f in files],
        "projectSettings": {
            "framework": None,
            "buildCommand": None,        # For static projects, leave None
            "installCommand": None,      # No install command needed
            "outputDirectory": "public", # Assuming a "public" folder; change if different
            "rootDirectory": None,
            "devCommand": None
        }
    }
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post("https://api.vercel.com/v13/deployments", json=payload, headers=headers)
    
    if response.status_code == 200:
        return(f"✅ Deployment successful: {response.json()['url']}")
    else:
        return(f"❌ Deployment failed: {response.text}")

if __name__ == "__main__":
    deploy_to_vercel('xwAGSIcz23njxip9tr54vIhj','ruchi_indian_kitchen',"./ruchi_indian_kitchen")

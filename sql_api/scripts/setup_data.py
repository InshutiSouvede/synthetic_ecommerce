# scripts/setup_data.py
import gdown
import zipfile
import os

def download_dataset():
    try:
        print("📦 Downloading dataset from Google Drive...")
        
        # Google Drive file ID
        file_id = "1sFeqfBEaOvuJh6Zz49R6OVbbsNh38vDg"
        
        # Project root
        project_root = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        print(f"Data directory: {data_dir}")
        
        # Download zip file
        zip_path = os.path.join(data_dir, "dataset.zip")
        url = f"https://drive.google.com/uc?id={file_id}"
        
        print(f"Downloading from: {url}")
        print("⏳ This may take a few minutes (2.5GB)...")
        
        result = gdown.download(url, zip_path, quiet=False, fuzzy=True)
        
        if result is None:
            print("❌ Download failed!")
            return
        
        print(f"✅ Download complete: {zip_path}")
        print(f"File size: {os.path.getsize(zip_path) / (1024*1024):.2f} MB")
        
        # Extract zip file
        print("📂 Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        
        print("✅ Extraction complete!")
        
        # List extracted files
        print("\n📁 Extracted contents:")
        for root, dirs, files in os.walk(data_dir):
            level = root.replace(data_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{sub_indent}{file}")
            if len(files) > 5:
                print(f"{sub_indent}... and {len(files) - 5} more files")
        
        # Remove zip file
        os.remove(zip_path)
        print("\n🗑️  Removed temporary zip file.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    download_dataset()
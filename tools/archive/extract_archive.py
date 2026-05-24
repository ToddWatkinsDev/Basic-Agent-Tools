import zipfile
import tarfile
import os

def tool(func):
    func._is_tool = True
    return func

@tool
def extract_archive(filepath, dest_dir='.'):
    """Automatically unzip .zip or extract .tar.gz files."""
    try:
        os.makedirs(dest_dir, exist_ok=True)
        if filepath.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(dest_dir)
        elif filepath.endswith('.tar.gz') or filepath.endswith('.tgz'):
            with tarfile.open(filepath, 'r:gz') as tar_ref:
                tar_ref.extractall(dest_dir)
        elif filepath.endswith('.tar'):
            with tarfile.open(filepath, 'r:') as tar_ref:
                tar_ref.extractall(dest_dir)
        else:
            return "Unsupported archive format."
        return f"Extracted {filepath} to {dest_dir}"
    except Exception as e:
        return f"Error extracting archive: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(extract_archive(sys.argv[1]))

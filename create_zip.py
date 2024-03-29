import zipfile
import os
from pathlib import Path


def zip_dir(zip_name, source_dir):
    """Zip the contents of an entire directory, recursively."""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(
                    file_path, start=os.path.dirname(source_dir))
                zipf.write(file_path, arcname)


def create_lambda_package():
    bin_dir = 'bin'
    output_zip = f'{bin_dir}/lambda.zip'
    source_code_dir = 'src'
    requirements_dir = 'lib'

    Path(bin_dir).mkdir(parents=True, exist_ok=True)

    zip_dir(output_zip, source_code_dir)

    if Path(requirements_dir).exists():
        with zipfile.ZipFile(output_zip, 'a', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(requirements_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(
                        file_path, start=os.path.dirname(requirements_dir))
                    zipf.write(file_path, arcname)


if __name__ == '__main__':
    create_lambda_package()
